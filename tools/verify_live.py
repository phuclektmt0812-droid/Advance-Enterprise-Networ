#!/usr/bin/env python3
"""Non-destructive live network checks via SSH; only meaningful with running GNS3/EVE.

Writes raw command evidence and a JSON report. It NEVER claims that a static check
constitutes proof of networking behavior.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from getpass import getpass
import json
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.auto_provision import load_inventory, real_connector

COMMANDS = {
    'router': ['show ip interface brief', 'show ip ospf neighbor', 'show ipv6 ospf neighbor',
               'show standby brief', 'show ip route', 'show ip bgp summary',
               'show bgp ipv6 unicast summary', 'show ip nat statistics',
               'show crypto isakmp sa', 'show crypto ipsec sa',
               'show policy-map interface GigabitEthernet0/1'],
    'switch': ['show vlan brief', 'show interfaces trunk', 'show etherchannel summary',
               'show spanning-tree root', 'show ip dhcp snooping',
               'show ip arp inspection', 'show port-security',
               'show port-security interface GigabitEthernet0/3',
               'show port-security address'],
}


def checklist(device: dict, evidence: dict[str, str]) -> dict[str, bool | None]:
    """Only conservative checks; None means the captured output needs human review."""
    if device['role'] == 'switch':
        vlan = evidence.get('show vlan brief', '')
        channel = evidence.get('show etherchannel summary', '')
        trunk = evidence.get('show interfaces trunk', '')
        port_security = evidence.get('show port-security interface GigabitEthernet0/3', '')
        return {
            'required_VLANs_visible': all(re.search(rf'^\s*{v}\s+', vlan, re.M) for v in (10, 20, 30, 99)),
            'LACP_portchannel_P_indicators': bool(re.search(r'Po1\(SU\)', channel)) and bool(re.search(r'\(P\)', channel)),
            'trunk_status_visible': 'trunking' in trunk.lower(),
            'access_port_security_enabled': bool(re.search(r'Port Security\s*:\s*Enabled', port_security, re.I)),
            'access_port_security_maximum_2': bool(re.search(r'Maximum MAC Addresses\s*:\s*2', port_security, re.I)),
            'access_port_security_violation_restrict': bool(re.search(r'Violation Mode\s*:\s*Restrict', port_security, re.I)),
        }
    ospf = evidence.get('show ip ospf neighbor', '')
    bgp = evidence.get('show ip bgp summary', '')
    hsrp = evidence.get('show standby brief', '')
    # IOS BGP State/PfxRcd must be a number for Established (0 received prefixes is valid).
    established = []
    for line in bgp.splitlines():
        cols = line.split()
        if len(cols) >= 10 and (cols[0].startswith('172.31.') or
                                cols[0].startswith('198.51.100.') or
                                cols[0].startswith('203.0.113.') or
                                cols[0].startswith('10.')):
            if cols[-1].isdigit() and cols[1] == '4':
                established.append(cols[0])
    expected_peer_count = 4 if device.get('site') == 'hcmc' else 3
    return {
        'OSPF_FULL_neighbour': 'FULL' in ospf.upper(),
        'HSRP_state_visible': bool(re.search(r'Active|Standby', hsrp, re.I)),
        'IPv4_BGP_established_expected_peer_count': len(established) >= expected_peer_count,
        'IPsec_SA_state_manual_review': None,
        'NAT_translation_manual_review': None,
        'QoS_queue_counters_manual_review': None,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--only', nargs='*', default=None, help='Hostnames to check')
    args = p.parse_args()
    devices = load_inventory()
    if args.only:
        devices = [d for d in devices if d['hostname'] in args.only]
    username = os.environ.get('TVI_USERNAME') or input('SSH username: ')
    password = os.environ.get('TVI_PASSWORD') or getpass('SSH password: ')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out = ROOT / 'build' / 'evidence' / stamp
    out.mkdir(parents=True, exist_ok=True)
    report = {'created_utc': stamp, 'devices': []}
    failure = False
    for d in devices:
        evidence = {}
        conn = None
        try:
            conn = real_connector(device_type=d['device_type'], host=d['ip'], port=d['port'],
                                  username=username, password=password, secret=password,
                                  timeout=15)
            conn.enable()
            for cmd in COMMANDS[d['role']]:
                evidence[cmd] = conn.send_command(cmd, read_timeout=45)
            (out / f"{d['hostname']}.txt").write_text(
                '\n\n'.join(f'$ {c}\n{v}' for c, v in evidence.items()), encoding='utf-8')
            checks = checklist(d, evidence)
            if any(v is False for v in checks.values()):
                failure = True
            report['devices'].append({'hostname': d['hostname'], 'checks': checks})
            print(f'{d["hostname"]}: {checks}')
        except Exception as exc:
            failure = True
            report['devices'].append({'hostname': d['hostname'], 'error': f'{type(exc).__name__}: {exc}'})
            print(f'FAIL {d["hostname"]}: {exc}')
        finally:
            if conn is not None:
                conn.disconnect()
    (out / 'results.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(f'Raw evidence and conservative checks: {out}')
    print('NOTE: Manual ping, firewall-deny, DHCP, failover, and throughput tests are also required.')
    raise SystemExit(2 if failure else 0)


if __name__ == '__main__':
    main()
