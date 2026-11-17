# MPLS L3VPN reference configuration

**Reference platform:** Cisco IOS-XE/CSR1000v PE/P routers with MPLS, LDP,
VRF and VPNv4 support. Feature availability differs by image and license.

## Provider roles

- PE-HCMC, PE-HANOI and PE-DANANG attach customer sites.
- P1/P2 provide the provider core.
- Run an IGP in the provider core and LDP on provider-facing links.
- Establish VPNv4 MP-BGP between PE routers.
- Use a separate customer VRF per site only if the assignment requires
  isolation; if the three sites are one enterprise VPN, use one shared VRF
  and a common route-target instead. The manifest currently describes
  separate VRFs as an isolation example, not an approved business policy.

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
ip vrf TVI_HCMC
 rd 65141:10
 route-target import 65141:10
 route-target export 65141:10
!
interface GigabitEthernet0/1
 description CUSTOMER_HANDOFF
 ip vrf forwarding TVI_HCMC
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
 address-family ipv4 vrf TVI_HCMC
  redistribute connected
 exit-address-family
```

## Mandatory adaptation

- Allocate unique PE/P loopbacks and every /31 link from the manifest.
- Ensure provider IGP carries PE loopbacks; do not redistribute customer routes
  into the provider global table.
- Configure a VPNv4 full mesh or route reflectors.
- The manifest's separate VRFs are an example. Confirm whether TVI sites
  should share one enterprise VRF; if so, use one shared RT consistently.
- The sample customer handoff address is illustrative and must be coordinated
  with the core router before use.
- Verify LDP, labels, VPNv4 routes, VRF route tables and traffic isolation.

The snippets are deliberately incomplete templates, not paste-ready configs.
