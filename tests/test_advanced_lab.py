from copy import deepcopy
from pathlib import Path
import yaml

from tools.validate_advanced_lab import validate

ROOT = Path(__file__).resolve().parents[1]


def load_manifest():
    return yaml.safe_load((ROOT / "advanced_lab" / "topology.yaml").read_text(encoding="utf-8"))


def test_advanced_manifest_is_valid_and_separate_from_core():
    assert validate(load_manifest()) == []


def test_advanced_address_block_cannot_overlap_core():
    plan = deepcopy(load_manifest())
    plan["addressing"]["blocks"]["evpn_underlay"] = "10.10.0.0/16"
    assert any("overlaps core block" in error for error in validate(plan))


def test_advanced_blocks_cannot_overlap_each_other():
    plan = deepcopy(load_manifest())
    plan["addressing"]["blocks"]["mpls_provider"] = plan["addressing"]["blocks"]["evpn_underlay"]
    assert any("overlap" in error for error in validate(plan))


def test_duplicate_vni_is_rejected():
    plan = deepcopy(load_manifest())
    plan["evpn"]["vnis"][1]["vni"] = plan["evpn"]["vnis"][0]["vni"]
    assert any("duplicate EVPN VNI" in error for error in validate(plan))


def test_duplicate_mpls_rd_is_rejected():
    plan = deepcopy(load_manifest())
    duplicate = deepcopy(plan["mpls"]["customer_vrfs"][0])
    duplicate["name"] = "TVI_DUPLICATE"
    plan["mpls"]["customer_vrfs"].append(duplicate)
    assert any("duplicate MPLS route distinguisher" in error for error in validate(plan))
