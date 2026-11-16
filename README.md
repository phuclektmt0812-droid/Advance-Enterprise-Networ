# TechViet Innovations (TVI)
# Advanced Enterprise Network Design & Implementation

## 1. Project Overview

This project designs and implements a scalable enterprise network
infrastructure for TechViet Innovations (TVI).

The proposed network connects three primary geographical locations:

- Ho Chi Minh City (HCMC): Headquarters, Data Center, and Executive Offices.
- Hanoi: R&D and Engineering Campus.
- Da Nang: Logistics and Distribution Hub.

The design addresses enterprise requirements for scalability,
high availability, security, routing, WAN connectivity,
network automation, and traffic optimization.

The network is designed to support the assignment's target scale:

- 4,000+ internal users.
- 10,000+ IoT endpoints.
- External guest networks.
- Future growth to 10,000+ users by 2030.

## 2. Project Objectives

The main objectives are:

- Design a hierarchical multi-site enterprise network.
- Implement IPv4 VLSM and IPv6 Dual-Stack addressing.
- Segment enterprise traffic using VLANs and security policies.
- Implement Layer 2 switching, EtherChannel, and STP.
- Provide gateway redundancy using HSRP or VRRP.
- Deploy OSPF as the internal routing underlay.
- Use BGP for inter-site and external routing.
- Design an EVPN-VXLAN or IPsec-based WAN overlay as supported
  by the selected lab platform.
- Provide centralized DHCP services and DHCP relay.
- Implement NAT/PAT, ACLs, and network hardening.
- Apply QoS policies to prioritize voice traffic.
- Automate network configuration and backups using Python
  (Netmiko/NAPALM) or Ansible.
- Verify connectivity, redundancy, security, and automation.

## 3. Lab Platform

The assignment identifies the following primary platforms:

1. EVE-NG
2. GNS3
3. Cisco Modeling Labs (CML)

Cisco Packet Tracer may only be used if the hardware requirements
for EVE-NG/GNS3 cannot be met and the instructor grants
pre-approval.

The selected platform and its supported features must be documented
before implementation.

The implementation must not claim that a feature is functional
unless it has been configured and tested in the selected environment.

## 4. Documentation

| File | Purpose |
|---|---|
| `docs/01-project-scope.md` | Project scope and assignment requirements |
| `docs/02-network-architecture.md` | Multi-site architecture and device roles |
| `docs/03-ip-vlan-plan.md` | VLAN, IPv4 VLSM, and IPv6 addressing |
| `docs/04-routing-wan-plan.md` | OSPF, BGP, WAN, overlay, and NAT |
| `docs/05-implementation-roadmap.md` | Implementation phases and milestones |
| `docs/06-design-decisions.md` | Design decisions, assumptions, and open issues |

## 5. Design Baseline

The proposed design includes:

- Three enterprise sites: HCMC, Hanoi, and Da Nang.
- A hierarchical campus network architecture.
- A Spine-and-Leaf fabric for the HCMC Data Center.
- VLAN-based segmentation for enterprise departments and services.
- IPv4 VLSM and IPv6 Dual-Stack.
- EtherChannel using LACP.
- Rapid PVST+ or MSTP for Layer 2 loop prevention.
- HSRP or VRRP for default gateway redundancy.
- OSPF for internal routing.
- BGP for inter-site and external routing.
- EVPN-VXLAN or IPsec-based overlay connectivity.
- Centralized DHCP at HCMC with DHCP relay at remote sites.
- ACLs, Layer 2 security, and edge security policies.
- NAT/PAT for external connectivity.
- QoS for voice and other critical traffic.
- Python or Ansible-based network automation.

The exact topology, device models, interface assignments, and
address allocations must be finalized during implementation.

## 6. Automation

The automation component will use Python with Netmiko/NAPALM
or Ansible.

The automation implementation should support:

- Externalized device inventory.
- Secure credential handling.
- Baseline configuration deployment.
- VLAN provisioning.
- Configuration backup.
- Execution logging.
- Error handling.
- Idempotent execution where supported.

Credentials and private keys must never be committed to the repository.

## 7. Project Status

**Status:** Design and planning.

The documents in this repository describe the proposed design.
They do not automatically indicate that the corresponding
network features have already been implemented.

Use the following status definitions:

- Planned: included in the design but not configured.
- In Progress: configuration or testing has started.
- Verified: configured and passed the required tests.
- Deferred: postponed with a documented reason.
- Not Supported: confirmed unavailable on the selected platform.

## 8. Important Notes

- Confirm the selected lab platform before building the topology.
- Do not use Packet Tracer without the required instructor approval.
- Do not use fixed-size IPv4 subnets without considering VLSM.
- Keep IPv4 and IPv6 addressing plans consistent.
- Verify device and protocol support before implementation.
- Capture genuine configuration and test evidence.
- Do not report simulated or planned capabilities as production-ready.