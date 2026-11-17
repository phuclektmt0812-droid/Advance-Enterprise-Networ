# MPLS L3VPN customer-edge handoff

The PE configs use a separate /30 handoff from each site CE. These are not
the core lab's WAN /30s and do not replace the existing GRE/IPsec overlay.

| Site | PE address | CE address | CE AS | Customer summary |
|---|---|---|---|---|
| HCMC | 10.43.0.1/30 | 10.43.0.2/30 | 65010 | 10.10.0.0/16 |
| Hanoi | 10.43.0.5/30 | 10.43.0.6/30 | 65020 | 10.20.0.0/16 |
| Da Nang | 10.43.0.9/30 | 10.43.0.10/30 | 65030 | 10.30.0.0/16 |

## CE interface and BGP template

Apply the matching site values to the CE device. The physical port is an
example; use the actual free interface from the selected router.

```text
interface GigabitEthernet0/3
 description TO_MPLS_PROVIDER_PE
 ip address 10.43.0.2 255.255.255.252
 no shutdown
!
ip route 10.10.0.0 255.255.0.0 Null0 250
router bgp 65010
 bgp log-neighbor-changes
 neighbor 10.43.0.1 remote-as 65141
 address-family ipv4
  network 10.10.0.0 mask 255.255.0.0
  neighbor 10.43.0.1 activate
 exit-address-family
```

For Hanoi use CE 10.43.0.6, PE 10.43.0.5, AS 65020 and summary
10.20.0.0/16. For Da Nang use CE 10.43.0.10, PE 10.43.0.9,
AS 65030 and summary 10.30.0.0/16.

The Null0 summary is a lab advertisement anchor only. In a connected
implementation, ensure more-specific site routes exist and are preferred;
do not blackhole production traffic. Do not add this summary route blindly
to the existing core router if it changes its current routing behavior.

## Verify

On each CE:
```text
show ip bgp summary
show ip route bgp
show ip route 10.10.0.0
```

On each PE:
```text
show ip bgp vpnv4 all summary
show ip route vrf TVI_ENTERPRISE
show ip bgp vpnv4 vrf TVI_ENTERPRISE
```

The PE-CE BGP session must be Established and each PE must learn the
appropriate customer summary. Cross-site reachability must be tested between
CEs only after the VPNv4 control plane and route-target import/export are
verified.
