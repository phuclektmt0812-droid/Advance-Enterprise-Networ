# IOS-XE MPLS L3VPN — provider core and PE examples

**Platform:** IOS-XE/CSR1000v image with CEF, MPLS, LDP, VRF and VPNv4
support. IOSv images commonly omit one or more required features. This is a
separate provider lab, not an extension to the core's simulated ISP routers.

## Provider addressing

| Link | Address A | Address B |
|---|---|---|
| PE-HCMC Gi0/0 ↔ P1 Gi0/0 | 10.41.0.0/31 | 10.41.0.1/31 |
| P1 Gi0/1 ↔ P2 Gi0/0 | 10.41.0.2/31 | 10.41.0.3/31 |
| P2 Gi0/1 ↔ PE-HANOI Gi0/0 | 10.41.0.4/31 | 10.41.0.5/31 |
| P2 Gi0/2 ↔ PE-DANANG Gi0/0 | 10.41.0.6/31 | 10.41.0.7/31 |

Loopbacks: P1 10.41.250.1/32, P2 .2/32, PE-HCMC .11/32,
PE-HANOI .12/32, PE-DANANG .13/32. Provider AS 65141.
Use OSPF 41 for the provider underlay and LDP for label distribution.

## P1 (provider P router)

```text
hostname P1
ip cef
mpls label protocol ldp
mpls ldp router-id Loopback0 force
interface Loopback0
 ip address 10.41.250.1 255.255.255.255
interface GigabitEthernet0/0
 description TO_PE_HCMC
 ip address 10.41.0.1 255.255.255.254
 mpls ip
 no shutdown
interface GigabitEthernet0/1
 description TO_P2
 ip address 10.41.0.2 255.255.255.254
 mpls ip
 no shutdown
router ospf 41
 router-id 10.41.250.1
 network 10.41.0.0 0.0.255.255 area 0
 network 10.41.250.1 0.0.0.0 area 0
```

## P2 (provider P router)

Use Loopback0 10.41.250.2/32, Gi0/0 10.41.0.3/31 toward P1,
Gi0/1 10.41.0.4/31 toward PE-HANOI and Gi0/2 10.41.0.6/31
toward PE-DANANG. Enable `mpls ip` on all three links. Configure OSPF 41
with router-id 10.41.250.2 and advertise the connected links and loopback.

## PE template (repeat on all three PEs)

Replace the PE-specific values below:

| PE | Loopback | Provider-facing IP | Customer VRF RD |
|---|---|---|---|
| PE-HCMC | 10.41.250.11/32 | 10.41.0.0/31 | 65141:11 |
| PE-HANOI | 10.41.250.12/32 | 10.41.0.5/31 | 65141:12 |
| PE-DANANG | 10.41.250.13/32 | 10.41.0.7/31 | 65141:13 |

Each PE must have provider-facing interface addressing, OSPF 41, LDP router-id
Loopback0 and MPLS enabled on the provider-facing interface. Use a unique RD
per PE and the common RT 65141:100.

```text
ip cef
mpls label protocol ldp
mpls ldp router-id Loopback0 force
ip vrf TVI_ENTERPRISE
 rd 65141:11
 route-target import 65141:100
 route-target export 65141:100
interface Loopback0
 ip address 10.41.250.11 255.255.255.255
interface GigabitEthernet0/0
 description PROVIDER_CORE
 ip address 10.41.0.0 255.255.255.254
 mpls ip
 no shutdown
interface GigabitEthernet0/1
 description CUSTOMER_CE_HANDOFF
 ip vrf forwarding TVI_ENTERPRISE
 ip address 10.43.0.1 255.255.255.252
 no shutdown
router ospf 41
 router-id 10.41.250.11
 network 10.41.0.0 0.0.255.255 area 0
 network 10.41.250.11 0.0.0.0 area 0
router bgp 65141
 bgp log-neighbor-changes
 neighbor 10.41.250.12 remote-as 65141
 neighbor 10.41.250.12 update-source Loopback0
 neighbor 10.41.250.13 remote-as 65141
 neighbor 10.41.250.13 update-source Loopback0
 address-family vpnv4
  neighbor 10.41.250.12 activate
  neighbor 10.41.250.12 send-community extended
  neighbor 10.41.250.13 activate
  neighbor 10.41.250.13 send-community extended
 exit-address-family
 address-family ipv4 vrf TVI_ENTERPRISE
  redistribute connected
 exit-address-family
```

The PE example above is PE-HCMC. For PE-HANOI/PE-DANANG, change the PE
loopback, provider link, RD, CE handoff and peer specifics consistently.
For a production-like lab, use CE-PE eBGP or a controlled static route on
each customer handoff; do not redistribute the entire provider global table
into the customer VRF.

## Customer handoff address plan

Reserve three non-overlapping /30s from the advanced services block:
HCMC 10.43.0.0/30, Hanoi 10.43.0.4/30, Da Nang 10.43.0.8/30.
PE uses the first address and CE uses the second. The sample PE interface
must therefore be changed per site. These are dedicated MPLS-lab links and
must not reuse the core lab's router-to-router transit.

## Verification

```text
show ip ospf neighbor
show mpls ldp neighbor
show mpls forwarding-table
show ip bgp vpnv4 all summary
show ip route vrf TVI_ENTERPRISE
show ip cef vrf TVI_ENTERPRISE
```

Acceptance requires VPNv4 peers Established, correct RT import/export,
customer routes in the VRF at all three PEs and end-to-end CE traffic. A
configuration snippet alone is not proof of an operational L3VPN.
