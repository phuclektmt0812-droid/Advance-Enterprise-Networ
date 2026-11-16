# OSPF Routing

## Objective
Provide internal IPv4 reachability using OSPFv2 and IPv6 reachability using OSPFv3 where supported.

## Baseline
- Proposed process ID: 10.
- Initial area: 0.
- Advertise only approved routed links, loopbacks and VLAN networks.
- Use passive interfaces for user-facing LANs unless an OSPF neighbor is intentionally required.
- Use point-to-point network type on routed point-to-point links where appropriate.
- Authenticate adjacencies where supported and required.
- Do not redistribute routes without an explicit filtering policy.

## Validation
Check neighbor state, route table, interface participation and end-to-end reachability. Test convergence after a planned link failure and retain before/after evidence.

## Status
Design baseline; network statements and interface commands require final addressing and interface mapping.
