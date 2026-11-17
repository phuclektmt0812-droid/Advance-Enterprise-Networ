# MPLS L3VPN reference configuration

**Reference platform:** Cisco IOS-XE/CSR1000v PE/P routers with MPLS, LDP,
VRF and VPNv4 support. Feature availability differs by image and license.

## Provider roles

- PE-HCMC, PE-HANOI and PE-DANANG attach customer sites.
- P1/P2 provide the provider core.
- Run an IGP in the provider core and LDP on provider-facing links.
- Establish VPNv4 MP-BGP between PE routers.
- Use one shared customer VRF (TVI_ENTERPRISE) across all three PE routers so
  the three sites exchange routes within the same enterprise VPN. The same
  route-target is imported/exported at each PE; use unique RDs per PE in the
  final device configuration if the platform design requires them.

## IOS-XE configuration skeleton — provider core

```text
! Apply only to MPLS-capable provider-facing interfaces.
ip cef
mpls label protocol ldp
mpls ldp router-id Loopback0 force
!
interface GigabitEthernet0/0
 description PROVIDER_CORE_LINK
 ip address 10.41.0.0 255.255.255.254
 mpls ip
 no shutdown
!
router ospf 41
 router-id 10.41.250.1
 network 10.41.0.0 0.0.255.255 area 0
 network 10.41.250.1 0.0.0.0 area 0
!
```

## IOS-XE configuration skeleton — PE

```text
ip vrf TVI_ENTERPRISE
 rd 65141:100
 route-target import 65141:100
 route-target export 65141:100
!
interface GigabitEthernet0/1
 description CUSTOMER_HANDOFF
 ip vrf forwarding TVI_ENTERPRISE
 ip address 10.10.254.1 255.255.255.252
 no shutdown
!
router bgp 65141
 bgp log-neighbor-changes
 neighbor 10.41.250.2 remote-as 65141
 neighbor 10.41.250.2 update-source Loopback0
 !
 address-family vpnv4
  neighbor 10.41.250.2 activate
  neighbor 10.41.250.2 send-community extended
 exit-address-family
 !
 address-family ipv4 vrf TVI_ENTERPRISE
  redistribute connected
 exit-address-family
```

## Mandatory adaptation

- Allocate unique PE/P loopbacks and every /31 link from the manifest.
- Ensure provider IGP carries PE loopbacks; do not redistribute customer routes
  into the provider global table.
- Configure a VPNv4 full mesh or route reflectors.
- The manifest models one shared TVI_ENTERPRISE VRF so all three sites can
  exchange enterprise routes. Use a unique RD per PE while keeping a common RT.
- The sample customer handoff address is illustrative and must be coordinated
  with the core router before use.
- Verify LDP, labels, VPNv4 routes, VRF route tables and traffic isolation.

The snippets are deliberately incomplete templates, not paste-ready configs.
