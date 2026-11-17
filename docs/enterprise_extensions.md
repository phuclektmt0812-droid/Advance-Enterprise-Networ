# TVI Enterprise Architecture Extensions and Compliance Register

**Purpose:** map every advanced enterprise requirement to an implementation or
a concrete extension design. This document distinguishes a working core lab
from a production-grade feature. A diagram, template or design explanation is
not evidence that a feature is deployed.

## 1. Compliance status

| Requirement | Current GWork implementation | Status / evidence needed |
|---|---|---|
| Three-site HQ/Hanoi/Da Nang | Dual routers and dual switches per site, two simulated ISPs | Core lab config generated; live lab required |
| IPv4 VLSM and IPv6 dual stack | network_plan.yaml, docs/ip_schema.csv, router subinterfaces | Static plan validation; live IPv4/IPv6 routing required |
| VLAN, 802.1Q, LACP, RSTP | IOSvL2 configuration generator | Verify trunks, Po1 members (P), root bridge |
| FHRP and centralized DHCP relay | HSRP, HQ dnsmasq, ip helper-address | Verify lease and WAN failure takeover |
| OSPF/OSPFv3 underlay | Per-site R1-R2 transit | Verify FULL neighbors and loopback reachability |
| eBGP with ISPs / inter-site overlay | eBGP to simulated ISP, GRE/IPsec with BGP | Verify Established and forwarding |
| NAT/PAT and Guest/IoT ACLs | Route-map overload and IPv4/IPv6 ACLs | Verify translations and positive/negative tests |
| DHCP Snooping and DAI | Switch trust boundaries on router/peer uplinks | Verify binding table and DAI drop counters |
| Port Security | Sticky MAC, maximum 2, violation restrict on host-facing ports | Generated config; verify show port-security |
| Zone-Based Firewall | Opt-in IOSv template in docs/config_templates | Not enabled by default; validate image syntax and tests |
| QoS for voice/video | EF priority class and AF31 bandwidth class | Verify counters under generated congestion |
| Netmiko automation | External inventory, getpass/env credentials, backups, snapshots, logs, idempotent state checks | Unit tests + actual SSH run |
| Physical topology | Equipment/rack and cabling view; interface matrix | Confirm node placement and cable mapping |
| EVPN-VXLAN spine-leaf | Separate two-spine/two-leaf Arista EOS starter configs, cabling/address map and host access VLANs under `advanced_lab/configs/evpn_vxlan/` | Config artifacts and manifest checks exist; live underlay, EVPN peers, VTEPs and host traffic remain unverified |
| Controller-based SD-WAN | `advanced_lab/configs/sdwan/IMPLEMENTATION_RUNBOOK.md` plus a documented dual-WAN routing fallback | Fallback is not controller SD-WAN; licensed controller/edge onboarding, policy and telemetry remain unverified |
| MPLS L3VPN | IOS-XE P/PE/CE starter configs, CE handoff map and staged bring-up under `advanced_lab/configs/mpls_l3vpn/` | Config artifacts exist; MPLS/LDP/VPNv4/VRF forwarding still requires compatible licensed images and runtime tests |
| NGFW | Zone/policy blueprint plus OPNsense lab guide under `advanced_lab/configs/security/` | Architecture and lab guide exist; firewall appliance deployment, stateful policy and inspection tests remain pending |
| ZTNA/SASE | OpenZiti reference architecture and quickstart preparation script under `advanced_lab/configs/ztna/` and `advanced_lab/deploy/ztna/` | Preparation/reference artifacts exist; identity, connector, service policy and app-only access tests remain pending |
| WLC/CAPWAP, Wi-Fi 6/7 | Catalyst 9800 WLAN/policy-profile/policy-tag CLI reference under `advanced_lab/configs/wireless/` | CLI reference exists; compatible WLC/AP, CAPWAP join and SSID traffic remain unverified |
| 10/40-Gbps and 99.99% | Production targets, not measurable from this virtual topology | Requires production hardware, capacity tests and availability evidence |
| Additional source-code items stated on assignment page 5 (client/server scripts, custom packet specification, message/file-transfer sequence diagram) | Not represented in this network-only repository | Confirm with instructor whether this cross-domain deliverable applies to Assignment 2; if it does, it is a separate missing deliverable and must not be invented from the network code |

## 2. Recommended target architecture

### Data-center fabric: EVPN-VXLAN

For a true fabric, add at least two spine nodes and two leaf nodes at HQ.
Use a compatible Arista vEOS or other supported vendor image that implements
BGP EVPN and VXLAN. Each leaf is a VTEP; spines provide the routed IP underlay
and EVPN route-reflector function. Map tenant VLANs to VXLAN VNIs, use anycast
gateway on leaf pairs, and exchange MAC/IP reachability using MP-BGP EVPN.

Minimum evidence:
- show bgp evpn summary (all peers Established)
- show vxlan vtep / vendor equivalent (VTEPs up)
- show interfaces Vxlan1 / vendor equivalent
- MAC/IP route learned remotely and same-VNI host-to-host traffic
- Underlay ECMP and a spine-link failure test

Do not label the existing campus VLAN trunks or GRE tunnels as EVPN-VXLAN.

### WAN: SD-WAN and MPLS

The existing dual-ISP design provides two underlay paths and protected GRE/IPsec
overlay tunnels. This demonstrates path diversity and failover, but is not a
controller-based SD-WAN deployment.

A complete SD-WAN demonstration needs:
- SD-WAN-capable edge nodes at all three sites
- controller/orchestrator and management-plane reachability
- dual broadband and MPLS transport labels
- centralized application-aware policy (voice prefers low-latency transport;
  bulk backup uses the cheaper transport)
- telemetry showing loss/latency/jitter and automatic path selection
- link-loss and brownout tests

MPLS requires provider PE/P nodes and a demonstrated L3VPN or equivalent
service. The two simple ISP routers in the current lab are not an MPLS core.

### Security: NGFW, ZTNA and SASE

The current ACLs, DHCP Snooping, DAI and generated access-port Port Security
are campus controls. The optional IOS Zone-Based Firewall template adds
stateful edge filtering but does not turn an IOS router into an NGFW.

A true NGFW demo requires a supported firewall appliance, zones/interfaces,
application-aware rules, IPS/URL or threat inspection as supported by the
image, and deny/allow logs.

A true ZTNA/SASE demo requires identity-aware access to a named internal
application, device/user posture or MFA integration where available, and
proof that a remote user receives access only to authorized applications.
A site-to-site IPsec tunnel or an ACL alone is not ZTNA.

### Wireless: WLC/CAPWAP

A wireless extension requires a controller and lightweight APs that support
CAPWAP, plus SSIDs mapped to corporate/guest VLANs and authentication policy.
Verify AP join state, CAPWAP control/data tunnel, SSID-to-VLAN mapping and
guest isolation. Wi-Fi 6/7 performance cannot be certified by IOSv switching.

## 3. Security implementation notes

- Access ports use sticky MAC learning, maximum two MAC addresses, and
  violation restrict; intended for a phone-plus-PC edge or small lab endpoint.
- Trunk/uplink interfaces are not Port Security access ports.
- DHCP Snooping and DAI trust is restricted to router and switch-peer uplinks.
  Host-facing ports remain untrusted.
- Guest and IoT ACLs remain the primary segmentation controls in the core lab.
- Apply docs/config_templates/IOSv_Zone_Based_Firewall_OPTIONAL.txt only
  after the base lab is stable. ZBF syntax and feature availability depend on
  IOSv release; keep console rollback access.

## 4. Design constraints and scale

The IP plan allocates 10.10.0.0/16, 10.20.0.0/16 and 10.30.0.0/16 per site.
The Da Nang IoT VLAN70 is a /18 sized for more than 10,000 endpoints. The
current node count is a teaching-scale topology, not a physical 10/40-Gbps
backbone. 99.99% availability is a design objective requiring measured
production service data; it cannot be established by a single laptop emulator.

## 5. Before claiming completion

A feature is implemented only when its config is loaded by the intended
platform, the platform accepts the configuration, the relevant positive and
negative tests pass, and raw evidence is saved. Architecture text and static
unit tests are not runtime proof.

## 6. Advance-GWork advanced implementation pack

The `Advance-GWork` branch contains an isolated `advanced_lab/` pack:
- machine-readable advanced topology and address plan;
- staged EVPN-VXLAN, MPLS L3VPN, SD-WAN, NGFW, ZTNA/SASE and WLC/CAPWAP designs;
- Arista EOS and IOS-XE reference configuration skeletons for EVPN-VXLAN
  and MPLS L3VPN;
- acceptance tests and a Python manifest validator.

This extension is deliberately not merged into the core generator. The
manifest validator checks structure and address allocation; it does not
certify vendor CLI syntax or runtime forwarding. The advanced stages remain
pending until the required licensed images/controllers are available and
their acceptance tests pass.
