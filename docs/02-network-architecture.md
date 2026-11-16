
# 02 -- Network Architecture

## 1. Architecture Overview

The proposed TVI network connects three geographical sites:

- HCMC Headquarters and Data Center.
- Hanoi R&D and Engineering Campus.
- Da Nang Logistics and Distribution Hub.

The architecture separates the campus LAN, data center fabric, WAN underlay, WAN overlay, and external connectivity.

The design must provide scalability, redundancy, traffic isolation, and centralized network services.

## 2. Logical Architecture

                         +----------------------+
                         |       Internet       |
                         |      ISP Network     |
                         +----------+-----------+
                                    |
                              eBGP / WAN Edge
                                    |
                +-------------------+-------------------+
                |                                       |
         +------+-------+                        WAN / SD-WAN
         | HCMC HQ Edge |                       Connectivity
         | Router / NGFW|                                |
         +------+-------+                 +--------------+--------------+
                |                         |              |              |
          HQ Core / Campus               |              |              |
                |                  +------+-----+  +-----+--------+
        +-------+--------+         | Hanoi R&D  |  | Da Nang Hub |
        |                |         | Campus     |  | Logistics   |
   Campus LAN       Data Center    +------------+  +-------------+
        |                |
   User VLANs       Spine-and-Leaf
                    EVPN-VXLAN Fabric

This is a logical architecture, not a final physical topology.

The physical topology must identify:

- Device hostnames.
- Device models and images.
- Interface identifiers.
- Link types and speeds.
- VLAN IDs.
- IPv4 and IPv6 subnets.
- Layer 2 and Layer 3 boundaries.
- Trust zones.
- Redundant paths.

## 3. Site Roles

### 3.1 HCMC Headquarters

HCMC is the central enterprise site.

Responsibilities:

- Headquarters campus connectivity.
- Data Center connectivity.
- Centralized DHCP and DNS services.
- WAN edge connectivity.
- Internet access and NAT/PAT.
- Enterprise routing and route distribution.
- Security policy enforcement.
- Management and automation services.

The Data Center should use a Spine-and-Leaf architecture with EVPN-VXLAN as the target fabric technology.

### 3.2 Hanoi R&D and Engineering Campus

Responsibilities:

- Engineering user connectivity.
- High-bandwidth compute and AI lab connectivity.
- Secure access to Data Center and private cloud services.
- East-west traffic optimization.
- Local VLAN and gateway services.
- WAN connectivity to HCMC and other sites.

### 3.3 Da Nang Logistics and Distribution Hub

Responsibilities:

- Logistics and warehouse user connectivity.
- IoT tracking and automation endpoints.
- Low-latency access to required services.
- Segmentation of IoT and Corporate traffic.
- Local VLAN and gateway services.
- WAN connectivity to HCMC and other sites.

## 4. Data Center Architecture

The HCMC Data Center is designed around a Spine-and-Leaf fabric.

### Spine Layer

- Provides Layer 3 connectivity between Spine and Leaf switches.
- Supports scalable east-west traffic.
- Provides the underlay transport for the overlay.

### Leaf Layer

- Connects servers and service endpoints.
- Provides access into the Data Center fabric.
- Participates in EVPN-VXLAN overlay connectivity.

### Overlay

EVPN-VXLAN is the target technology for scalable Layer 2 over Layer 3 connectivity.

MP-BGP may be used to distribute EVPN routes.

The exact device images and feature support must be verified before implementation.

## 5. Campus LAN Architecture

The campus LAN uses a hierarchical design.

The logical layers are:

1. Core/Distribution: Layer 3 routing and gateway services.
2. Access: End-device connectivity and VLAN assignment.

The design includes:

- VLAN segmentation.
- 802.1Q trunk links.
- EtherChannel using LACP.
- Rapid PVST+ or MSTP.
- Explicit STP root bridge selection.
- Unused-port isolation using VLAN 999.
- HSRP or VRRP for default gateway redundancy.

The final topology must include redundant links and avoid unnecessary Layer 2 loops.

## 6. Layer 2 and Layer 3 Responsibilities

### Layer 2

Layer 2 switching provides:

- VLAN creation and assignment.
- Access port configuration.
- 802.1Q trunking.
- EtherChannel/LACP.
- STP loop prevention.
- Port Security.
- DHCP Snooping.
- Dynamic ARP Inspection.

### Layer 3

Layer 3 devices provide:

- Inter-VLAN routing.
- Default gateway redundancy.
- OSPF underlay routing.
- BGP overlay and external routing.
- WAN connectivity.
- Route filtering and summarization.
- DHCP relay.

## 7. Routing Architecture

The routing design separates underlay and overlay functions.

### Underlay

OSPF provides internal IP reachability across the enterprise routing infrastructure.

OSPFv3 is required for IPv6 routing.

### Overlay and WAN

BGP is used for inter-site and external routing.

The design should evaluate:

- eBGP with ISP networks.
- iBGP or MP-BGP for enterprise route distribution.
- EVPN for the Data Center overlay.
- IPsec tunnels where required for site-to-site encryption.
- SD-WAN concepts for path selection and direct cloud access.

The exact routing topology depends on the selected lab platform and supported device images.

## 8. High Availability

The design must reduce single points of failure.

Required mechanisms include:

- HSRP or VRRP for gateway redundancy.
- EtherChannel using LACP for core links.
- STP root bridge enforcement.
- Redundant Layer 3 paths where supported.
- Redundant WAN paths where supported.

Failover behavior must be demonstrated by shutting down a primary link or gateway and observing network convergence.

## 9. Centralized Network Services

Centralized DHCP services are located at HCMC HQ.

The design includes:

- DHCP scopes for client VLANs.
- DHCP relay at remote Layer 3 gateways.
- Centralized DNS services.
- Reachability from branches to central services.

The final server IP addresses must match the approved IPv4 and IPv6 addressing plan.

## 10. Security Zones

The network separates traffic into security zones.

| Zone | Purpose | Security Requirement |
|---|---|---|
| Executive | Executive and Finance devices | Strict access control |
| Engineering | R&D and Engineering devices | Controlled access to compute resources |
| Logistics | Logistics and warehouse operations | Controlled access to required services |
| Server | Enterprise services and applications | Restricted inbound access |
| IoT | Tracking and automation endpoints | Allow only required services |
| Guest | Visitors and guest devices | Internet-only access |
| Voice | IP phones and voice services | QoS and restricted access |
| Management | Network device management | Administrative access only |

ACLs and firewall policies must enforce the required isolation.

Guest devices must not access Corporate or Management resources.

IoT devices must only communicate with explicitly permitted services.

## 11. Wireless Architecture

The design should include Wireless LAN Controller (WLC) integration with CAPWAP.

Wireless access should support the relevant user groups and traffic segmentation.

The implementation must document the wireless controller, access point, VLAN, and management relationships.

Wi-Fi 6/7 capabilities are design targets and must not be claimed as implemented unless the selected lab platform supports them.

## 12. Remote Access and Cloud Connectivity

The architecture adopts ZTNA and SASE principles for remote users.

The design should consider:

- Identity-based access.
- Least-privilege authorization.
- Encrypted connections.
- Secure access to internal applications.
- Direct cloud access from branch locations where appropriate.

Commercial SASE integration is outside the scope of a basic virtual lab unless explicitly available.

## 13. Design Limitations and Open Items

- Confirm the selected lab platform and device images.
- Confirm EVPN-VXLAN and MP-BGP support.
- Confirm HSRP/VRRP and LACP support.
- Confirm IPv6 and OSPFv3 support.
- Confirm IPsec and QoS support.
- Finalize physical interface assignments.
- Finalize device quantities and redundant paths.

All limitations must be documented in the final report.
