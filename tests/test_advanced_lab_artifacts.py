from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_evpn_reference_has_underlay_and_overlay_configuration():
    spine = read("advanced_lab/configs/evpn_vxlan/SPINE1.cfg")
    leaf = read("advanced_lab/configs/evpn_vxlan/LEAF1.cfg")
    guide = read("advanced_lab/configs/evpn_vxlan/DEVICE_CONFIGS.md")
    for token in ("router ospf 100", "address-family evpn", "route-reflector-client"):
        assert token in spine
    for token in ("router ospf 100", "address-family evpn", "interface Vxlan1",
                  "vxlan vlan 110 vni 10110", "no shutdown"):
        assert token in leaf
    assert "show bgp evpn summary" in guide


def test_mpls_reference_has_ldp_vpnv4_and_customer_vrf():
    p_router = read("advanced_lab/configs/mpls_l3vpn/P1.cfg")
    pe = read("advanced_lab/configs/mpls_l3vpn/PE-HCMC.cfg")
    guide = read("advanced_lab/configs/mpls_l3vpn/DEVICE_CONFIGS.md")
    for token in ("mpls ip", "mpls ldp", "router ospf 41"):
        assert token in p_router
    for token in ("address-family vpnv4", "ip vrf TVI_ENTERPRISE",
                  "route-target import", "address-family ipv4 vrf TVI_ENTERPRISE"):
        assert token in pe
    assert "show mpls ldp neighbor" in guide


def test_core_qos_is_documented_and_attached_by_generator():
    content = read("docs/config_templates/IOS_QOS_VOICE_VIDEO.txt")
    assert "TVI-WAN-OUT" in content
    assert "strict-priority" in content
    generator = read("tools/build_lab.py")
    assert "service-policy output TVI-WAN-OUT" in generator


def test_controller_and_security_stages_have_concrete_artifacts():
    paths = [
        "advanced_lab/configs/evpn_vxlan/SPINE1.cfg",
        "advanced_lab/configs/evpn_vxlan/SPINE2.cfg",
        "advanced_lab/configs/evpn_vxlan/LEAF1.cfg",
        "advanced_lab/configs/evpn_vxlan/LEAF2.cfg",
        "advanced_lab/configs/mpls_l3vpn/P1.cfg",
        "advanced_lab/configs/mpls_l3vpn/P2.cfg",
        "advanced_lab/configs/mpls_l3vpn/PE-HCMC.cfg",
        "advanced_lab/configs/mpls_l3vpn/PE-HANOI.cfg",
        "advanced_lab/configs/mpls_l3vpn/PE-DANANG.cfg",
        "advanced_lab/configs/mpls_l3vpn/CE_HANDOFF.md",
        "advanced_lab/configs/mpls_l3vpn/CE-HCMC.cfg",
        "advanced_lab/configs/mpls_l3vpn/CE-HANOI.cfg",
        "advanced_lab/configs/mpls_l3vpn/CE-DANANG.cfg",
        "advanced_lab/configs/security/OPNSENSE_LAB_GUIDE.md",
        "advanced_lab/configs/sdwan/IMPLEMENTATION_RUNBOOK.md",
        "advanced_lab/configs/security/NGFW_POLICY_BLUEPRINT.md",
        "advanced_lab/configs/ztna/OPENZITI_REFERENCE.md",
        "advanced_lab/configs/wireless/CISCO_9800_REFERENCE.txt",
        "advanced_lab/configs/wireless/C9800_CLI_TEMPLATE.txt",
        "advanced_lab/deploy/ztna/prepare-openziti.ps1",
        "advanced_lab/deploy/ztna/README.md",
        "advanced_lab/configs/sdwan/DUAL_WAN_ROUTING_FALLBACK.md",
    ]
    for path in paths:
        assert (ROOT / path).is_file()
        assert len(read(path)) > 400


def test_mpls_has_site_specific_ce_configs_and_consistent_handoffs():
    cases = [
        ("HCMC", "10.43.0.2", "10.43.0.1", "65010", "10.10.250.1"),
        ("HANOI", "10.43.0.6", "10.43.0.5", "65020", "10.20.250.1"),
        ("DANANG", "10.43.0.10", "10.43.0.9", "65030", "10.30.250.1"),
    ]
    for site, ce_ip, pe_ip, asn, loopback in cases:
        content = read(f"advanced_lab/configs/mpls_l3vpn/CE-{site}.cfg")
        assert f"ip address {ce_ip} 255.255.255.252" in content
        assert f"neighbor {pe_ip} remote-as 65141" in content
        assert f"router bgp {asn}" in content
        assert loopback in content


def test_evpn_leafs_have_access_ports_for_each_mapped_vlan():
    for leaf in ("LEAF1", "LEAF2"):
        content = read(f"advanced_lab/configs/evpn_vxlan/{leaf}.cfg")
        for vlan in (110, 120, 150):
            assert f"switchport access vlan {vlan}" in content
            assert f"vxlan vlan {vlan} vni" in content


def test_evpn_vxlan_interfaces_are_enabled_and_tenant_ports_match_vnis():
    for leaf in ("LEAF1", "LEAF2"):
        content = read(f"advanced_lab/configs/evpn_vxlan/{leaf}.cfg")
        assert "interface Vxlan1" in content
        assert "no shutdown" in content.split("interface Vxlan1", 1)[1]
        for port, vlan in (("Ethernet3", 110), ("Ethernet4", 120), ("Ethernet5", 150)):
            section = content.split(f"interface {port}", 1)[1].split("interface ", 1)[0]
            assert f"switchport access vlan {vlan}" in section


def test_mpls_pe_ce_neighbors_are_configured_inside_customer_vrf_af():
    for site, neighbor, asn in (
        ("HCMC", "10.43.0.2", "65010"),
        ("HANOI", "10.43.0.6", "65020"),
        ("DANANG", "10.43.0.10", "65030"),
    ):
        content = read(f"advanced_lab/configs/mpls_l3vpn/PE-{site}.cfg")
        af = content.split("address-family ipv4 vrf TVI_ENTERPRISE", 1)[1]
        assert f"neighbor {neighbor} remote-as {asn}" in af
        assert f"neighbor {neighbor} activate" in af
        assert f"neighbor {neighbor} remote-as" not in content.split("address-family ipv4 vrf", 1)[0]


def test_wireless_template_has_enterprise_authentication_and_guest_mapping():
    content = read("advanced_lab/configs/wireless/C9800_CLI_TEMPLATE.txt")
    for token in ("security dot1x authentication-list TVI-DOT1X",
                  "security wpa wpa2 ciphers aes",
                  "security web-auth",
                  "vlan 110", "vlan 150",
                  "wireless tag policy TVI-SITE-POLICY"):
        assert token in content
