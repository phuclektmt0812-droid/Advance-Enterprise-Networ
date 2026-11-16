#!/usr/bin/env python3
"""TVI Step 9: credential-safe, state-aware multi-device automation.

Run: python automation/auto_provision.py
Credentials: TVI_USERNAME / TVI_PASSWORD environment, otherwise getpass.
Requires netmiko and pyyaml for real SSH (tests supply a fake connector).
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from getpass import getpass
import logging
import os
from pathlib import Path
import re
from typing import Callable, Any
import yaml

ROOT = Path(__file__).resolve().parents[1]
AUTOMATION_DIR = Path(__file__).resolve().parent


@dataclass
class DeviceResult:
    hostname: str
    success: bool
    changed: bool
    message: str


def load_inventory(path: Path = AUTOMATION_DIR / 'inventory.yaml') -> list[dict]:
    with path.open(encoding='utf-8') as file:
        value = yaml.safe_load(file)
    devices = value['devices']
    if not devices or not all({'hostname', 'ip', 'device_type', 'role', 'port'} <= set(d) for d in devices):
        raise ValueError('inventory.yaml must define hostname, ip, port, role and device_type')
    if len({d['hostname'] for d in devices}) != len(devices):
        raise ValueError('Duplicate hostnames in inventory.yaml')
    return devices


def load_vlan_payload(path: Path = AUTOMATION_DIR / 'vlans.yaml') -> list[dict]:
    with path.open(encoding='utf-8') as file:
        vlans = yaml.safe_load(file)['vlans']
    if len({int(v['id']) for v in vlans}) != len(vlans):
        raise ValueError('Duplicate VLAN ID in automation/vlans.yaml')
    for vlan in vlans:
        vid = int(vlan['id'])
        name = str(vlan['name'])
        if not 1 <= vid <= 4094 or not re.fullmatch(r'[A-Z][A-Z0-9_-]{0,25}', name):
            raise ValueError(f'Unsafe VLAN entry: {vlan}')
    return vlans


def parse_vlan_brief(output: str) -> dict[int, str]:
    result = {}
    for line in output.splitlines():
        # Cisco IOS: "10   EXEC_FINANCE  active ..."
        match = re.match(r'^\s*(\d{1,4})\s+(\S+)\s+(active|suspended|act/lshut|act/unsup)\b', line)
        if match:
            result[int(match.group(1))] = match.group(2)
    return result


def compute_commands(running: str, vlan_brief: str, role: str, desired_vlans: list[dict]) -> list[str]:
    """Return only necessary configuration commands based on live state."""
    cmds = []
    if not re.search(r'^aaa new-model\s*$', running, re.MULTILINE):
        cmds.append('aaa new-model')
    if not re.search(r'^aaa authentication login default local\s*$', running, re.MULTILINE):
        cmds.append('aaa authentication login default local')
    if not re.search(r'^aaa authorization exec default local\s*$', running, re.MULTILINE):
        cmds.append('aaa authorization exec default local')
    if not re.search(r'^ntp server 10\.10\.60\.10(?:\s|$)', running, re.MULTILINE):
        cmds.append('ntp server 10.10.60.10')
    if not re.search(r'^logging (?:host )?10\.10\.60\.10(?:\s|$)', running, re.MULTILINE):
        cmds.append('logging host 10.10.60.10')
    if 'Authorized TVI training lab only.' not in running:
        cmds.append('banner motd ^CAuthorized TVI training lab only.^C')
    if role == 'switch':
        current = parse_vlan_brief(vlan_brief)
        for vlan in desired_vlans:
            vid, name = int(vlan['id']), vlan['name']
            if current.get(vid) != name:
                cmds.extend([f'vlan {vid}', f'name {name}', 'exit'])
    return cmds


def make_logger(path: Path) -> logging.Logger:
    path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(f'tvi.automation.{path.resolve()}')
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.FileHandler(path, encoding='utf-8')
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
        logger.addHandler(handler)
    return logger


def real_connector(**kwargs):
    try:
        from netmiko import ConnectHandler
    except ImportError as exc:
        raise RuntimeError('Netmiko missing: run pip install -r requirements.txt') from exc
    return ConnectHandler(**kwargs)


def capture(conn: Any, hostname: str, label: str, backups: Path) -> tuple[str, str]:
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
    running = conn.send_command('show running-config', read_timeout=60)
    brief = conn.send_command('show ip interface brief', read_timeout=60)
    (backups / f'{hostname}_{stamp}_{label}_backup.cfg').write_text(running + '\n', encoding='utf-8')
    (backups / f'{hostname}_{stamp}_{label}_interfaces.txt').write_text(brief + '\n', encoding='utf-8')
    return running, brief


def automate_device(
    device: dict, username: str, password: str, vlans: list[dict],
    connector: Callable[..., Any], backups: Path, logger: logging.Logger,
) -> DeviceResult:
    name = device['hostname']
    conn = None
    try:
        conn = connector(device_type=device['device_type'], host=device['ip'],
                         port=int(device['port']), username=username, password=password,
                         secret=password, timeout=15, conn_timeout=15)
        conn.enable()
        running, _ = capture(conn, name, 'before', backups)
        vlan_brief = conn.send_command('show vlan brief', read_timeout=30) if device['role'] == 'switch' else ''
        commands = compute_commands(running, vlan_brief, device['role'], vlans)
        if commands:
            output = conn.send_config_set(commands, read_timeout=90)
            if re.search(r'% (?:Invalid input|Incomplete command|Ambiguous command|Error)', output, re.I):
                raise RuntimeError(f'IOS rejected a configuration command on {name}; check device console')
            conn.send_command('write memory', read_timeout=60)
        capture(conn, name, 'after', backups)
        logger.info('%s success role=%s commands=%d', name, device['role'], len(commands))
        return DeviceResult(name, True, bool(commands), f'Applied {len(commands)} config commands')
    except Exception as exc:
        # Messages intentionally exclude passwords or configuration payloads.
        msg = f'{type(exc).__name__}: {str(exc).splitlines()[0][:160]}'
        logger.error('%s failed: %s', name, msg)
        return DeviceResult(name, False, False, msg)
    finally:
        if conn is not None:
            try:
                conn.disconnect()
            except Exception:
                logger.warning('%s disconnect failed', name)


def run(
    devices: list[dict], vlans: list[dict], username: str, password: str,
    connector: Callable[..., Any] = real_connector,
    base_dir: Path = ROOT / 'build' / 'automation_results',
) -> list[DeviceResult]:
    backups = base_dir / 'backups'
    backups.mkdir(parents=True, exist_ok=True)
    logger = make_logger(base_dir / 'logs' / 'automation.log')
    results = []
    for d in devices:
        result = automate_device(d, username, password, vlans, connector, backups, logger)
        results.append(result)
        print(f"{'PASS' if result.success else 'FAIL'} {result.hostname}: {result.message}")
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description='TVI Step 9 network automation')
    parser.add_argument('--inventory', type=Path, default=AUTOMATION_DIR / 'inventory.yaml')
    parser.add_argument('--vlans', type=Path, default=AUTOMATION_DIR / 'vlans.yaml')
    parser.add_argument('--only', nargs='*', default=None, help='Optional device hostnames')
    args = parser.parse_args()
    devices = load_inventory(args.inventory)
    if args.only:
        unknown = set(args.only) - {d['hostname'] for d in devices}
        if unknown:
            parser.error('Unknown hostname(s): ' + ', '.join(sorted(unknown)))
        devices = [d for d in devices if d['hostname'] in args.only]
    vlans = load_vlan_payload(args.vlans)
    username = os.environ.get('TVI_USERNAME') or input('SSH username: ')
    password = os.environ.get('TVI_PASSWORD') or getpass('SSH password: ')
    if not username or not password:
        parser.error('SSH credentials cannot be blank')
    results = run(devices, vlans, username, password)
    raise SystemExit(0 if all(r.success for r in results) else 2)


if __name__ == '__main__':
    main()
