#!/usr/bin/env python3
"""TVI network baseline and backup automation.

Default behavior is read-only backup collection. Configuration changes require
an explicit --apply-vlans flag. Credentials are prompted interactively and are
never read from or written to inventory.yaml.
"""
from __future__ import annotations

import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from getpass import getpass
from typing import Any

import yaml
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

ROOT = Path(__file__).resolve().parent
INVENTORY = ROOT / "inventory.yaml"
BACKUP_DIR = ROOT / "backups"
LOG_DIR = ROOT / "logs"
VLAN_BASELINE = [
    "vlan 10", " name Executive",
    "vlan 20", " name Engineering",
    "vlan 30", " name Logistics",
    "vlan 99", " name Management",
]
SHOW_COMMANDS = {
    "running_config": "show running-config",
    "interface_brief": "show ip interface brief",
}


def setup_logging() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(LOG_DIR / "automation.log", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def load_inventory(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise FileNotFoundError(f"Inventory not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    devices = data.get("devices", [])
    if not isinstance(devices, list):
        raise ValueError("inventory.devices must be a list")
    validated = []
    for item in devices:
        if not isinstance(item, dict):
            raise ValueError("Each device entry must be a mapping")
        if item.get("enabled", True) is False:
            continue
        required = ("name", "host", "device_type")
        missing = [key for key in required if not item.get(key)]
        if missing:
            raise ValueError(f"Device entry missing {', '.join(missing)}: {item}")
        item.setdefault("port", 22)
        validated.append(item)
    return validated


def connect(device: dict[str, Any], username: str, password: str):
    params = {
        "device_type": device["device_type"],
        "host": device["host"],
        "port": int(device.get("port", 22)),
        "username": username,
        "password": password,
        "fast_cli": False,
        "conn_timeout": 15,
        "auth_timeout": 15,
        "banner_timeout": 15,
    }
    return ConnectHandler(**params)


def backup_device(device: dict[str, Any], username: str, password: str) -> bool:
    name = str(device["name"])
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    target_dir = BACKUP_DIR / name
    target_dir.mkdir(parents=True, exist_ok=True)
    connection = None
    try:
        connection = connect(device, username, password)
        for label, command in SHOW_COMMANDS.items():
            output = connection.send_command(command, read_timeout=60)
            target = target_dir / f"{timestamp}-{label}.txt"
            target.write_text(output.rstrip() + "\n", encoding="utf-8")
            logging.info("%s: saved %s", name, target.relative_to(ROOT))
        return True
    except (NetmikoAuthenticationException, NetmikoTimeoutException) as exc:
        logging.error("%s: connection failed: %s", name, exc)
    except Exception:
        logging.exception("%s: backup failed", name)
    finally:
        if connection is not None:
            connection.disconnect()
    return False


def apply_vlan_baseline(device: dict[str, Any], username: str, password: str) -> bool:
    name = str(device["name"])
    connection = None
    try:
        connection = connect(device, username, password)
        current = connection.send_command("show vlan brief", read_timeout=45)
        commands = []
        for vlan_id, vlan_name in ((10, "Executive"), (20, "Engineering"),
                                   (30, "Logistics"), (99, "Management")):
            if f"{vlan_id} " not in current and f"{vlan_id}\n" not in current:
                commands.extend([f"vlan {vlan_id}", f" name {vlan_name}"])
        if commands:
            result = connection.send_config_set(commands)
            logging.info("%s: VLAN baseline applied", name)
            logging.debug("%s: %s", name, result)
        else:
            logging.info("%s: VLAN baseline already present", name)
        return True
    except (NetmikoAuthenticationException, NetmikoTimeoutException) as exc:
        logging.error("%s: configuration connection failed: %s", name, exc)
    except Exception:
        logging.exception("%s: VLAN configuration failed", name)
    finally:
        if connection is not None:
            connection.disconnect()
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, default=INVENTORY)
    parser.add_argument("--apply-vlans", action="store_true",
                        help="Create required VLANs on enabled inventory devices.")
    parser.add_argument("--skip-backup", action="store_true",
                        help="Skip the default pre-change and post-change backups.")
    args = parser.parse_args()

    setup_logging()
    try:
        devices = load_inventory(args.inventory)
    except Exception as exc:
        logging.error("Cannot load inventory: %s", exc)
        return 2
    if not devices:
        logging.warning("No enabled devices in inventory; nothing to do.")
        return 0

    username = os.getenv("TVI_NET_USERNAME") or input("Network username: ").strip()
    password = os.getenv("TVI_NET_PASSWORD") or getpass("Network password: ")
    if not username or not password:
        logging.error("Username and password are required.")
        return 2

    failed = []
    for device in devices:
        name = str(device["name"])
        logging.info("Processing %s (%s)", name, device["host"])
        if not args.skip_backup and not backup_device(device, username, password):
            failed.append(name + ":backup")
            continue
        if args.apply_vlans:
            if not apply_vlan_baseline(device, username, password):
                failed.append(name + ":vlan")
                continue
            if not args.skip_backup and not backup_device(device, username, password):
                failed.append(name + ":post-backup")

    if failed:
        logging.error("Completed with failures: %s", ", ".join(failed))
        return 1
    logging.info("Automation completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
