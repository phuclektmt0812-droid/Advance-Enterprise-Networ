# BGP Routing

## Objective
Use eBGP for external ISP routing and the selected BGP design for inter-site or Data Center overlay routes.

## Lab Baseline
- TVI private AS: 65010.
- Simulated ISP private AS: 65000.
- Documentation-only ISP link example: 203.0.113.0/30 (TEST-NET-3).
- Apply explicit prefix filters and maximum-prefix safeguards where supported.
- Advertise only approved enterprise prefixes.
- Do not originate default or redistribute OSPF routes without a documented policy.

## EVPN Note
MP-BGP EVPN is a separate Data Center overlay requirement and requires compatible switch/router images. Basic IPv4 eBGP peering does not demonstrate EVPN-VXLAN.

## Validation
Verify peer state, received/advertised prefixes, best path, route filtering and reachability. Capture evidence for normal and failure conditions.

## Status
Design baseline only; neighbor addresses, route maps and EVPN configuration depend on the final topology and image support.
