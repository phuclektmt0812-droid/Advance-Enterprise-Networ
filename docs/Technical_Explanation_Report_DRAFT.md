---
title: "TechViet Innovations: Enterprise Network Design and Implementation"
subtitle: "Technical Explanation Report — Draft, Pending Live Lab Verification"
author: "Student / Team: [ADD GROUP NAME]"
date: "13 November 2026"
lang: en-US
geometry: "margin=0.82in"
fontsize: 10pt
mainfont: "DejaVu Sans"
colorlinks: true
---

\newpage

# Executive Summary

This report proposes a three-site enterprise IP network for TechViet Innovations (TVI), connecting Ho Chi Minh City headquarters, the Hanoi engineering campus, and the Da Nang logistics hub. The design addresses isolation of departments, resilient site gateways, secure inter-site communications, private branch addressing, prioritized voice services, and automated infrastructure administration.

The implemented **teaching-lab design** includes two network routers and two campus switches at each site, two simulated ISP routers, four GRE tunnels protected by IPsec, internal OSPF, inter-site and ISP BGP sessions, redundant virtual IPv4 gateways, centralized HQ DHCP/DNS, VLAN segmentation, ACL-based restrictions, PAT, policy-based QoS, and secure Python/Netmiko automation. The working implementation must be validated inside GNS3 or EVE-NG using licensed IOSv and IOSvL2 images.

**Verification status:** Python-based static checks and mocked automation tests are available. **End-to-end device behavior and SLA claims are not yet independently verified.** The instructor should not treat a generated Cisco configuration as proof of successful emulation. Evidence screenshots must be added after running the live test plan.

# Business Requirements and Scope

TVI serves more than 2,000 headquarters users, 1,500 Hanoi engineering users, and 500 Da Nang logistics users, plus 10,000+ IoT endpoints and guests. The assignment specifies growth to 10,000+ internal users by 2030, a 10/40 Gbps HQ backbone target, 99.99% uptime, secure hybrid workforce access, and differentiated traffic handling for voice, video, and data.

The emulated lab **does not instantiate thousands of hosts**. The IP allocation reserves enough space for enterprise growth, while sample client nodes exercise forwarding. Physical link speeds and the stated uptime target cannot be certified by a small virtual topology. Real production design would require hardware sizing, formal capacity/availability studies, link diversity, and fault-domain analysis.

# Logical Network Architecture

![Illustrative three-site logical topology. Exact port mapping is recorded in `docs/interface_matrix.csv`.](TVI_Logical_Topology.png){ width=100% }

**HCMC** uses two campus/WAN routers with HSRP and LACP-connected switches. The HCMC service VLAN (60) hosts centralized DNS/DHCP, a demonstration inventory web endpoint, NTP, and syslog. An automation host in management VLAN 99 uses SSH to administer the enterprise infrastructure.

**Hanoi** uses engineering VLAN20 with `/21` IPv4 capacity and a redundant WAN design. **Da Nang** uses a `/18` IPv4 IoT segment, permitting more than 16,000 addresses in that segment alone. All three sites use VLANs 10, 20, 30, 50, 70, 80, 99, and 999, with VLAN60 at HQ.

Two simulated providers (ISP-A AS64501 and ISP-B AS64502) connect the enterprise R1 and R2 paths, respectively. GRE/IPsec tunnels from HQ to the branches carry inter-site BGP routes for private enterprise address blocks. This represents a secure WAN overlay, **not a genuine orchestrated SD-WAN service**.

# IPv4 VLSM and IPv6 Plan

The source-of-truth for addresses is `network_plan.yaml`, with a generated full allocation table `docs/ip_schema.csv`. Summary site allocations are:

| Site | IPv4 summary | IPv6 summary | Enterprise ASN |
|---|---|---|---|
| HCMC | 10.10.0.0/16 | 2001:db8:10::/48 | 65010 |
| Hanoi | 10.20.0.0/16 | 2001:db8:20::/48 | 65020 |
| Da Nang | 10.30.0.0/16 | 2001:db8:30::/48 | 65030 |

Selected IPv4/VLSM allocations:

| Site / VLAN | Prefix | Virtual gateway | Capacity intent |
|---|---|---|---|
| HCMC VLAN10 executives | 10.10.8.0/22 | 10.10.8.1 | 1,022 usable hosts |
| HCMC VLAN20 engineering | 10.10.16.0/22 | 10.10.16.1 | 1,022 usable hosts |
| Hanoi VLAN20 engineering | 10.20.16.0/21 | 10.20.16.1 | 2,046 usable hosts |
| Da Nang VLAN30 logistics | 10.30.32.0/22 | 10.30.32.1 | 1,022 usable hosts |
| Da Nang VLAN70 IoT | 10.30.128.0/18 | 10.30.128.1 | 16,382 usable hosts |
| All sites VLAN99 | 10.x.99.0/24 | 10.x.99.1 | Device management |

Every site's R1 VLAN interface uses the second usable host address (usually `.2`), R2 the third (`.3`), with a virtual HSRP gateway at the first usable address (`.1`). IPv6 VLANs use `/64` allocations like `2001:db8:20:20::/64` for Hanoi Engineering; router interface suffixes are `::2` and `::3`. IPv6 is carried through GRE tunnels with eBGP peering over IPv6 tunnel addressing. The `2001:db8::/32` IPv6 range and `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24` IPv4 WAN ranges are documentation-only; these addresses **cannot serve as real public Internet allocations**.

`python tools/validate_plan.py` examines collisions among VLAN, routed transit, loopback, WAN, and overlay subnets. A site-level `/16` summary is distributed through BGP using a high-distance Null0 covering route, while connected and OSPF-learned more-specific VLAN routes permit local forwarding.

# Layer 2 Design: VLAN, STP, and Link Aggregation

Each site uses two layer-2 switches connected through a two-member LACP EtherChannel. Inter-switch links form `Port-channel1`; `GigabitEthernet0/1` and `GigabitEthernet0/2` carry the physical links. `GigabitEthernet0/0` on each switch is an 802.1Q trunk toward its site's router. The native VLAN is VLAN999, and unused access ports are administratively shut down in VLAN999.

Rapid PVST+ elects SW1 as the intended primary root (priority 4096) and SW2 as secondary (8192). STP protects against accidental L2 loops beyond the single logical LACP port-channel; it does not substitute for router high availability. PortFast/BPDU Guard are enabled only on intended host-facing ports. DHCP Snooping and Dynamic ARP Inspection protect selected client VLANs, with trusted router uplinks and LACP port-channels.

Expected commands: `show vlan brief`, `show interfaces trunk`, `show etherchannel summary`, `show spanning-tree root`, `show ip dhcp snooping`, `show ip arp inspection`.

# First-Hop Redundancy, DHCP Relay, and DNS

Each router implements HSRP for enterprise VLANs. R1 has priority 110, R2 priority 100; both use `preempt`, and WAN interface tracking subtracts 30 from R1's priority on uplink failure. If R1's WAN fails, R2 should become active and send traffic through ISP-B and the backup GRE/IPsec overlay. Router failover is demonstrable; HQ server or single-attachment access-client failures are not covered by the scaled lab.

The central DHCP and DNS service is `10.10.60.10` in HQ VLAN60. Both routers configure `ip helper-address 10.10.60.10` on client VLAN interfaces. Linux `dnsmasq` uses the relay agent IP address to select the correct scope and hands out virtual HSRP gateway addresses and appropriate DNS settings. Guest DHCP options use DNS `192.0.2.18` on the simulated Internet service rather than the HQ private resolver.

HCMC server also runs basic chrony NTP, syslog reception on UDP/514, and an inventory service on `10.10.60.20:8080`. The inventory service is a lab endpoint for testing allowed IoT traffic, not a production database.

# Internal OSPF and Inter-Site BGP/Protected WAN

Each site has a directly connected R1-R2 transit (`10.x.254.0/30`), with OSPF Area 0 and OSPFv3 adjacency on those links. VLAN networks are advertised passively in OSPF; loopback interfaces support stable router identity and reachability tests. When an R1 campus trunk fails, R1 can learn the surviving site's specific VLAN routes over the transit from R2 instead of forwarding only toward a Null0 summary.

BGP is used in two distinct contexts. First, each enterprise R1 forms eBGP with ISP-A and R2 with ISP-B. Second, enterprise routers exchange site `/16` routes with branch peers over GRE tunnels protected by IPsec. R1 and R2 additionally use iBGP within each site to share private site routes and support alternate forwarding. Prefix lists block private corporate prefixes from being advertised to the simulated ISP neighbors, while WAN underlay reachability is provided by directly connected networks and routed/provider prefixes.

There are **four tunnel pairs:** HCMC-R1/HANOI-R1, HCMC-R2/HANOI-R2, HCMC-R1/DANANG-R1, and HCMC-R2/DANANG-R2. The GRE tunnels carry IPv4 and IPv6 routes; IKEv1 with an auto-generated disposable pre-shared key establishes IPsec security associations. For production use, migrate to appropriately approved IKEv2/certificates and hardened cryptographic parameters, and test both active and backup underlay paths.

Successful configuration must be demonstrated with `show ip ospf neighbor`, `show ip bgp summary`, tunnel interface states, `show crypto isakmp sa`, and actual incrementing `show crypto ipsec sa` counters after inter-site traffic. The presence of `Tunnel10` in configuration alone **does not prove** that cryptographic negotiation succeeded.

# Access Security, NAT, and IPv6 Isolation

The design places Guests in VLAN50 and IoT systems in VLAN70. IPv4 ACLs block Guest access to `10.0.0.0/8` internal enterprise networks while allowing outbound simulated Internet traffic. IoT ACLs permit DNS to HQ DNS and application access to inventory host `10.10.60.20`, but deny other enterprise-private destinations. Matching IPv6 ACLs restrict Guest and IoT access to the lab's `2001:db8::/32` enterprise documentation space. Actual production access policies should be evaluated for stateful behavior and strict least privilege.

NAT/PAT uses an extended ACL and route-map on each enterprise WAN edge interface. Internal-to-internal destinations are exempted from overload NAT, so VPN-bound traffic uses original enterprise addresses. Internet-bound packets are translated to the corresponding ISP-facing router IP. Verification requires both NAT table entries and a successful HTTP response from the simulated Internet host (`192.0.2.18`).

SSH is the only configured vty management protocol; a management-source ACL restricts login to site management subnets. Disposable lab credentials are generated locally on demand and excluded from version control. AAA, NTP, Syslog, and banners can also be deployed through Netmiko automation.

# Voice/Video QoS

Voice VLAN80 interfaces mark incoming demonstration voice traffic with DSCP EF. The WAN QoS policy contains a priority class for EF (20%) and a bandwidth class for AF31 video (15%), with class-default forwarding for ordinary data. QoS should be evaluated under congestion, and voice/video counters must increase on the actual IOS image. Depending on the IOSv forwarding path and whether classification occurs before or after encryption, packet counters on the physical IPsec-transporting interface may require image-specific policy placement. Configuration text alone is insufficient QoS proof.

# Network Automation (Step 9)

`automation/auto_provision.py` reads `automation/inventory.yaml` and `automation/vlans.yaml`, prompts securely for credentials when not supplied by the environment, and uses Netmiko SSH to manage enterprise nodes. For every successful connection it saves **before and after** snapshots of `show running-config` and `show ip interface brief`, applies missing AAA/NTP/Syslog/banner settings, and creates missing standard corporate VLANs and demonstration VLAN140 on switches. It saves running changes to startup and logs successes, errors, and connect failures. It avoids reapplying already present settings when a device returns consistent running-state information.

The automation project includes mock-driven tests for idempotency and connection failure handling. Real image support must still be tested. Inventory excludes ISP routers because they are modeled as third-party providers. `build/` files contain disposable secrets and must not be published or reused on production infrastructure.

# Testing, Fault Injection, and Evidence

The complete test plan is `docs/testcases.md`, containing routing, DHCP, ACL-negative, IPv6, NAT, EtherChannel, QoS, security, automation, and failover cases. Example acceptance tests include:

- HANOI-CORP-CLIENT obtains an address in `10.20.16.0/21`, gateway `10.20.16.1` from centralized HQ DHCP.
- HANOI-GUEST-CLIENT cannot ping HQ's private server but can access simulated Internet host `192.0.2.18` using PAT.
- HCMC-R1 learns a private route to Da Nang through the active GRE/IPsec/BGP overlay.
- A shutdown of HANOI-R1 `GigabitEthernet0/1` causes HSRP to transfer to HANOI-R2 and inter-site traffic to recover via ISP-B/tunnel11.
- The first Netmiko run creates demo VLAN140 and backups; repeated execution does not apply unnecessary changes.

**Actual results: NOT YET RECORDED.** After completing the lab, insert command outputs/screenshots into the final PDF. At minimum include OSPF/BGP neighbors, HSRP roles, DHCP client settings, NAT table entries, an IPsec SA counter sample, access-list deny counters, QoS classes, automation logs, and a failover packet-loss/timing summary. Do not replace results with expected behavior text.

## Live test record template

| Case | Date/time | Expected | Actual observation | Result | Evidence |
|---|---|---|---|---|---|
| R03 | [fill] | HQ to Hanoi management ping succeeds | [collect] | **NOT TESTED** | [CLI screenshot] |
| D05 | [fill] | Guest cannot reach HQ private server | [collect] | **NOT TESTED** | [ACL/ping screenshot] |
| R10 | [fill] | Failover to R2 via ISP-B | [measure convergence] | **NOT TESTED** | [ping & HSRP] |
| A01 | [fill] | Netmiko creates VLAN140 and backups | [collect] | **NOT TESTED** | [script log] |

# Implementation Limitations, Risks, and Future Enhancements

The scaled teaching lab illustrates the required traditional network mechanisms but has **not** implemented a genuine EVPN-VXLAN spine/leaf fabric, an SD-WAN policy controller, managed NGFW, WLC/CAPWAP Wi-Fi 6/7 integration, or end-user SASE/ZTNA broker. Although the assignment mentions these as enterprise technology targets, implementation scope cannot be inferred solely from the basic 10-step lab scorecard. Confirmation from the lecturer is needed before declaring full compliance.

The single attached HQ service host, single connected endpoint links, and one lab machine hosting the emulator are remaining single points of failure. The emulated virtual interfaces also cannot demonstrate a guaranteed 40 Gbps production backbone or 99.99% annual service uptime. For a production evolution, use redundant service hosts and distribution planes, diverse WAN carriers, proper cryptographic governance, managed policy enforcement, remote-access identity integration, resilient EVPN fabric, wireless control, telemetry, and automated recovery runbooks.

# Reproducibility and Submission

The repository provides generated Cisco initial configuration sources, YAML inventory and address plan, Python automation, topology diagrams, Ubuntu service scripts, tests, and a 15-minute demonstration script. The actual grading submission should additionally include **exported startup-configs from each running virtual device** and screenshots/results from completed live tests. A ZIP package without that runtime evidence should be labeled a working project candidate rather than a fully validated enterprise deployment.

The detailed installation and execution procedure is in `README.md`. Lab source code is deliberately kept separate from disposable credentialed files in `build/`.
