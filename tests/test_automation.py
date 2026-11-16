from pathlib import Path
from automation.auto_provision import (
    compute_commands, parse_vlan_brief, run, load_vlan_payload, load_inventory,
)


class FakeConnection:
    def __init__(self, *, missing_aaa=True):
        self.running = ('hostname TEST-SW\n'
                        'ntp server 10.10.60.10\n'
                        'logging 10.10.60.10\n'
                        'banner motd ^CAuthorized TVI training lab only.^C\n')
        if not missing_aaa:
            self.running += ('aaa new-model\n'
                             'aaa authentication login default local\n'
                             'aaa authorization exec default local\n')
        self.vlans = {10: 'EXEC_FINANCE', 20: 'ENGINEERING', 30: 'LOGISTICS', 99: 'MANAGEMENT'}
        self.writes = 0
        self.sent = []
        self.disconnects = 0

    def enable(self):
        pass

    def send_command(self, command, read_timeout=30):
        if command == 'show running-config':
            return self.running
        if command == 'show ip interface brief':
            return 'Interface    IP-Address    OK? Method Status Protocol\nVlan99 10.10.99.11 YES manual up up'
        if command == 'show vlan brief':
            return 'VLAN Name             Status    Ports\n' + '\n'.join(
                f'{vid:<4} {name:<20} active' for vid, name in sorted(self.vlans.items()))
        if command == 'write memory':
            self.writes += 1
            return '[OK]'
        raise AssertionError(f'Unexpected command: {command}')

    def send_config_set(self, commands, read_timeout=90):
        self.sent.append(commands)
        self.running += '\n' + '\n'.join(commands) + '\n'
        for i, command in enumerate(commands):
            if command.startswith('vlan ') and i + 1 < len(commands):
                self.vlans[int(command.split()[1])] = commands[i + 1].split()[1]
        return 'Successfully configured'

    def disconnect(self):
        self.disconnects += 1


def test_vlan_parser():
    value = parse_vlan_brief('10 EXEC_FINANCE active Gi0/3\n140 DEMO_AUDIT active\n1002 fddi-default act/unsup')
    assert value[10] == 'EXEC_FINANCE'
    assert value[140] == 'DEMO_AUDIT'


def test_idempotency_and_backup_files(tmp_path):
    fake = FakeConnection()
    dev = [{'hostname': 'HCMC-SW1', 'ip': '10.10.99.11', 'port': 22,
            'device_type': 'cisco_ios', 'role': 'switch', 'site': 'hcmc'}]
    connector = lambda **_: fake
    first = run(dev, load_vlan_payload(), 'operator', 'dummy_test_secret', connector, tmp_path)
    assert first[0].success is True and first[0].changed is True
    assert fake.vlans[140] == 'DEMO_AUDIT'
    assert fake.writes == 1
    second = run(dev, load_vlan_payload(), 'operator', 'dummy_test_secret', connector, tmp_path)
    assert second[0].success is True and second[0].changed is False
    assert fake.writes == 1
    assert len(list((tmp_path / 'backups').glob('*.cfg'))) == 4  # before & after for both runs
    assert len(list((tmp_path / 'backups').glob('*interfaces.txt'))) == 4
    assert 'success' in (tmp_path / 'logs' / 'automation.log').read_text()
    assert fake.disconnects == 2


def test_error_handling_does_not_abort_next_device(tmp_path):
    working = FakeConnection()
    def connect(**kwargs):
        if kwargs['host'] == '10.10.99.11':
            raise TimeoutError('device unreachable')
        return working
    devs = [
        {'hostname': 'BAD-SW', 'ip': '10.10.99.11', 'port': 22, 'device_type': 'cisco_ios', 'role': 'switch'},
        {'hostname': 'GOOD-SW', 'ip': '10.10.99.12', 'port': 22, 'device_type': 'cisco_ios', 'role': 'switch'},
    ]
    res = run(devs, load_vlan_payload(), 'operator', 'dummy_test_secret', connect, tmp_path)
    assert len(res) == 2
    assert res[0].success is False and res[1].success is True
    assert 'BAD-SW failed' in (tmp_path / 'logs' / 'automation.log').read_text()


def test_router_does_not_receive_vlan_commands():
    expected = compute_commands('hostname R1\n', '', 'router', load_vlan_payload())
    assert not any(x.startswith('vlan ') for x in expected)
    assert 'aaa new-model' in expected


def test_inventory_has_all_enterprise_nodes():
    devices = load_inventory()
    assert len(devices) == 12
    assert sum(d['role'] == 'router' for d in devices) == 6
    assert sum(d['role'] == 'switch' for d in devices) == 6
