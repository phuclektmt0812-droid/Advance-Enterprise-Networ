# Arista EOS EVPN-VXLAN — two-leaf runnable stage

The authoritative per-device configs are the four files in this folder:
`SPINE1.cfg`, `SPINE2.cfg`, `LEAF1.cfg`, and `LEAF2.cfg`.
Do not copy a second, hand-maintained configuration from this document.

## Minimum topology

| Link | Endpoint A | Endpoint B | IPv4 |
|---|---|---|---|
| 1 | SPINE1 Ethernet1 | LEAF1 Ethernet1 | 10.40.0.0/31 |
| 2 | SPINE2 Ethernet1 | LEAF1 Ethernet2 | 10.40.0.2/31 |
| 3 | SPINE1 Ethernet2 | LEAF2 Ethernet1 | 10.40.0.4/31 |
| 4 | SPINE2 Ethernet2 | LEAF2 Ethernet2 | 10.40.0.6/31 |

Loopbacks: SPINE1 .1, SPINE2 .2, LEAF1 .11, LEAF2 .12 in
10.40.250.0/24. All nodes use AS 65140 and OSPF process 100 area 0.
The spines are EVPN route reflectors.

## Tenant access ports

| VLAN | VNI | Subnet | LEAF1 | LEAF2 |
|---|---|---|---|---|
| 110 CORP_APP | 10110 | 10.40.130.0/24 | Ethernet3 | Ethernet3 |
| 120 CORP_DB | 10120 | 10.40.140.0/24 | Ethernet4 | Ethernet4 |
| 150 GUEST | 10150 | 10.40.150.0/24 | Ethernet5 | Ethernet5 |

For the first L2 test, configure Host A as 10.40.130.11/24 on LEAF1
Ethernet3 and Host B as 10.40.130.12/24 on LEAF2 Ethernet3. No gateway is
needed for same-subnet bridging. VLAN 120 and 150 are separate VNIs and are
not routed to one another in this stage.

## Bring-up sequence

1. Import the four EOS nodes and cable the four underlay links.
2. Apply each matching .cfg file. Confirm all physical interfaces are up.
3. Confirm OSPF neighbors and reachability between all four loopbacks.
4. Confirm each leaf has two Established EVPN sessions to the spines.
5. Confirm Vxlan1 is up and VLAN-to-VNI mappings are present.
6. Connect Host A and Host B; confirm the remote MAC is learned and ping
   works in both directions.
7. Shut one spine-facing link in a controlled test; verify traffic continues
   through the other spine. Restore the link afterward.

## Useful EOS checks

```text
show ip ospf neighbor
show ip route 10.40.250.11
show ip route 10.40.250.12
show bgp evpn summary
show bgp evpn route-type mac-ip
show vxlan vtep
show vxlan address-table
show interfaces Vxlan1
show mac address-table dynamic
```

This is a two-leaf L2 EVPN stage. It does not claim symmetric IRB, anycast
gateway, inter-VNI routing or four-leaf deployment. Those require a separate
L3 VNI/gateway and policy design.

## Platform note

Use an EOS release/image that supports BGP EVPN and VXLAN. Interface naming,
feature support and exact syntax must be confirmed on that release. Static
repository tests do not parse EOS CLI or prove data-plane forwarding.
