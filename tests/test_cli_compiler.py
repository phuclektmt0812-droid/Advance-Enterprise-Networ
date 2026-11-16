from pathlib import Path
import xml.etree.ElementTree as ET
import pytest
from tools.build_lab import compile_ios_cli, render_switch, create_router
from tools.validate_plan import load_plan

CRED = {'TVI_USERNAME': 'mockadmin', 'TVI_PASSWORD': 'FAKEPASSWORD', 'TVI_IPSEC_PSK': 'MOCK-PSK'}


def test_cli_compiler_adds_context_exits_between_vlan_statements():
    p=load_plan()
    sw=compile_ios_cli(render_switch('hcmc',p['sites']['hcmc'],1,CRED))
    assert 'vlan 10\nname EXEC_FINANCE\nexit\nvlan 20\nname ENGINEERING' in sw
    assert 'vlan 999\nname BLACKHOLE\nexit\nspanning-tree vlan' in sw
    assert '{' not in sw


def test_cli_compiler_handles_nested_qos_and_bgp():
    p=load_plan()
    cfg=compile_ios_cli(create_router('hcmc',p['sites']['hcmc'],1,p,CRED))
    assert 'class class-default\nfair-queue\nexit\nexit\npolicy-map TVI-MARK-VOICE' in cfg
    assert 'exit-address-family\naddress-family ipv6' in cfg
    assert 'standby 99 preempt' in cfg
    assert 'tunnel protection ipsec profile TVI-GRE-IPSEC' in cfg
    assert '{' not in cfg


def test_compiler_rejects_incorrect_indentation():
    with pytest.raises(ValueError):
        compile_ios_cli(' hostname R1')


def test_drawio_has_network_device_nodes():
    path=Path(__file__).resolve().parents[1]/'docs'/'TVI_Logical_Topology.drawio'
    root=ET.parse(path).getroot()
    text=' '.join(x.attrib.get('value','') for x in root.iter('mxCell'))
    assert all(n in text for n in ('HCMC-R1','HANOI-R1','DANANG-R1','ISP-A','ISP-B'))
