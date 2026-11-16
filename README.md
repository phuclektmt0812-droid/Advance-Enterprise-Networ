# Large Enterprise Network Design and Implementation

## 1. Project Overview

This project designs and implements a simulated enterprise network
connecting three sites:

-   **HCMC Headquarters (HQ)**
-   **Hanoi Branch**
-   **Da Nang Branch**
-   **ISP network** for external connectivity simulation

The initial implementation uses **Cisco Packet Tracer**. Python with
Netmiko is the planned automation approach, subject to connectivity and
device-support verification.

## 2. Project Objectives

The project aims to:

-   Design a structured multi-site enterprise network.
-   Segment users and services using VLANs.
-   Provide inter-VLAN and inter-site connectivity.
-   Implement dynamic routing with OSPF and external connectivity with
    eBGP.
-   Provide DHCP, DNS, NAT/PAT, and access control.
-   Demonstrate network security and traffic-management features where
    supported.
-   Develop an automation component and verify its practical
    compatibility with the lab.

## 3. Documentation

  -------------------------------------------------------------------------
  File                                  Purpose
  ------------------------------------- -----------------------------------
  `docs/01-project-scope.md`            Scope, objectives, and requirement
                                        tracking

  `docs/02-network-architecture.md`     Site architecture and device roles

  `docs/03-ip-vlan-plan.md`             VLAN and IPv4 addressing plan

  `docs/04-routing-wan-plan.md`         WAN, OSPF, BGP, and NAT design

  `docs/05-implementation-roadmap.md`   Implementation sequence

  `docs/06-design-decisions.md`         Confirmed decisions, assumptions,
                                        and open issues
  -------------------------------------------------------------------------

## 4. Current Design Baseline

-   Three enterprise sites: HCMC, Hanoi, and Da Nang.
-   IPv4 private addressing from `10.0.0.0/8`.
-   VLANs: 10 (Corporate), 20 (Guest), 30 (IoT), 40 (Server), and 99
    (Management).
-   OSPF Area 0 for internal routing.
-   eBGP between the HQ edge router and the ISP router.
-   DHCP/DNS server located at HCMC HQ.
-   NAT/PAT at the HQ edge router.

See the documents in `docs/` for the detailed plan.

## 5. Important Implementation Notes

1.  Device models and interface assignments must be verified in the
    installed Packet Tracer version before configuration.
2.  Packet Tracer is a simulator. Do not assume that every IOS command
    or external management feature is implemented.
3.  Netmiko normally requires a reachable network device exposing a
    compatible management interface. External Netmiko access to Packet
    Tracer simulated devices must be tested before treating it as a
    confirmed deliverable.
4.  VPN, IPv6, redundancy, QoS, DHCP Snooping, and Dynamic ARP
    Inspection must be checked against the assignment rubric and Packet
    Tracer feature support.
5.  Do not commit real passwords, private keys, or virtual
    machine/device images to the repository.

## 6. Project Status

**Status:** Design baseline in progress.

The addressing and architecture documents are a starting baseline.
Update the documents whenever a design decision changes, and keep device
configurations consistent with the approved plan.
