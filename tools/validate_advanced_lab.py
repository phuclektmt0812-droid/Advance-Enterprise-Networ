#!/usr/bin/env python3
"""Validate the separate advanced-lab manifest; no device configs are deployed."""
from __future__ import annotations

import ipaddress
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "advanced_lab" / "topology.yaml"


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    addressing = data.get("addressing", {})
    reserved = [ipaddress.ip_network(x) for x in addressing.get("core_reserved", [])]
    pools: list[tuple[str, ipaddress._BaseNetwork]] = []

    for name, raw in addressing.get("blocks", {}).items():
        try:
            net = ipaddress.ip_network(raw, strict=True)
        except ValueError as exc:
            errors.append(f"invalid block {name}: {exc}")
            continue
        for core in reserved:
            if net.overlaps(core):
                errors.append(f"advanced block {name} overlaps core block {core}")
        for other_name, other in pools:
            if net.overlaps(other):
                errors.append(f"blocks {name} ({net}) and {other_name} ({other}) overlap")
        pools.append((name, net))

    for group, entries in addressing.get("links", {}).items():
        for raw in entries:
            try:
                net = ipaddress.ip_network(raw, strict=True)
            except ValueError as exc:
                errors.append(f"invalid link {group} {raw}: {exc}")
                continue
            if not any(net.subnet_of(parent) for _, parent in pools):
                errors.append(f"link {group} {net} is outside all advanced blocks")
            for core in reserved:
                if net.overlaps(core):
                    errors.append(f"link {group} {net} overlaps core block {core}")

    loopbacks = []
    for raw in addressing.get("vtep_loopbacks", []):
        try:
            host = ipaddress.ip_interface(raw)
            loopbacks.append(host)
            if not any(host.ip in parent for _, parent in pools):
                errors.append(f"VTEP loopback {raw} is outside advanced blocks")
        except ValueError as exc:
            errors.append(f"invalid VTEP loopback {raw}: {exc}")
    if len({str(x.ip) for x in loopbacks}) != len(loopbacks):
        errors.append("duplicate VTEP loopback address")

    evpn = data.get("evpn", {})
    vnis = evpn.get("vnis", [])
    vlan_ids = [x.get("vlan") for x in vnis]
    vni_ids = [x.get("vni") for x in vnis]
    if len(set(vlan_ids)) != len(vlan_ids):
        errors.append("duplicate EVPN VLAN ID")
    if len(set(vni_ids)) != len(vni_ids):
        errors.append("duplicate EVPN VNI")
    for item in vnis:
        try:
            ipaddress.ip_network(item["subnet"], strict=True)
        except (KeyError, ValueError) as exc:
            errors.append(f"invalid EVPN subnet in {item}: {exc}")

    vrfs = data.get("mpls", {}).get("customer_vrfs", [])
    names = [x.get("name") for x in vrfs]
    rds = [x.get("rd") for x in vrfs]
    if len(set(names)) != len(names):
        errors.append("duplicate MPLS VRF name")
    if len(set(rds)) != len(rds):
        errors.append("duplicate MPLS route distinguisher")

    required = {"evpn_vxlan", "mpls_l3vpn", "sdwan", "ngfw", "ztna_sase", "wireless"}
    missing = required - set(data.get("platform_requirements", {}))
    if missing:
        errors.append(f"missing platform requirements: {', '.join(sorted(missing))}")
    return errors


def main() -> int:
    try:
        data = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
        errors = validate(data)
    except (OSError, yaml.YAMLError) as exc:
        print(f"Unable to load advanced lab manifest: {exc}", file=sys.stderr)
        return 2
    if errors:
        print("Advanced lab validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Advanced lab validation: PASS")
    print("Manifest syntax, address blocks, link pools, EVPN IDs and MPLS VRFs are consistent.")
    print("This is static validation only; no vendor CLI or runtime network is tested.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
