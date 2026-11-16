
# 06 -- Design Decisions and Open Issues

## 1. Purpose

This document records the major architectural decisions, implementation assumptions, technical constraints, and unresolved issues for the TVI enterprise network project.

It must remain consistent with:

- `01-project-scope.md`
- `02-network-architecture.md`
- `03-ip-vlan-plan.md`
- `04-routing-wan-plan.md`
- `05-implementation-roadmap.md`

A decision is considered implemented only after it has been configured and verified in the lab.

## 2. Assignment Requirements

The following requirements are explicitly stated in the assignment and must guide the design.

| ID | Requirement | Assignment Reference |
|---|---|---|
| R-01 | Support HCMC HQ, Hanoi R&D, and Da Nang Logistics sites | Project Context |
| R-02 | Support 4,000+ internal users and 10,000+ IoT endpoints, scalable to 10,000+ users by 2030 | Goals and Scale |
| R-03 | Use Spine-and-Leaf with EVPN-VXLAN for the Data Center | Enterprise Network Features |
| R-04 | Use SD-WAN with dual-ISP broadband and MPLS underlays | Enterprise Network Features |
| R-05 | Provide campus VLAN segmentation and loop prevention | Enterprise Network Features |
| R-06 | Use micro-segmentation, NGFW, and ACLs | Security Posture |
| R-07 | Implement IPv4 VLSM and IPv6 deployment | Technical Requirements |
| R-08 | Centralize DHCP at HQ and use DHCP Relay at branches | Technical Requirements |
| R-09 | Configure HSRP or VRRP for gateway redundancy | Technical Requirements |
| R-10 | Use EtherChannel with LACP on core links | Technical Requirements |
| R-11 | Use OSPF for internal routing and BGP for inter-site and external ISP routing | Technical Requirements |
| R-12 | Prioritize VoIP traffic over WAN links | Technical Requirements |
| R-13 | Implement security features including Port Security, DHCP Snooping, DAI, and Zone-based Firewall concepts | Integrated Technologies |
| R-14 | Implement network automation using Python or Ansible | Integrated Technologies |
| R-15 | Integrate WLC with CAPWAP | Integrated Technologies |
| R-16 | Verify end-to-end connectivity and failover | Implementation Process |
| R-17 | Submit a Technical Explanation Report, configurations/code, and a live simulation demonstration | Submission Requirements |

## 3. Confirmed Design Decisions

The following decisions establish the current design baseline.

| ID | Decision | Reason |
|---|---|---|
| D-01 | Use a three-site enterprise architecture: HCMC, Hanoi, and Da Nang | Matches the TVI scenario |
| D-02 | Use hierarchical IPv4 addressing with VLSM | Required by the assignment |
| D-03 | Use IPv4/IPv6 Dual-Stack as the addressing target | Required by the assignment |
| D-04 | Use separate VLANs for Corporate, Guest, IoT, Server, Voice, and Management traffic where required | Supports traffic segmentation |
| D-05 | Retain VLAN 10, 20, 30, and 99 for the automation requirements | Matches Step 9 VLAN definitions |
| D-06 | Use OSPF for internal routing | Matches the underlay requirement |
| D-07 | Use BGP for inter-site and external routing | Matches the overlay and WAN requirements |
| D-08 | Use HSRP or VRRP for default gateway redundancy | Matches the FHRP requirement |
| D-09 | Use LACP for EtherChannel links | Matches the Layer 2 requirement |
| D-10 | Use centralized DHCP at HCMC HQ with DHCP Relay at branches | Matches the IP services requirement |
| D-11 | Apply NAT/PAT at the appropriate Internet-facing edge | Supports external connectivity |
| D-12 | Use Python (Netmiko/NAPALM) or Ansible for automation | Matches Step 9 |
| D-13 | Use EVE-NG, GNS3, or CML as the primary lab platform | Matches the assignment's allowed platforms |

## 4. Proposed Addressing Decisions

The following values are planning decisions and must be checked against the final topology.

| ID | Decision | Current Value |
|---|---|---|
| D-14 | Private IPv4 address space | `10.0.0.0/8` |
| D-15 | HCMC site block | `10.10.0.0/16` |
| D-16 | Hanoi site block | `10.20.0.0/16` |
| D-17 | Da Nang site block | `10.30.0.0/16` |
| D-18 | WAN transit address space | `10.255.0.0/16` |
| D-19 | Enterprise private AS | `65010` |
| D-20 | Simulated ISP private AS | `65000` |

The IPv6 prefixes currently shown in the addressing plan use the documentation prefix `2001:db8::/32`.

They are examples for lab documentation and must not be represented as production global IPv6 allocations.

The final VLSM subnet sizes must be calculated from actual host requirements rather than assuming that every VLAN uses the same prefix length.

## 5. Lab Platform Decision

The assignment permits:

- EVE-NG.
- GNS3.
- Cisco Modeling Labs (CML).

Cisco Packet Tracer may only be used if EVE-NG/GNS3 hardware requirements cannot be met and the instructor provides prior approval.

The platform decision must consider:

- Available CPU and RAM.
- Virtualization support.
- Device image availability.
- OSPF and OSPFv3 support.
- BGP and MP-BGP support.
- EVPN-VXLAN support.
- IPsec support.
- HSRP/VRRP support.
- LACP and STP support.
- QoS support.
- SSH access for automation.

No advanced feature should be marked as implemented solely because it appears in the design document.

## 6. Automation Decisions

The assignment allows either Python or Ansible.

The implementation must satisfy these requirements:

1. Device inventory is stored externally.
2. Inventory includes hostname, management IP, device type, and SSH port.
3. Credentials are not hardcoded in scripts or configuration files.
4. Credentials are supplied through environment variables, interactive `getpass()`, or Ansible Vault.
5. Baseline configurations include AAA, NTP, Syslog, and banner.
6. VLAN provisioning includes:
   - VLAN 10: Executive.
   - VLAN 20: Engineering.
   - VLAN 30: Logistics.
   - VLAN 99: Management.
7. Capture `show running-config` and `show ip interface brief` before and after changes.
8. Save timestamped backups under `/backups/`.
9. Record successful operations and SSH exceptions in `automation.log`.
10. Handle unreachable devices without terminating the entire automation process.
11. Implement idempotency so repeated executions do not create unnecessary changes.

The automation implementation must be tested against the selected EVE-NG/GNS3/CML lab devices.

## 7. WAN and Routing Decisions

The current routing design uses:

- OSPF/OSPFv3 for internal routing.
- BGP for inter-site and external routing.
- MP-BGP EVPN where supported for the Data Center overlay.
- SD-WAN concepts for WAN path selection.
- IPsec for encrypted site-to-site connectivity where implemented.
- NAT/PAT for permitted external access.

The initial logical topology uses HQ as the central site connecting Hanoi and Da Nang.

This is an initial topology model, not proof that the full SD-WAN, dual-ISP, or MPLS architecture has been implemented.

The final WAN design must document the actual transport paths and the supported overlay technology.

## 8. Open Issues Requiring Resolution

| ID | Open Issue | Required Action |
|---|---|---|
| O-01 | Exact lab platform | Select EVE-NG, GNS3, or CML |
| O-02 | Device image availability | Confirm router and switch images |
| O-03 | Hardware resources | Confirm CPU, RAM, storage, and virtualization support |
| O-04 | Physical topology | Finalize device placement and link connections |
| O-05 | Interface mapping | Record actual interface identifiers |
| O-06 | IPv4 VLSM | Determine host counts and calculate final subnet sizes |
| O-07 | IPv6 allocation | Confirm final hierarchical prefix allocation |
| O-08 | WAN transports | Determine the available dual-ISP and MPLS simulation approach |
| O-09 | BGP overlay | Confirm iBGP/MP-BGP and EVPN support |
| O-10 | IPsec | Confirm supported tunnel implementation |
| O-11 | Gateway redundancy | Confirm HSRP/VRRP support on selected devices |
| O-12 | Layer 2 security | Verify DHCP Snooping, DAI, and Port Security support |
| O-13 | QoS | Verify marking and queuing support |
| O-14 | Wireless | Confirm WLC and CAPWAP implementation approach |
| O-15 | Automation connectivity | Confirm SSH reachability from the automation node |
| O-16 | ZTNA/SASE | Determine which aspects can be simulated and which require conceptual documentation |

Open issues must be resolved or explicitly documented as limitations before final submission.

## 9. Important Technical Caveats

### 9.1 Simulation Limitations

Virtual lab platforms may not reproduce every production feature or performance characteristic.

The project must distinguish between:

- Designed: included in the architecture.
- Configured: commands or policies have been applied.
- Verified: actual test evidence confirms the expected behavior.
- Limited: the selected platform cannot fully reproduce the feature.

Do not claim production-scale throughput, 99.99% uptime, or support for 10,000+ users based only on a small virtual simulation.

### 9.2 EVPN-VXLAN

EVPN-VXLAN requires compatible network images and appropriate control-plane and data-plane support.

If the selected images do not support the required features, document the limitation and do not claim a functioning EVPN-VXLAN fabric.

### 9.3 SD-WAN and MPLS

A basic routed connection between two sites is not equivalent to a complete SD-WAN deployment.

The final report must distinguish between the simulated WAN connectivity and the full SD-WAN design requirements.

### 9.4 IPsec

A routed point-to-point link does not provide encryption by itself.

If IPsec is required, tunnel establishment and encrypted traffic must be verified separately.

### 9.5 Automation

Netmiko and Ansible require reachable management interfaces and supported device access methods.

The automation node must be able to reach the network devices through the management network.

Credentials must never be stored as plaintext in scripts or inventory files.

## 10. Change Control

When a design decision changes:

1. Update the relevant document in `docs/`.
2. Update this decision log.
3. Update the IPv4 and IPv6 addressing plan if addresses or VLANs change.
4. Update the logical and physical topology diagrams.
5. Update device configurations and automation inventory.
6. Verify the affected network functions.
7. Record the reason and impact of the change.

All project documents, topology diagrams, and configurations must describe the same final network design.

## 11. Final Decision Status

The current repository documents represent the design baseline.

The following items remain subject to implementation and verification:

- Final physical topology.
- Final VLSM calculations.
- Final IPv6 addressing.
- Device-specific routing configurations.
- Full WAN and IPsec implementation.
- EVPN-VXLAN deployment.
- Security policy enforcement.
- QoS behavior.
- Automation execution.
- End-to-end and failover testing.

These items must not be marked complete until supported by actual lab evidence.
