#!/usr/bin/env python3
"""Strictly validate address-plan invariants; runs without virtual devices."""
from __future__ import annotations
import ipaddress
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_plan(path: Path | None = None) -> dict:
    with (path or ROOT / 'network_plan.yaml').open(encoding='utf-8') as file:
        return yaml.safe_load(file)


def validate(plan: dict) -> list[str]:
    errors = []
    lan: list[tuple[str, ipaddress.IPv4Network]] = []
    underlay: list[tuple[str, ipaddress.IPv4Network]] = []
    ipv6: list[tuple[str, ipaddress.IPv6Network]] = []
    for site, spec in plan['sites'].items():
        expected_site = ipaddress.ip_network(spec['base'] + '.0.0/16')
        for vid, subnet in spec['vlans'].items():
            net = ipaddress.ip_network(subnet, strict=True)
            if not net.subnet_of(expected_site):
                errors.append(f'{site}: VLAN {vid} outside {expected_site}')
            if net.num_addresses < 8:
                errors.append(f'{site}: VLAN {vid} too small for hosts/gateway')
            lan.append((f'{site} vlan{vid}', net))
            v6 = ipaddress.ip_network(f"2001:db8:{spec['ipv6_site']}:{vid}::/64")
            ipv6.append((f'{site} vlan{vid}', v6))
        t = ipaddress.ip_network(spec['transit'])
        underlay.append((f'{site} transit', t))
        for i, loop in enumerate(spec['loopbacks']):
            underlay.append((f'{site} loopback R{i+1}', ipaddress.ip_network(loop)))
        if len(set(spec['vlans'])) != len(spec['vlans']):
            errors.append(f'{site}: duplicate VLAN IDs')
    for name, wan in plan['wan']['links'].items():
        net = ipaddress.ip_network(wan['network'])
        underlay.append((f'WAN {name}', net))
        for key in ('router_ip', 'isp_ip'):
            if ipaddress.ip_address(wan[key]) not in net.hosts():
                errors.append(f'{name}: {key} not a usable WAN host')
    for tun in plan['wan']['tunnels']:
        underlay.append((tun['name'], ipaddress.ip_network(tun['subnet'])))
        ipv6.append((tun['name'], ipaddress.ip_network(tun['ipv6'])))
    underlay.append(('ISP-ISP', ipaddress.ip_network(plan['wan']['isp_interconnect'])))
    underlay.append(('INTERNET_TEST', ipaddress.ip_network(plan['wan']['internet_test_link'])))
    # LAN VLAN networks are intentionally inside site /16s. Other networks must not overlap one another.
    for nets, name in ((lan + underlay, 'IPv4'), (ipv6, 'IPv6')):
        for i, (label_a, a) in enumerate(nets):
            for label_b, b in nets[i + 1:]:
                if a.overlaps(b):
                    errors.append(f'{name}: {label_a} ({a}) overlaps {label_b} ({b})')
    for site in plan['sites']:
        expected = {'hcmc': '65010', 'hanoi': '65020', 'danang': '65030'}[site]
        if str(plan['sites'][site]['asn']) != expected:
            errors.append(f'{site}: unexpected BGP AS')
    return errors


def main():
    errs = validate(load_plan())
    if errs:
        print('ADDRESS PLAN INVALID:')
        for err in errs:
            print(f'  - {err}')
        raise SystemExit(1)
    print('PASS: All allocated VLAN, transit, loopback, WAN, and tunnel networks are non-overlapping.')


if __name__ == '__main__':
    main()
