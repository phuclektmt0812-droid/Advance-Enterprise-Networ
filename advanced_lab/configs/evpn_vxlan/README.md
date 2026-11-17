# EVPN-VXLAN reference configuration

**Reference platform:** Arista EOS / vEOS-lab. This is a syntax-oriented
starting point, not a universal configuration for Cisco or Juniper images.
Confirm command support against the exact licensed EOS release.

## Design

- SPINE1 and SPINE2 are routed underlay nodes and EVPN route reflectors.
- LEAF1-LEAF4 are VTEPs with unique loopbacks from
  `advanced_lab/topology.yaml`.
- MP-BGP EVPN carries MAC/IP reachability.
- VLAN 110/120/150 map to VNIs 10110/10120/10150.
- Use symmetric IRB/anycast gateway only after validating the selected EOS
  release and adding a consistent anycast gateway MAC/IP plan.

## Configuration skeleton — spine

```text
! Replace interface names and addresses from the final cabling sheet.
hostname SPINE1
ip routing
interface Loopback0
   ip address 10.40.250.1/32
!
interface Ethernet1
   no switchport
   ip address 10.40.0.0/31
!
router bgp 65140
   router-id 10.40.250.1
   neighbor EVPN-LEAFS peer group
   neighbor EVPN-LEAFS remote-as 65140
   neighbor EVPN-LEAFS update-source Loopback0
   neighbor EVPN-LEAFS send-community extended
   neighbor 10.40.250.11 peer group EVPN-LEAFS
   neighbor 10.40.250.12 peer group EVPN-LEAFS
   address-family evpn
      neighbor EVPN-LEAFS activate
      neighbor EVPN-LEAFS route-reflector-client
```

## Configuration skeleton — leaf

```text
! Example LEAF1. Underlay routing and peer IPs must match the cabling plan.
hostname LEAF1
ip routing
interface Loopback0
   ip address 10.40.250.11/32
!
interface Vxlan1
   vxlan source-interface Loopback0
   vxlan udp-port 4789
   vxlan vlan 110 vni 10110
   vxlan vlan 120 vni 10120
   vxlan vlan 150 vni 10150
!
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

## Before using

1. Allocate the eight /31 links to actual spine-leaf interfaces; the manifest
   lists the pool but does not assign each link to a named port.
2. Configure and verify the routed underlay (OSPF or eBGP) before BGP EVPN.
3. Confirm route-reflector policy and EVPN address-family support.
4. Add VLANs, access ports, anycast gateway and IRB only after the base VTEPs
   are established.
5. Capture the EVPN acceptance evidence in `docs/acceptance_tests.md`.

Do not paste these skeletons blindly: they are not complete device configs.


## Exact minimum-stage cabling and host addressing

Use four vEOS nodes and two lightweight Linux/VPCS hosts. Cable:

| Link | Device A | Port A | Device B | Port B | IPv4 subnet |
|---|---|---|---|---|---|
| Underlay | SPINE1 | Ethernet1 | LEAF1 | Ethernet1 | 10.40.0.0/31 |
| Underlay | SPINE2 | Ethernet1 | LEAF1 | Ethernet2 | 10.40.0.2/31 |
| Underlay | SPINE1 | Ethernet2 | LEAF2 | Ethernet1 | 10.40.0.4/31 |
| Underlay | SPINE2 | Ethernet2 | LEAF2 | Ethernet2 | 10.40.0.6/31 |
| Tenant host | LEAF1 | Ethernet3 | HOST-A | eth0 | VLAN 110 |
| Tenant host | LEAF2 | Ethernet3 | HOST-B | eth0 | VLAN 110 |

Host A: `10.40.130.11/24`; Host B: `10.40.130.12/24`.
No default gateway is needed for this same-subnet L2 extension test. Both
host-facing ports are access VLAN 110 and VLAN 110 maps to VNI 10110.
The additional Ethernet4/Ethernet5 ports on each leaf are reserved for VLAN
120 and VLAN 150 test hosts.

## Apply and verify

1. Load the matching SPINE1, SPINE2, LEAF1 and LEAF2 files.
2. Verify OSPF underlay and loopback reachability.
3. Verify MP-BGP EVPN sessions on both spines and leaves.
4. Confirm VLAN 110 / VNI 10110 is active and the remote host MAC is learned.
5. Ping Host B from Host A. Then disconnect one spine-leaf link and repeat.

Typical EOS checks:
```text
show ip ospf neighbor
show ip route 10.40.250.12
show bgp evpn summary
show vxlan vtep
show vxlan address-table
show mac address-table dynamic
```

The config set is a two-leaf L2 EVPN demonstration. It intentionally does
not claim symmetric IRB, anycast gateway, multi-tenant inter-VNI routing,
or four-leaf scale-out; those require an additional L3 VNI/gateway design.
