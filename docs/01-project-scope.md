# 01 -- Project Scope and Requirements

## 1. Project Overview

This project designs and implements an enterprise network for
TechViet Innovations (TVI).

The network connects three primary locations:

| Site | Role | Main Requirements |
|---|---|---|
| HCMC | Headquarters, Data Center, Executive Offices | Central services, high availability, data center connectivity |
| Hanoi | R&D and Engineering Campus | High-bandwidth compute, AI labs, secure private cloud access |
| Da Nang | Logistics and Distribution Hub | IoT connectivity, warehouse automation, low-latency services |

The design must support:

- 4,000+ internal users.
- 10,000+ IoT endpoints.
- External guest networks.
- Growth to 10,000+ users by 2030.

The assignment also specifies a 10/40 Gbps HQ backbone
and a 99.99% availability target.

These are design targets. A small virtual lab cannot independently
prove production-scale throughput or four-nines availability.

## 2. Project Scope

The project includes the following areas:

1. Enterprise network architecture and logical topology.
2. IPv4 VLSM and IPv6 Dual-Stack addressing.
3. VLANs, trunking, EtherChannel, and Spanning Tree.
4. First Hop Redundancy Protocols.
5. Centralized DHCP and DHCP relay.
6. OSPF internal routing.
7. BGP inter-site and external routing.
8. WAN overlay using EVPN-VXLAN or IPsec as appropriate.
9. Network security and traffic segmentation.
10. NAT/PAT and external connectivity.
11. QoS for voice traffic.
12. Network automation using Python or Ansible.
13. End-to-end testing and technical documentation.

## 3. Functional Requirements

| Area | Required Capability | Status |
|---|---|---|
| Architecture | Three-site enterprise network | Planned |
| Data Center | Spine-and-Leaf architecture with EVPN-VXLAN design | Planned |
| LAN | VLANs and 802.1Q trunking | Planned |
| Link Aggregation | EtherChannel using LACP | Planned |
| Loop Prevention | RSTP or MSTP with root bridge enforcement | Planned |
| Gateway Redundancy | HSRP or VRRP | Planned |
| IP Addressing | IPv4 VLSM and IPv6 Dual-Stack | Planned |
| Internal Routing | OSPF underlay | Planned |
| Overlay Routing | BGP/EVPN or IPsec connectivity | Planned |
| External Routing | eBGP with ISP | Planned |
| DHCP | Centralized DHCP at HQ and relay at branches | Planned |
| DNS | Centralized DNS services | Planned |
| NAT | NAT/PAT overload | Planned |
| Security | ACLs, segmentation, and edge security | Planned |
| Layer 2 Security | Port Security, DHCP Snooping, and DAI | Planned |
| Remote Access | ZTNA/SASE principles | Planned |
| QoS | Voice traffic prioritization across WAN links | Planned |
| Wireless | WLC and CAPWAP integration | Planned |
| Automation | Python/Ansible configuration and backup automation | Planned |
| Verification | Connectivity, failover, security, and automation tests | Planned |

A requirement is marked Verified only after implementation and
successful testing.

## 4. Non-Functional Requirements

### 4.1 Scalability

The addressing and network architecture must accommodate the
current user and IoT requirements and allow future expansion.

### 4.2 High Availability

The design must reduce single points of failure through:

- Redundant Layer 2 links.
- EtherChannel using LACP.
- STP root bridge planning.
- HSRP or VRRP gateway redundancy.
- Redundant Layer 3 paths where supported.
- WAN redundancy concepts.

### 4.3 Performance

The design must consider:

- High-bandwidth data center traffic.
- East-west traffic in the Hanoi R&D environment.
- Low-latency IoT and logistics traffic.
- Voice and video traffic.
- Direct cloud access where appropriate.

### 4.4 Security

The network must isolate Guest, Corporate, IoT, Server,
and Management traffic.

Security controls should include ACLs, Layer 2 protections,
secure management protocols, and remote-access security principles.

### 4.5 Automation

Configuration and backup tasks should be repeatable,
logged, and protected against unnecessary configuration changes.

Credentials must not be stored as plaintext in source files.

## 5. Lab Platform Requirements

The assignment allows:

- EVE-NG.
- GNS3.
- Cisco Modeling Labs (CML).

Cisco Packet Tracer is permitted only when EVE-NG/GNS3
hardware requirements cannot be met and the instructor
has approved its use in advance.

The selected platform must be documented.

The following must be verified against the selected platform
and device images:

- OSPFv3 and IPv6 support.
- BGP and MP-BGP support.
- EVPN-VXLAN support.
- IPsec support.
- HSRP or VRRP support.
- LACP and STP support.
- QoS and security feature support.
- External SSH access for automation.

## 6. Out of Scope and Limitations

The following production capabilities may not be fully reproducible
in a small educational virtual lab:

- Actual 10/40 Gbps production throughput.
- Measured 99.99% production availability.
- Full-scale 10,000-user and 10,000-IoT endpoint load.
- Commercial SASE service integration.
- Production-grade Wi-Fi 6/7 coverage and roaming.

These requirements should be addressed through design,
configuration evidence, and documented limitations.

They must not be claimed as fully implemented unless
the lab provides valid evidence.

## 7. Requirement Tracking

Use the following status definitions:

- **Planned:** included in the design but not configured.
- **In Progress:** configuration or testing has started.
- **Verified:** implemented and passed the required tests.
- **Deferred:** postponed with a documented reason.
- **Not Supported:** confirmed unavailable on the selected platform.

Each requirement should have corresponding configuration
and verification evidence before being marked Verified.

## 8. Assignment Clarification

The assignment includes a general submission paragraph requesting
client/server scripts, custom packet/message structures, and
message/file-transfer sequence diagrams.

These items appear different from the main enterprise network
design requirements.

The project team should clarify with the instructor whether
these client/server deliverables are additionally required
or whether they are generic submission instructions.

They should not be silently treated as completed network
automation deliverables.