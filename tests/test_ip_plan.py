from copy import deepcopy
import ipaddress
import pytest
from tools.validate_plan import load_plan, validate
from tools.build_lab import render_dnsmasq, render_switch, create_router

CREDENTIALS = {'TVI_USERNAME': 'dummy', 'TVI_PASSWORD': 'REPLACE_AT_BUILD', 'TVI_IPSEC_PSK': 'REPLACE_AT_BUILD'}


def test_no_subnet_overlaps_and_correct_site_blocks():
    assert validate(load_plan()) == []


def test_overlap_is_detected():
    plan = deepcopy(load_plan())
    plan['sites']['hanoi']['vlans'][30] = plan['sites']['hanoi']['vlans'][10]
    assert any('overlaps' in err for err in validate(plan))


def test_vlan_must_fit_site_prefix():
    plan = deepcopy(load_plan())
    plan['sites']['hanoi']['vlans'][30] = '10.77.22.0/24'
    assert any('outside' in err for err in validate(plan))


@pytest.mark.parametrize('site', ['hcmc', 'hanoi', 'danang'])
def test_router_has_ospf_bgp_hsrp_ipv6_nat_qos(site):
    plan = load_plan()
    config = create_router(site, plan['sites'][site], 1, plan, CREDENTIALS)
    for expected in ('router ospf 10', 'ipv6 router ospf 10', 'router bgp ',
                     'standby 99 ip', 'standby 99 preempt', 'ip nat inside source route-map',
                     'ip access-list extended ACL-GUEST-IN', 'ip access-list extended ACL-IOT-IN',
                     'ipv6 traffic-filter V6-GUEST-IN in', 'ipv6 traffic-filter V6-IOT-IN in',
                     'service-policy output TVI-WAN-OUT', 'ip helper-address 10.10.60.10',
                     'ipv6 address 2001:db8:', 'tunnel protection ipsec profile'):
        assert expected in config


@pytest.mark.parametrize('site', ['hcmc', 'hanoi', 'danang'])
def test_switch_has_lacp_stp_snooping_dai(site):
    plan = load_plan()
    conf = render_switch(site, plan['sites'][site], 1, CREDENTIALS)
    for expected in ('channel-group 1 mode active', 'spanning-tree mode rapid-pvst',
                     'ip dhcp snooping', 'ip arp inspection vlan',
                     'spanning-tree bpduguard enable', 'interface Vlan99', 'switchport trunk native vlan 999',
                     'switchport port-security', 'switchport port-security maximum 2',
                     'switchport port-security violation restrict',
                     'switchport port-security mac-address sticky'):
        assert expected in conf
    # Host-facing ports remain untrusted for DHCP Snooping and DAI.
    host_port = conf.split('interface GigabitEthernet0/3', 1)[1].split('interface GigabitEthernet0/4', 1)[0]
    assert 'ip dhcp snooping trust' not in host_port
    assert 'ip arp inspection trust' not in host_port


def test_dnsmasq_has_branch_dhcp_and_correct_gateways():
    cfg = render_dnsmasq(load_plan())
    assert 'dhcp-range=set:hanoi_v20,10.20.16.100,10.20.23.245,255.255.248.0,12h' in cfg
    assert 'dhcp-option=tag:danang_v70,option:router,10.30.128.1' in cfg
    assert 'dhcp-option=tag:hanoi_v50,option:dns-server,192.0.2.18' in cfg


def test_vlan_address_sizing():
    p = load_plan()
    assert ipaddress.ip_network(p['sites']['hanoi']['vlans'][20]).num_addresses - 2 >= 1500
    assert ipaddress.ip_network(p['sites']['danang']['vlans'][70]).num_addresses - 2 >= 10000


def test_site_ips_not_advertised_to_provider():
    p = load_plan()
    for site, spec in p['sites'].items():
        for r in (1, 2):
            c = create_router(site, spec, r, p, CREDENTIALS)
            assert 'ip prefix-list ISP-OUT seq 5 deny 0.0.0.0/0 le 32' in c
            assert 'neighbor ' + p['wan']['links'][f'{site}-r{r}']['isp_ip'] + ' prefix-list ISP-OUT out' in c


def test_crypto_psk_injected_not_hardcoded_source():
    p = load_plan()
    r = create_router('hanoi', p['sites']['hanoi'], 1, p, CREDENTIALS)
    assert 'crypto isakmp key REPLACE_AT_BUILD address 198.51.100.2' in r
