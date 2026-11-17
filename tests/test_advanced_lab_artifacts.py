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
    assert "'service-policy output TVI-WAN-OUT'" in generator


def test_controller_and_security_stages_have_concrete_artifacts():
    paths = [
        "advanced_lab/configs/sdwan/IMPLEMENTATION_RUNBOOK.md",
        "advanced_lab/configs/security/NGFW_POLICY_BLUEPRINT.md",
        "advanced_lab/configs/ztna/OPENZITI_REFERENCE.md",
        "advanced_lab/configs/wireless/CISCO_9800_REFERENCE.txt",
    ]
    for path in paths:
        assert (ROOT / path).is_file()
        assert len(read(path)) > 500
