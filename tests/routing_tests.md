# Routing Test Plan

| ID | Test | Expected Result | Evidence |
|---|---|---|---|
| ROUTE-01 | OSPF neighbor formation | Expected neighbors reach FULL | Neighbor output |
| ROUTE-02 | OSPF route propagation | Approved internal prefixes installed | Routing table |
| ROUTE-03 | BGP ISP peering | Session reaches Established | BGP summary |
| ROUTE-04 | BGP prefix filtering | Only approved prefixes accepted/advertised | BGP table/policy counters |
| ROUTE-05 | Inter-site route reachability | Approved site prefixes reachable | Route and traceroute |
| ROUTE-06 | Primary link failure | Alternate path converges if designed | Before/after route output |
| ROUTE-07 | IPv6 routing | OSPFv3/BGPv6 routes work where deployed | IPv6 route/neighbor output |

## Execution Record
Record actual device, command, expected result, observed result, pass/fail and evidence file. Tests remain Not Run until executed.
