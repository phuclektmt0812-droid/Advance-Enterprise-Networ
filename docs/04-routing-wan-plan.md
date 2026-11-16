# 04 -- Routing and WAN Plan

## 1. Autonomous Systems

  Network            AS Number
  ---------------- -----------
  Enterprise             65010
  ISP simulation         65000

These are private-use AS numbers for the lab.

## 2. OSPF Internal Routing

-   Protocol: OSPFv2 for IPv4.
-   Process ID: 10 (locally significant).
-   Area: 0.
-   Participating Layer 3 devices: R-HQ, SW-HQ-Core, R-HN, and R-DN.
-   Advertise enterprise VLAN and WAN/transit networks as appropriate.
-   Use passive interfaces on user-facing VLANs where no OSPF neighbor
    is expected.

Expected neighbor relationships:

  Link                 Expected OSPF neighbors
  -------------------- -------------------------
  R-HQ -- SW-HQ-Core   R-HQ and SW-HQ-Core
  R-HQ -- R-HN         R-HQ and R-HN
  R-HQ -- R-DN         R-HQ and R-DN

The exact network statements or interface-level OSPF configuration will
be selected after interface assignments are known.

## 3. eBGP External Routing

-   R-HQ belongs to AS 65010.
-   ISP Router belongs to AS 65000.
-   eBGP peering uses the `203.0.113.0/30` link.
-   R-HQ uses `203.0.113.1`; ISP uses `203.0.113.2`.

The ISP side should provide a default route or a small simulated
external network. The enterprise should not advertise private internal
networks to an external network unless the assignment explicitly
requires it.

## 4. Default Route Distribution

Intended traffic path:

1.  Enterprise clients send non-enterprise traffic to their local
    default gateway.
2.  OSPF provides routes between the enterprise sites.
3.  R-HQ forwards external traffic toward the ISP.
4.  R-HQ performs NAT/PAT for internal client traffic where required.
5.  The ISP returns traffic through the HQ edge router.

A default route learned or configured at R-HQ may be injected into OSPF
after the ISP-facing route is verified.

## 5. NAT/PAT

NAT/PAT is planned at R-HQ.

-   Inside interfaces: enterprise-facing interfaces/subinterfaces as
    appropriate.
-   Outside interface: ISP-facing interface.
-   Translation: overload using the HQ ISP-facing address.
-   NAT ACL: include only the enterprise private networks intended to
    access the simulated external network.

Do not configure NAT until routing between sites and the ISP test
network works without NAT where applicable.

## 6. WAN Design and VPN Clarification

The baseline uses two logical point-to-point links:

-   HQ--Hanoi: `10.255.0.0/30`
-   HQ--Da Nang: `10.255.0.4/30`

These links provide routed WAN connectivity in the simulation. They do
**not** automatically provide encryption or constitute an IPsec VPN.

If the assignment explicitly requires site-to-site VPN, decide whether
to: - Build branch-to-HQ connectivity through the ISP network and
configure a supported IPsec design; or - Use another explicitly
permitted overlay design.

Verify Packet Tracer support for the required commands and tunnel
behavior before committing to this extension.

## 7. Routing Test Targets

-   OSPF neighbors reach FULL state on all intended adjacencies.
-   Each site learns the other sites' VLAN routes.
-   A host in Hanoi can reach a permitted host/server at HQ.
-   A host in Da Nang can reach a permitted host/server at HQ.
-   HQ can reach the simulated ISP-side test network.
-   Branches can reach the simulated ISP-side test network through HQ,
    if default-route propagation and NAT are configured.
