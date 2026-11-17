from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_evpn_reference_has_underlay_and_overlay_configuration():
    content = read("advanced_lab/configs/evpn_vxlan/DEVICE_CONFIGS.md")
    for token in ("router ospf 100", "address-family evpn", "interface Vxlan1",
                  "vxlan vlan 110 vni 10110", "show bgp evpn summary"):
        assert token in content


def test_mpls_reference_has_ldp_vpnv4_and_customer_vrf():
    content = read("advanced_lab/configs/mpls_l3vpn/DEVICE_CONFIGS.md")
    for token in ("mpls ip", "mpls ldp", "address-family vpnv4",
                  "ip vrf TVI_ENTERPRISE", "route-target import"):
        assert token in content


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
        "advanced_lab/configs/security/OPNSENSE_LAB_GUIDE.md",
        "advanced_lab/configs/sdwan/IMPLEMENTATION_RUNBOOK.md",
        "advanced_lab/configs/security/NGFW_POLICY_BLUEPRINT.md",
        "advanced_lab/configs/ztna/OPENZITI_REFERENCE.md",
        "advanced_lab/configs/wireless/CISCO_9800_REFERENCE.txt",
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
