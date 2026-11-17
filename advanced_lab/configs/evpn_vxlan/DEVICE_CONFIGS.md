# Arista EOS EVPN-VXLAN — runnable two-leaf starter

**Platform:** Arista vEOS-lab/EOS with BGP EVPN and VXLAN support. These are
separate-device configuration examples for a 2-spine/2-leaf minimum lab.
They are not IOSv configs. Confirm interface naming and EOS syntax against
the exact image before pasting.

## Cable and addressing map

| Link | Side A | Side B |
|---|---|---|
| SPINE1-Ethernet1 ↔ LEAF1-Ethernet1 | 10.40.0.0/31 | 10.40.0.1/31 |
| SPINE2-Ethernet1 ↔ LEAF1-Ethernet2 | 10.40.0.2/31 | 10.40.0.3/31 |
| SPINE1-Ethernet2 ↔ LEAF2-Ethernet1 | 10.40.0.4/31 | 10.40.0.5/31 |
| SPINE2-Ethernet2 ↔ LEAF2-Ethernet2 | 10.40.0.6/31 | 10.40.0.7/31 |

Loopbacks: SPINE1 10.40.250.1/32, SPINE2 .2/32, LEAF1 .11/32,
LEAF2 .12/32. AS 65140. Underlay OSPF process 100, area 0.
VLAN/VNI: 110/10110, 120/10120, 150/10150.

## SPINE1

```text
hostname SPINE1
ip routing
interface Loopback0
   ip address 10.40.250.1/32
interface Ethernet1
   no switchport
   ip address 10.40.0.0/31
   ip ospf area 0.0.0.0
   no shutdown
interface Ethernet2
   no switchport
   ip address 10.40.0.4/31
   ip ospf area 0.0.0.0
   no shutdown
router ospf 100
   router-id 10.40.250.1
   passive-interface Loopback0
router bgp 65140
   router-id 10.40.250.1
   neighbor LEAVES peer group
   neighbor LEAVES remote-as 65140
   neighbor LEAVES update-source Loopback0
   neighbor LEAVES send-community extended
   neighbor 10.40.250.11 peer group LEAVES
   neighbor 10.40.250.12 peer group LEAVES
   address-family evpn
      neighbor LEAVES activate
      neighbor LEAVES route-reflector-client
```

## SPINE2

Use the same pattern with:
- Loopback0: 10.40.250.2/32
- Ethernet1: 10.40.0.2/31
- Ethernet2: 10.40.0.6/31
- OSPF/BGP router-id: 10.40.250.2
- EVPN neighbors: 10.40.250.11 and 10.40.250.12

## LEAF1

```text
hostname LEAF1
ip routing
vlan 110
   name CORP_APP
vlan 120
   name CORP_DB
vlan 150
   name GUEST
interface Loopback0
   ip address 10.40.250.11/32
interface Ethernet1
   no switchport
   ip address 10.40.0.1/31
   ip ospf area 0.0.0.0
   no shutdown
interface Ethernet2
   no switchport
   ip address 10.40.0.3/31
   ip ospf area 0.0.0.0
   no shutdown
interface Ethernet3
   switchport access vlan 110
   spanning-tree portfast
   no shutdown
interface Ethernet4
   switchport access vlan 110
   spanning-tree portfast
   no shutdown
interface Vxlan1
   vxlan source-interface Loopback0
   vxlan udp-port 4789
   vxlan vlan 110 vni 10110
   vxlan vlan 120 vni 10120
   vxlan vlan 150 vni 10150
router ospf 100
   router-id 10.40.250.11
   passive-interface Loopback0
router bgp 65140
   router-id 10.40.250.11
   neighbor SPINES peer group
   neighbor SPINES remote-as 65140
   neighbor SPINES update-source Loopback0
   neighbor SPINES send-community extended
   neighbor 10.40.250.1 peer group SPINES
   neighbor 10.40.250.2 peer group SPINES
   vlan 110
      rd 10.40.250.11:10110
      route-target both 10110:10110
      redistribute learned
   vlan 120
      rd 10.40.250.11:10120
      route-target both 10120:10120
      redistribute learned
   vlan 150
      rd 10.40.250.11:10150
      route-target both 10150:10150
      redistribute learned
   address-family evpn
      neighbor SPINES activate
```

## LEAF2

Copy LEAF1 and change:
- hostname to LEAF2
- Loopback0 to 10.40.250.12/32
- Ethernet1 to 10.40.0.5/31; Ethernet2 to 10.40.0.7/31
- Leaf BGP router-id and each VLAN RD to use 10.40.250.12
- Attach the second test host to Ethernet3 in VLAN 110

## Verification

Run on all nodes:
```text
show ip ospf neighbor
show ip route 10.40.250.11
show ip route 10.40.250.12
show bgp evpn summary
show bgp evpn route-type mac-ip
show vxlan vtep
show interfaces Vxlan1
```

Then ping between two hosts attached to VLAN 110 on different leaves.
VLAN 120 and 150 are separate L2 VNIs; inter-VNI routing is intentionally
not enabled in this starter. Do not claim inter-VNI routing until an anycast
gateway/IRB design and its security policy are added and tested.

## Extend to LEAF3/LEAF4

Use remaining manifest links .8/31 through .14/31 and loopbacks
10.40.250.13/32 and .14/32. Add those loopbacks as EVPN peers on both spines.
The 2-leaf stage is the first acceptance gate; do not start all nodes on the
8 GB host simultaneously.
