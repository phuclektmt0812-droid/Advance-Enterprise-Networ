# IOS-XE MPLS L3VPN — authoritative per-device configurations

The authoritative configurations are the individual device files:
`P1.cfg`, `P2.cfg`, `PE-HCMC.cfg`, `PE-HANOI.cfg`,
`PE-DANANG.cfg`, and the three `CE-*.cfg` files. This document is the
addressing and procedure index; do not paste the former generic PE template.

## Provider topology and addressing

| Link | Endpoint A | Address A | Endpoint B | Address B |
|---|---|---|---|---|
| 1 | PE-HCMC Gi0/0 | 10.41.0.0/31 | P1 Gi0/0 | 10.41.0.1/31 |
| 2 | P1 Gi0/1 | 10.41.0.2/31 | P2 Gi0/0 | 10.41.0.3/31 |
| 3 | P2 Gi0/1 | 10.41.0.4/31 | PE-HANOI Gi0/0 | 10.41.0.5/31 |
| 4 | P2 Gi0/2 | 10.41.0.6/31 | PE-DANANG Gi0/0 | 10.41.0.7/31 |

Provider loopbacks: P1 10.41.250.1/32, P2 .2/32, PE-HCMC .11/32,
PE-HANOI .12/32, PE-DANANG .13/32. Provider OSPF process 41, AS 65141,
LDP on every provider-facing link.

## Customer handoffs

| Site | PE interface | PE address | CE interface | CE address | CE AS |
|---|---|---|---|---|---|
| HCMC | Gi0/1 | 10.43.0.1/30 | Gi0/0 | 10.43.0.2/30 | 65010 |
| Hanoi | Gi0/1 | 10.43.0.5/30 | Gi0/0 | 10.43.0.6/30 | 65020 |
| Da Nang | Gi0/1 | 10.43.0.9/30 | Gi0/0 | 10.43.0.10/30 | 65030 |

All three PE routers use VRF TVI_ENTERPRISE and common RT 65141:100; each
has a unique RD. CE-PE eBGP is configured inside the customer's VRF address
family on each PE. The CE advertises its site summary and Loopback100 test
prefix.

## Apply order

1. Cable the four provider links and three CE handoffs exactly as above.
2. Apply P1, P2 and all three PE configs.
3. Verify OSPF adjacency and provider loopback reachability.
4. Verify LDP neighbors and label forwarding.
5. Apply the three CE configs and verify CE-PE eBGP.
6. Verify PE VPNv4 sessions and the customer VRF routes.
7. Ping the other two CE Loopback100 addresses from each CE.

## Verification

```text
show ip ospf neighbor
show mpls ldp neighbor
show mpls forwarding-table
show ip bgp vpnv4 all summary
show ip route vrf TVI_ENTERPRISE
show ip bgp vpnv4 vrf TVI_ENTERPRISE
show ip bgp summary
```

On each CE:
```text
show ip bgp summary
show ip route bgp
ping 10.20.250.1 source Loopback100
```

Repeat sourced pings for all remote site loopbacks. Control-plane sessions
alone do not prove the VPN data plane.

## Platform limitations

Use an IOS-XE/CSR1000v image with CEF, MPLS, LDP, VRF and VPNv4 support.
Many IOSv images do not implement all these features. Verify the selected
image and interface names before applying. These configs use classic
`ip vrf` syntax; translate consistently if the selected IOS-XE release
requires `vrf definition`.
