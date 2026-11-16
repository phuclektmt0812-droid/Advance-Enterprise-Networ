# Network Architecture

## 1. Scope
The TVI enterprise network connects HCMC Headquarters and Data Center, Hanoi R&D and Engineering Campus, and Da Nang Logistics and Distribution Hub. The architecture separates campus LAN, Data Center fabric, WAN underlay/overlay, Internet edge, and shared services.

## 2. Logical Topology
```text
                         Internet / ISP
                               |
                         eBGP WAN Edge
                               |
                       HCMC HQ Edge / NGFW
                         /             \
                    HQ Core          Data Center
                       |             Spine / Leaf
                  Campus LAN        EVPN-VXLAN*
                       |
             +---------+---------+
             |                   |
          WAN/SD-WAN           WAN/SD-WAN
             |                   |
        Hanoi Campus         Da Nang Hub
        R&D / Engineering    Logistics / IoT
```
*EVPN-VXLAN is a design target and depends on compatible device images.

## 3. Site Roles
- **HCMC:** Headquarters, Data Center, centralized DHCP/DNS, WAN edge, Internet/NAT, security enforcement, management and automation.
- **Hanoi:** R&D and engineering users, compute/AI lab connectivity, controlled access to Data Center services.
- **Da Nang:** Logistics users, warehouse systems, IoT tracking and automation endpoints.

## 4. Campus LAN
Use a hierarchical core/distribution and access design. Segment users and services with VLANs; use 802.1Q trunks, LACP EtherChannel, RSTP/MSTP, explicit STP root selection, and HSRP/VRRP where supported. Place unused access ports in VLAN 999 and administratively disable them.

## 5. Data Center
The target fabric is Spine-and-Leaf. Spines provide routed underlay connectivity; leaf switches connect servers and provide VXLAN VTEPs. EVPN route distribution requires supported MP-BGP EVPN functionality. Do not label this fabric implemented until the selected images and lab prove it.

## 6. Routing and WAN
OSPFv2/OSPFv3 provide internal underlay reachability. BGP supports external ISP routing and the selected inter-site/overlay design. IPsec is required where encrypted site-to-site transport is specified. SD-WAN, dual-ISP and MPLS are separate capabilities; a simple routed hub-and-spoke lab is not equivalent to a full SD-WAN deployment.

## 7. Shared Services
Centralize DHCP and DNS at HCMC. Configure DHCP relay on remote client VLAN gateways. Reserve static addresses for network infrastructure and servers. Ensure the addressing plan, DHCP scopes, relay targets and device configurations agree.

## 8. Security Zones
Separate Executive/Finance, Engineering, Logistics, Server, Guest, IoT, Voice and Management traffic. Apply least-privilege ACL/firewall policy. Guest access should not reach internal corporate or management networks. IoT devices should reach only explicitly approved services.

## 9. High Availability
Use redundant uplinks, LACP, STP root planning, gateway redundancy and alternate Layer 3/WAN paths where the selected platform supports them. Demonstrate failover with recorded before/after reachability and routing state.

## 10. Open Design Inputs
Before final device configurations, confirm device models/images, physical interfaces, endpoint counts per VLAN, final VLSM, IPv6 allocation, WAN transports, wireless controller support and feature compatibility.
