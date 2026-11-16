# Design Decisions and Open Issues

## 1. Purpose
Record design choices, assumptions and unresolved technical questions. A design decision is not proof of implementation; status becomes Verified only after lab testing and evidence capture.

## 2. Baseline Decisions
| ID | Decision | Rationale / Status |
|---|---|---|
| D-01 | Three sites: HCMC, Hanoi and Da Nang | Matches TVI scenario |
| D-02 | Private IPv4 planning space: 10.0.0.0/8 | Internal addressing baseline |
| D-03 | Site blocks: HCMC 10.10.0.0/16, Hanoi 10.20.0.0/16, Da Nang 10.30.0.0/16 | Proposed; check overlap with actual networks |
| D-04 | WAN transit block: 10.255.0.0/16 | Proposed lab allocation |
| D-05 | VLAN 10 Executive, 20 Engineering, 30 Logistics, 99 Management | Required to remain consistent with automation task |
| D-06 | Additional VLANs for Server, Guest, IoT, Voice and unused ports | Deploy only where required |
| D-07 | OSPF for internal routing; BGP for ISP/overlay routing | Assignment-aligned target |
| D-08 | Central DHCP/DNS at HCMC with DHCP relay at branches | Assignment-aligned target |
| D-09 | HSRP or VRRP, LACP and STP for campus resilience | Verify feature support |
| D-10 | Python/Netmiko or Ansible for automation | Depends on reachable SSH management interfaces |

## 3. Lab Planning Values
- Enterprise private AS: 65010.
- Simulated ISP private AS: 65000.
- OSPF process: 10, initially Area 0.
- HQ server planning address: 10.10.40.10.
- HQ core-router transit: 10.10.254.0/30.
- HQ-Hanoi transit: 10.255.0.0/30.
- HQ-Da Nang transit: 10.255.0.4/30.
- 203.0.113.0/24 is TEST-NET-3 documentation space, not a real public allocation.
- 2001:db8::/32 is IPv6 documentation space, not a production allocation.

## 4. Addressing Rules
Do not assume every VLAN uses /24. Calculate VLSM from endpoint counts, growth and infrastructure reservations. Keep IPv4 subnets non-overlapping. Allocate /64 prefixes to ordinary IPv6 LAN VLANs. Finalize gateways, DHCP ranges and relay targets only after the endpoint inventory and topology are approved.

## 5. Platform Decision
The assignment permits EVE-NG, GNS3 or CML. Packet Tracer should only be used if the assignment's stated conditions and instructor approval are met. Verify OSPFv3, BGP/EVPN, IPsec, HSRP/VRRP, LACP, security features, QoS and SSH automation support against the actual images.

## 6. Open Issues
| ID | Issue | Required Resolution |
|---|---|---|
| O-01 | Final lab platform and images | Select platform and verify features |
| O-02 | Endpoint counts per VLAN/site | Supply counts and growth estimates |
| O-03 | Final VLSM and IPv6 prefixes | Calculate and validate address plan |
| O-04 | Physical interfaces and links | Finalize topology and interface map |
| O-05 | Dual ISP/MPLS/SD-WAN | Decide what can be simulated and document limits |
| O-06 | EVPN-VXLAN | Confirm compatible control/data-plane support |
| O-07 | IPsec | Configure and verify encryption if required |
| O-08 | Wireless/WLC/CAPWAP | Confirm device/image support |
| O-09 | Automation SSH access | Verify management reachability and credentials handling |
| O-10 | ZTNA/SASE | Distinguish conceptual design from deployable lab functions |

## 7. Change Control
When a design changes, update the addressing workbook, topology, affected device configurations, automation inventory and tests together. Record the reason and rerun impacted tests. Never claim production throughput, four-nines availability or full-scale endpoint capacity from a small virtual lab.
