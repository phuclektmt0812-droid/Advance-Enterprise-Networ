# 02 -- Network Architecture

## 1. High-Level Design

The enterprise network contains one headquarters, two branches, and one
ISP simulation.

``` text
                         +----------------+
                         |   ISP Router   |
                         |    AS 65000    |
                         +--------+-------+
                                  |
                              eBGP / WAN
                                  |
                         +--------+-------+
                         |   R-HQ (Edge)  |
                         +--------+-------+
                                  |
                         Transit Ethernet
                                  |
                         +--------+-------+
                         |   SW-HQ-Core   |
                         | Layer 3 Switch |
                         +---+--------+---+
                             |        |
                       Trunk |        | Trunk
                             |        |
                       +-----+--+  +--+------+
                       |SW-HQ-A1|  |SW-HQ-A2 |
                       +--------+  +---------+
                             |
                     HQ user/server VLANs

          OSPF point-to-point WAN links from R-HQ:
                   /                         \
                  /                           \
          +------+-----+                 +-----+------+
          |    R-HN     |                 |    R-DN     |
          +------+-----+                 +-----+------+
                 |                             |
              Trunks                        Trunk
                 |                             |
          +------+-----+                 +-----+------+
          | Branch LAN |                 | Branch LAN |
          | 2 x L2 SW  |                 | 1 x L2 SW  |
          +------------+                 +------------+
```

The diagram is logical. Physical interface numbers and exact cable types
will be recorded after devices are placed in Packet Tracer.

## 2. Device Roles

  ---------------------------------------------------------------------------
  Site             Device role                   Quantity Responsibility
  ---------------- ---------------- --------------------- -------------------
  HCMC             Edge router                          1 WAN, OSPF, eBGP,
                                                          NAT/PAT

  HCMC             Layer 3 core                         1 HQ VLAN gateways
                   switch                                 and inter-VLAN
                                                          routing

  HCMC             Layer 2 access                       2 End-device access
                   switch                                 and VLAN trunking

  HCMC             Server                          1 or 2 DHCP and DNS

  Hanoi            Branch router                        1 WAN routing and
                                                          router-on-a-stick

  Hanoi            Layer 2 access                       2 User access
                   switch                                 

  Da Nang          Branch router                        1 WAN routing and
                                                          router-on-a-stick

  Da Nang          Layer 2 access                       1 User access
                   switch                                 

  ISP              ISP router                           1 External routing
                                                          simulation
  ---------------------------------------------------------------------------

Candidate models include Cisco 2911 routers, Catalyst 3560 Layer 3
switches, and Catalyst 2960 Layer 2 switches. These are candidates, not
a final interface-level commitment. Confirm availability and feature
support in the installed Packet Tracer version.

## 3. Layer 2 and Layer 3 Design

### HCMC HQ

-   The Layer 3 core switch hosts SVIs for VLANs 10, 20, 30, 40, and 99.
-   The two access switches connect to the core using 802.1Q trunks.
-   The core switch connects to the HQ edge router through a dedicated
    routed transit subnet.
-   The DHCP/DNS server uses a static address in VLAN 40.

### Hanoi

-   The branch router provides default gateways using 802.1Q
    subinterfaces.
-   The two access switches provide user access ports and trunk
    connectivity.
-   VLANs 10, 20, 30, and 99 are planned.

### Da Nang

-   The branch router provides default gateways using 802.1Q
    subinterfaces.
-   The access switch provides user access ports and a trunk to the
    router.
-   VLANs 10, 20, 30, and 99 are planned.

## 4. Routing Design

-   OSPF Area 0 is used for internal enterprise routing.
-   OSPF runs between the HQ edge router, HQ core switch, and branch
    routers.
-   eBGP runs between the HQ edge router (AS 65010) and ISP router (AS
    65000).
-   The HQ edge router is the enterprise exit point toward the simulated
    ISP.
-   A default route from the ISP side is intended to be propagated into
    the enterprise OSPF domain, subject to the final routing
    configuration.

## 5. Centralized Services

The DHCP/DNS server is located at HCMC HQ.

-   DHCP scopes are created for each client VLAN.
-   Remote VLANs use DHCP relay on their Layer 3 gateway.
-   DNS records are configured on the central server.
-   Branches must have routed reachability to the server subnet.

## 6. Security Zones

-   **Corporate (VLAN 10):** internal employee devices.
-   **Guest (VLAN 20):** restricted access; should not initiate
    connections to Corporate or Management networks.
-   **IoT (VLAN 30):** restricted access to only required services.
-   **Server (VLAN 40):** centrally hosted services at HQ.
-   **Management (VLAN 99):** device management traffic.

ACL policy details will be documented before implementation. Do not
apply an ACL until required permitted services and management access
have been identified.

## 7. Design Limitations and Open Items

-   The initial logical WAN design uses point-to-point links between HQ
    and branches. This is not, by itself, an IPsec VPN. If the
    assignment requires site-to-site VPN, the WAN design must be
    extended and verified against Packet Tracer support.
-   Physical redundancy and HSRP are not included in the first baseline.
-   QoS, DHCP Snooping, and DAI depend on the selected Packet Tracer
    device models and supported commands.
