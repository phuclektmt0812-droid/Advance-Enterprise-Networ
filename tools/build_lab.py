#!/usr/bin/env python3
"""Generate Cisco IOSv/IOSvL2 lab configs, DHCP/DNS settings, and port matrix.

Requires: PyYAML. Run locally with `python tools/build_lab.py`.
Writes credentialed lab configs only under build/ (gitignored).
No Cisco images or running virtual networks are bundled.
"""
from __future__ import annotations
import csv
import ipaddress as ip
import os
from pathlib import Path
import secrets
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from validate_plan import load_plan, validate  # noqa: E402

G0 = 'GigabitEthernet0/0'
G1 = 'GigabitEthernet0/1'
G2 = 'GigabitEthernet0/2'


def host(net: str, n: int) -> str:
    return str(ip.ip_network(net).network_address + n)


def mask(net: str) -> str:
    return str(ip.ip_network(net).netmask)


def v6prefix(site: dict, vlan_id: int) -> str:
    return f"2001:db8:{site['ipv6_site']}:{vlan_id}::"


def write(path: Path, content: str, *, private: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + '\n', encoding='utf-8')
    if private:
        try:
            path.chmod(0o600)
        except OSError:
            pass


def load_or_create_secrets(build: Path) -> dict:
    path = build / 'secrets.local.env'
    if path.exists():
        info = dict(line.strip().split('=', 1) for line in path.read_text().splitlines()
                    if line.strip() and not line.startswith('#'))
    else:
        info = {
            'TVI_USERNAME': 'netadmin',
            'TVI_PASSWORD': secrets.token_urlsafe(18),
            'TVI_IPSEC_PSK': secrets.token_urlsafe(28),
        }
        write(path, '\n'.join(f'{key}={value}' for key, value in info.items()), private=True)
    required = ('TVI_USERNAME', 'TVI_PASSWORD', 'TVI_IPSEC_PSK')
    if any(not info.get(k) for k in required):
        raise ValueError('Missing required entry in build/secrets.local.env')
    return info


def base_config(hostname: str, cred: dict) -> list[str]:
    return [
        f'hostname {hostname}',
        'no ip domain-lookup',
        'ip domain name tvi.lab',
        'service password-encryption',
        f"username {cred['TVI_USERNAME']} privilege 15 secret 0 {cred['TVI_PASSWORD']}",
        f"enable secret 0 {cred['TVI_PASSWORD']}",
        'ip ssh version 2',
        'banner motd ^CAuthorized TVI training lab only.^C',
        'service timestamps log datetime msec',
        'line console 0',
        ' logging synchronous',
        'line vty 0 4',
        ' login local',
        ' transport input ssh',
        ' access-class MGMT-SOURCES in',
        'ip access-list standard MGMT-SOURCES',
        ' permit 10.10.99.0 0.0.0.255',
        ' permit 10.20.99.0 0.0.0.255',
        ' permit 10.30.99.0 0.0.0.255',
        ' deny any log',
    ]


def allowed_vlans(site: dict) -> list[int]:
    return sorted(set(site['vlans']) | {999})


def render_switch(site_name: str, spec: dict, which: int, cred: dict) -> str:
    hostname = f'{site_name.upper()}-SW{which}'
    allowed = ','.join(str(x) for x in allowed_vlans(spec))
    access_names = {10: 'EXEC_FINANCE', 20: 'ENGINEERING', 30: 'LOGISTICS',
                    50: 'GUEST', 60: 'SERVERS', 70: 'IOT',
                    80: 'VOICE', 99: 'MANAGEMENT', 999: 'BLACKHOLE'}
    c = base_config(hostname, cred)
    c += ['no ip routing', 'vtp mode transparent', 'spanning-tree mode rapid-pvst']
    for vid in allowed_vlans(spec):
        c.extend([f'vlan {vid}', f' name {access_names[vid]}'])
    c += [f'spanning-tree vlan {allowed} priority {4096 if which == 1 else 8192}']
    # Management SVI and virtual gateway; router subinterfaces use host .2/.3.
    c += [
        'interface Vlan99', ' description MANAGEMENT_SVI',
        f" ip address {host(spec['vlans'][99], 10 + which)} {mask(spec['vlans'][99])}",
        ' no shutdown',
        f"ip default-gateway {host(spec['vlans'][99], 1)}",
    ]
    # DHCP/ARP safeguards. Only trusted uplinks and port-channel bypass checks.
    snooped = ','.join(str(v) for v in spec['vlans'] if v not in (60, 99))
    c += ['ip dhcp snooping', 'no ip dhcp snooping information option',
          f'ip dhcp snooping vlan {snooped}', f'ip arp inspection vlan {snooped}']
    for ifname in (G0, 'Port-channel1'):
        c += [f'interface {ifname}', ' description ROUTER_TRUNK' if ifname == G0 else ' description LACP_PEER_SW',
              ' switchport mode trunk', ' switchport trunk native vlan 999',
              f' switchport trunk allowed vlan {allowed}',
              ' ip dhcp snooping trust', ' ip arp inspection trust', ' no shutdown']
    for i in (1, 2):
        c += [f'interface GigabitEthernet0/{i}', ' description LACP_TO_OTHER_SWITCH',
              ' switchport mode trunk', ' switchport trunk native vlan 999',
              f' switchport trunk allowed vlan {allowed}',
              ' channel-group 1 mode active', ' no shutdown']
    # Endpoints are not dual-homed in the teaching lab. Redundant network infrastructure remains.
    port_map = {3: (10 if site_name == 'hcmc' else 20 if site_name == 'hanoi' else 30) if which == 1 else 50}
    if which == 1:
        port_map[6] = 70
        port_map[7] = 80
        if site_name == 'hcmc':
            port_map[4] = 60
            port_map[5] = 99
    for number in range(3, 8):
        vlan = port_map.get(number, 999)
        c += [f'interface GigabitEthernet0/{number}',
              f' description {"ENDPOINT_VLAN" + str(vlan) if number in port_map else "DISABLED_UNUSED"}',
              ' switchport mode access', f' switchport access vlan {vlan}']
        if number in port_map:
            c += [' spanning-tree portfast', ' spanning-tree bpduguard enable']
            if site_name == 'hcmc' and number in (4, 5) and which == 1:
                c += [' ip dhcp snooping trust', ' ip arp inspection trust']
            c += [' no shutdown']
        else:
            c += [' shutdown']
    return '\n'.join(c)


def create_router(site_name: str, spec: dict, which: int, plan: dict, cred: dict) -> str:
    rid = f'{site_name}-r{which}'
    hostname = f'{site_name.upper()}-R{which}'
    wan = plan['wan']['links'][rid]
    internal = ip.ip_network(spec['transit'])
    other_internal = str(internal.network_address + (2 if which == 1 else 1))
    mine_internal = str(internal.network_address + which)
    v6_internal = f"2001:db8:fe:{spec['ipv6_site']}::{which}"
    other_v6_internal = f"2001:db8:fe:{spec['ipv6_site']}::{3 - which}"
    c = base_config(hostname, cred)
    c += [
        'ip routing', 'ipv6 unicast-routing',
        'ip cef', 'ipv6 cef',
        'ip prefix-list SITE-ONLY seq 5 permit 10.0.0.0/8 le 32',
        'ip prefix-list ISP-IN seq 5 deny 10.0.0.0/8 le 32',
        'ip prefix-list ISP-IN seq 10 permit 0.0.0.0/0 le 32',
        'ip prefix-list ISP-OUT seq 5 deny 0.0.0.0/0 le 32',
        'ipv6 prefix-list V6-SITES seq 5 permit 2001:db8::/32 le 48',
        'ip access-list extended NAT-ELIGIBLE',
        f" deny ip {spec['base']}.0.0 0.0.255.255 10.0.0.0 0.255.255.255",
        f" permit ip {spec['base']}.0.0 0.0.255.255 any",
        'route-map NAT-ROUTE permit 10', ' match ip address NAT-ELIGIBLE',
        'ipv6 access-list V6-GUEST-IN',
        f" deny ipv6 {v6prefix(spec, 50)}/64 2001:db8::/32",
        ' permit ipv6 any any',
        'ipv6 access-list V6-IOT-IN',
        f" permit ipv6 {v6prefix(spec, 70)}/64 host 2001:db8:10:60::20",
        f" deny ipv6 {v6prefix(spec, 70)}/64 2001:db8::/32",
        ' permit ipv6 any any',
        f'ip nat inside source route-map NAT-ROUTE interface {G1} overload',
        'ip access-list extended ACL-GUEST-IN',
        ' permit udp any eq bootpc any eq bootps',
        f" deny ip {host(spec['vlans'][50], 0)} {ip.ip_network(spec['vlans'][50]).hostmask} 10.0.0.0 0.255.255.255",
        f" permit ip {host(spec['vlans'][50], 0)} {ip.ip_network(spec['vlans'][50]).hostmask} any",
        'ip access-list extended ACL-IOT-IN',
        ' permit udp any eq bootpc any eq bootps',
        f" permit udp {host(spec['vlans'][70], 0)} {ip.ip_network(spec['vlans'][70]).hostmask} host {plan['services']['dns_dhcp']} eq domain",
        f" permit tcp {host(spec['vlans'][70], 0)} {ip.ip_network(spec['vlans'][70]).hostmask} host {plan['services']['dns_dhcp']} eq domain",
        f" permit ip {host(spec['vlans'][70], 0)} {ip.ip_network(spec['vlans'][70]).hostmask} host {plan['services']['iot_app']}",
        f" deny ip {host(spec['vlans'][70], 0)} {ip.ip_network(spec['vlans'][70]).hostmask} 10.0.0.0 0.255.255.255",
        f" permit ip {host(spec['vlans'][70], 0)} {ip.ip_network(spec['vlans'][70]).hostmask} any",
        'class-map match-any TVI-VOICE', ' match dscp ef',
        'class-map match-any TVI-VIDEO', ' match dscp af31',
        'policy-map TVI-WAN-OUT', ' class TVI-VOICE', '  priority percent 20',
        ' class TVI-VIDEO', '  bandwidth percent 15',
        ' class class-default', '  fair-queue',
        'policy-map TVI-MARK-VOICE', ' class class-default', '  set dscp ef',
        'interface GigabitEthernet0/0',
        ' description 8021Q_TRUNK_TO_SITE_SWITCH',
        ' no ip address', ' no shutdown',
    ]
    for vlan_id, subnet in spec['vlans'].items():
        num = int(vlan_id)
        gw = host(subnet, 1)
        own = host(subnet, which + 1)
        v6 = f'{v6prefix(spec, num)}{which + 1}'
        c += [f'interface {G0}.{num}', f' description {site_name.upper()}_VLAN_{num}',
              f' encapsulation dot1Q {num}', f' ip address {own} {mask(subnet)}',
              f' ipv6 address {v6}/64', ' ipv6 ospf 10 area 0',
              ' ip nat inside', f' standby {num} ip {gw}',
              f' standby {num} priority {110 if which == 1 else 100}',
              f' standby {num} track {G1} 30', f' standby {num} preempt']
        if num not in (60, 99):
            c += [f" ip helper-address {plan['services']['dns_dhcp']}"]
        if num == 50:
            c += [' ip access-group ACL-GUEST-IN in', ' ipv6 traffic-filter V6-GUEST-IN in']
        if num == 70:
            c += [' ip access-group ACL-IOT-IN in', ' ipv6 traffic-filter V6-IOT-IN in']
        if num == 80:
            c += [' service-policy input TVI-MARK-VOICE']
    c += [
        f'interface {G1}', f" description WAN_TO_{wan['provider']}",
        f" ip address {wan['router_ip']} {mask(wan['network'])}",
        ' ip nat outside', ' service-policy output TVI-WAN-OUT', ' no shutdown',
        f'interface {G2}', ' description SITE_LOCAL_OSPF_IBGP',
        f' ip address {mine_internal} {internal.netmask}',
        f' ipv6 address {v6_internal}/64', ' ipv6 ospf 10 area 0', ' no shutdown',
        'interface Loopback0', f" ip address {host(spec['loopbacks'][which - 1], 0)} 255.255.255.255",
        f" ipv6 address 2001:db8:fe:{spec['ipv6_site']}:1::{which}/128",
        ' ipv6 ospf 10 area 0',
        f"ip route 0.0.0.0 0.0.0.0 {wan['isp_ip']}",
        f"ip route {spec['base']}.0.0 255.255.0.0 Null0 250",
        f"ipv6 route 2001:db8:{spec['ipv6_site']}::/48 Null0 250",
    ]
    # Build IPsec-protected GRE tunnels on the respective R1/R2 paths.
    tubes = [t for t in plan['wan']['tunnels'] if rid in (t['a'], t['b'])]
    c += [
        'crypto isakmp policy 10', ' encr aes 256', ' hash sha',
        ' authentication pre-share', ' group 14', ' lifetime 86400',
        'crypto ipsec transform-set TVI-ESP esp-aes 256 esp-sha-hmac',
        ' mode transport',
        'crypto ipsec profile TVI-GRE-IPSEC', ' set transform-set TVI-ESP',
    ]
    peer_interfaces = []
    for tun in tubes:
        peer = tun['b'] if rid == tun['a'] else tun['a']
        peer_ip = plan['wan']['links'][peer]['router_ip']
        net = ip.ip_network(tun['subnet'])
        mine_ip = str(net.network_address + (1 if rid == tun['a'] else 2))
        other_ip = str(net.network_address + (2 if rid == tun['a'] else 1))
        v6net = ip.ip_network(tun['ipv6'])
        own_v6 = str(v6net.network_address + (1 if rid == tun['a'] else 2))
        other_v6 = str(v6net.network_address + (2 if rid == tun['a'] else 1))
        c += [f"crypto isakmp key {cred['TVI_IPSEC_PSK']} address {peer_ip}",
              f"interface Tunnel{tun['id']}", f" description IPSEC_GRE_{tun['name']}",
              f' ip address {mine_ip} {net.netmask}',
              f' ipv6 address {own_v6}/{v6net.prefixlen}',
              f' tunnel source {G1}', f' tunnel destination {peer_ip}',
              ' tunnel mode gre ip', ' tunnel protection ipsec profile TVI-GRE-IPSEC',
              ' ip tcp adjust-mss 1360', ' no shutdown']
        peer_as = plan['sites'][peer.split('-')[0]]['asn']
        peer_interfaces.append((other_ip, other_v6, peer_as))
    c += [
        'router ospf 10', f' router-id {spec["ospf_id"]}.{spec["ospf_id"]}.0.{which}',
        ' passive-interface default', f' no passive-interface {G2}',
        f" network {spec['base']}.0.0 0.0.255.255 area 0",
        'ipv6 router ospf 10', f' router-id {spec["ospf_id"]}.{spec["ospf_id"]}.0.{which}',
        ' passive-interface default', f' no passive-interface {G2}',
        f"router bgp {spec['asn']}",
        ' bgp log-neighbor-changes',
        f" neighbor {wan['isp_ip']} remote-as {plan['wan']['ispa_as'] if which == 1 else plan['wan']['ispb_as']}",
        f' neighbor {other_internal} remote-as {spec["asn"]}',
        f' neighbor {other_v6_internal} remote-as {spec["asn"]}',
    ]
    for peer_ip, peer_v6, remote_as in peer_interfaces:
        c += [f' neighbor {peer_ip} remote-as {remote_as}',
              f' neighbor {peer_v6} remote-as {remote_as}']
    c += [' address-family ipv4',
          f"  network {spec['base']}.0.0 mask 255.255.0.0",
          f"  neighbor {wan['isp_ip']} activate",
          f"  neighbor {wan['isp_ip']} prefix-list ISP-IN in",
          f"  neighbor {wan['isp_ip']} prefix-list ISP-OUT out",
          f'  neighbor {other_internal} activate',
          f'  neighbor {other_internal} next-hop-self',
          f'  neighbor {other_internal} prefix-list SITE-ONLY in',
          f'  neighbor {other_internal} prefix-list SITE-ONLY out']
    for peer_ip, _, _ in peer_interfaces:
        c += [f'  neighbor {peer_ip} activate',
              f'  neighbor {peer_ip} prefix-list SITE-ONLY in',
              f'  neighbor {peer_ip} prefix-list SITE-ONLY out']
    c += [' exit-address-family',
          ' address-family ipv6',
          f"  network 2001:db8:{spec['ipv6_site']}::/48",
          f'  neighbor {other_v6_internal} activate',
          f'  neighbor {other_v6_internal} next-hop-self',
          f'  neighbor {other_v6_internal} prefix-list V6-SITES in',
          f'  neighbor {other_v6_internal} prefix-list V6-SITES out']
    for _, peer_v6, _ in peer_interfaces:
        c += [f'  neighbor {peer_v6} activate',
              f'  neighbor {peer_v6} prefix-list V6-SITES in',
              f'  neighbor {peer_v6} prefix-list V6-SITES out']
    c += [' exit-address-family']
    return '\n'.join(c)


def render_isp(which: str, plan: dict, cred: dict) -> str:
    asn = plan['wan'][f'isp{which.lower()}_as']
    other_as = plan['wan'][f'isp{"b" if which == "A" else "a"}_as']
    own_peers = [(name, link) for name, link in plan['wan']['links'].items()
                 if link['provider'] == f'ISP-{which}']
    c = base_config(f'ISP-{which}', cred)
    c = [item for item in c if item != ' access-class MGMT-SOURCES in']
    c += ['ip routing', 'ip cef', 'ip prefix-list NO-PRIVATE seq 5 deny 10.0.0.0/8 le 32',
          'ip prefix-list NO-PRIVATE seq 10 permit 0.0.0.0/0 le 32']
    for name, link in own_peers:
        c += [f"interface {link['isp_port']}", f' description TO_{name.upper()}',
              f" ip address {link['isp_ip']} {mask(link['network'])}", ' no shutdown']
    c += [f'interface {"GigabitEthernet0/3"}', ' description INTER_ISP_BGP',
          f' ip address {"192.0.2.1" if which == "A" else "192.0.2.2"} 255.255.255.252',
          ' no shutdown']
    if which == 'A':
        c += ['interface GigabitEthernet0/4', ' description INTERNET_TEST_HOST',
              ' ip address 192.0.2.17 255.255.255.252', ' no shutdown']
    summ = '198.51.100.0' if which == 'A' else '203.0.113.0'
    c += [f'ip route {summ} 255.255.255.0 Null0 250',
          f'router bgp {asn}', ' bgp log-neighbor-changes',
          f' neighbor {"192.0.2.2" if which == "A" else "192.0.2.1"} remote-as {other_as}']
    for name, link in own_peers:
        asn_customer = plan['sites'][name.split('-')[0]]['asn']
        c += [f" neighbor {link['router_ip']} remote-as {asn_customer}"]
    c += [' address-family ipv4', f'  network {summ} mask 255.255.255.0']
    if which == 'A':
        c += ['  network 192.0.2.16 mask 255.255.255.252']
    c += [f'  neighbor {"192.0.2.2" if which == "A" else "192.0.2.1"} activate']
    for _, link in own_peers:
        c += [f"  neighbor {link['router_ip']} activate",
              f"  neighbor {link['router_ip']} prefix-list NO-PRIVATE in"]
    c += [' exit-address-family']
    return '\n'.join(c)


def render_dnsmasq(plan: dict) -> str:
    c = [
        '# HQ DNS + relayed DHCP, install on Linux server 10.10.60.10 (eth0)',
        'port=53', 'bind-dynamic', 'interface=eth0', 'log-dhcp',
        'domain-needed', 'bogus-priv', 'domain=tvi.lab',
        'address=/dhcp.tvi.lab/10.10.60.10',
        'address=/inventory.tvi.lab/10.10.60.20',
    ]
    for site, spec in plan['sites'].items():
        for vlan_id, subnet in spec['vlans'].items():
            vid = int(vlan_id)
            if vid in (60, 99):
                continue
            net = ip.ip_network(subnet)
            start = str(net.network_address + 100)
            stop = str(net.broadcast_address - 10)
            if ip.ip_address(start) >= ip.ip_address(stop):
                raise ValueError(f'No DHCP range for {site} VLAN {vid}')
            tag = f'{site}_v{vid}'
            c += [f'dhcp-range=set:{tag},{start},{stop},{net.netmask},12h',
                  f'dhcp-option=tag:{tag},option:router,{host(subnet, 1)}',
                  f"dhcp-option=tag:{tag},option:dns-server,{plan['services']['internet_test'] if vid == 50 else plan['services']['dns_dhcp']}"]
    return '\n'.join(c)


def matrix(plan: dict) -> list[tuple[str, str, str, str, str]]:
    out = []
    for site in plan['sites']:
        s = site.upper()
        for r in (1, 2):
            out += [(f'{s}-R{r}', G0, f'{s}-SW{r}', 'GigabitEthernet0/0', '802.1Q trunk')]
            link = plan['wan']['links'][f'{site}-r{r}']
            out += [(f'{s}-R{r}', G1, link['provider'], link['isp_port'], 'ISP physical uplink')]
        out += [(f'{s}-R1', G2, f'{s}-R2', G2, 'OSPF + iBGP transit')]
        for p in (1, 2):
            out += [(f'{s}-SW1', f'GigabitEthernet0/{p}', f'{s}-SW2',
                     f'GigabitEthernet0/{p}', 'LACP Port-channel1')]
        out += [(f'{s}-SW1', 'GigabitEthernet0/3', f'{s}-CORP-CLIENT', 'eth0', 'Site corporate client'),
                (f'{s}-SW2', 'GigabitEthernet0/3', f'{s}-GUEST-CLIENT', 'eth0', 'Guest client')]
    out += [('HCMC-SW1', 'GigabitEthernet0/4', 'HQ-DHCP-DNS', 'eth0', 'HQ centralized DHCP/DNS'),
            ('HCMC-SW1', 'GigabitEthernet0/5', 'AUTOMATION', 'eth0', 'Netmiko control host'),
            ('ISP-A', 'GigabitEthernet0/3', 'ISP-B', 'GigabitEthernet0/3', 'Provider interconnect'),
            ('ISP-A', 'GigabitEthernet0/4', 'INTERNET-TEST', 'eth0', 'Simulated web/DNS server')]
    return out



def compile_ios_cli(raw: str) -> str:
    """Turn indentation-grouped config clauses into a safe CLI paste with explicit exits.

    The compiler has a small, documented Cisco IOS mode grammar. Unknown top-level
    instructions remain unaltered. It is still essential to check syntax on the
    particular IOS image before deployment.
    """
    entry0 = ('line ', 'interface ', 'vlan ', 'ip access-list ', 'ipv6 access-list ',
              'route-map ', 'class-map ', 'policy-map ', 'router ', 'ipv6 router ',
              'crypto isakmp policy ', 'crypto ipsec profile ', 'crypto ipsec transform-set ')
    depth = 0
    out = []
    for line in raw.splitlines():
        if not line.strip() or line.strip().startswith('!'):
            continue
        cmd = line.strip()
        target = len(line) - len(line.lstrip(' '))
        if cmd == 'exit-address-family':
            if depth != 2:
                raise ValueError('exit-address-family used outside BGP family mode')
            out.append('exit-address-family')
            depth = 1
            continue
        if target > 2:
            raise ValueError(f'Unexpected indentation on IOS line: {line!r}')
        while depth > target:
            out.append('exit')
            depth -= 1
        if target > depth:
            raise ValueError(f'Unexpected nested IOS statement: {line!r} (depth={depth})')
        out.append(cmd)
        if (target == 0 and cmd.startswith(entry0)) or (target == 1 and cmd.startswith(('class ', 'address-family '))):
            depth += 1
    while depth:
        out.append('exit')
        depth -= 1
    return '\n'.join(out) + '\n'

def generate(plan: dict, outdir: Path, cred: dict):
    config_dir = outdir / 'Configurations'
    inv_devices = []
    for site, spec in plan['sites'].items():
        for r in (1, 2):
            name = f'{site.upper()}-R{r}'
            data = create_router(site, spec, r, plan, cred)
            write(config_dir / site.upper() / f'{name}.cfg', compile_ios_cli(data), private=True)
            inv_devices.append({'hostname': name, 'ip': host(spec['vlans'][99], r + 1),
                                'device_type': 'cisco_ios', 'port': 22, 'role': 'router', 'site': site})
        for sw in (1, 2):
            name = f'{site.upper()}-SW{sw}'
            data = render_switch(site, spec, sw, cred)
            write(config_dir / site.upper() / f'{name}.cfg', compile_ios_cli(data), private=True)
            inv_devices.append({'hostname': name, 'ip': host(spec['vlans'][99], sw + 10),
                                'device_type': 'cisco_ios', 'port': 22, 'role': 'switch', 'site': site})
    for which in ('A', 'B'):
        write(config_dir / 'ISP' / f'ISP-{which}.cfg', compile_ios_cli(render_isp(which, plan, cred)), private=True)
    for device_cfg in config_dir.rglob('*.cfg'):
        lines = ['enable', 'configure terminal', device_cfg.read_text(encoding='utf-8').strip(),
                 'end', 'configure terminal', 'crypto key generate rsa modulus 2048',
                 'end', 'write memory']
        write(device_cfg.with_suffix('.bootstrap.txt'), '\n'.join(lines), private=True)
    write(outdir / 'services' / 'dnsmasq.conf', render_dnsmasq(plan))
    write(ROOT / 'automation' / 'inventory.yaml', yaml.safe_dump({'devices': inv_devices}, sort_keys=False))
    csv_path = ROOT / 'docs' / 'interface_matrix.csv'
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(('Node A', 'Interface A', 'Node B', 'Interface B', 'Description'))
        writer.writerows(matrix(plan))
    with (ROOT / 'docs' / 'ip_schema.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(('Site', 'VLAN', 'IPv4 Network', 'Mask', 'HSRP Gateway',
                         'R1 IP', 'R2 IP', 'IPv6 /64', 'Notes'))
        for site, spec in plan['sites'].items():
            for vid, subnet in spec['vlans'].items():
                writer.writerow([site, vid, subnet, mask(subnet), host(subnet, 1),
                                 host(subnet, 2), host(subnet, 3),
                                 v6prefix(spec, int(vid)) + '/64',
                                 'Static server/management' if int(vid) in (60, 99) else 'Central DHCP via relay'])
    # Deliberately do not generate imported startup-config dumps. Router crypto and SSH
    # RSA keys are device state; paste cfg contents into CLI after `configure terminal`.
    info = [
        'IMPORTANT: This folder contains secrets for a PRIVATE, DISPOSABLE lab only.',
        'Build/configuration files are excluded from Git by .gitignore.',
        'Paste each .bootstrap.txt on the corresponding device CONSOLE in GNS3/EVE-NG.',
        'Generate a 2048-bit RSA key on each device after applying the config:',
        '  conf t', '  crypto key generate rsa modulus 2048', '  end', '  write memory',
        'Generated user:', cred['TVI_USERNAME'],
        'Passwords/PSK are in build/secrets.local.env. Never publish them.',
        'This is a template: verify syntax on your exact IOSv/IOSvL2 images.',
    ]
    write(outdir / 'START_HERE.txt', '\n'.join(info))
    return len(inv_devices), len(plan['wan']['tunnels'])


def main():
    plan = load_plan()
    errs = validate(plan)
    if errs:
        raise SystemExit('Invalid IP plan:\n' + '\n'.join(errs))
    out = ROOT / 'build'
    out.mkdir(exist_ok=True)
    cred = load_or_create_secrets(out)
    devices, tunnels = generate(plan, out, cred)
    print(f'OK: Generated {devices} enterprise configs, 2 provider configs, '
          f'{tunnels} GRE/IPsec tunnel pairs, DHCP/DNS configuration, '
          'inventory, interface matrix, and IP schema.')
    print('IMPORTANT: Only static checks are possible until you load configs into GNS3/EVE-NG.')


if __name__ == '__main__':
    main()
