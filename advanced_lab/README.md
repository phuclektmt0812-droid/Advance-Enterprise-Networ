# TVI Advanced Enterprise Lab (separate from core)

This lab is an **optional extension** to the 14-device core topology. It lives
on its own branch and uses separate address space. Do not merge its device
configs into `network_plan.yaml` or `tools/build_lab.py`.

## Goals

Implement and demonstrate, where licensed images/controllers are available:

1. HQ EVPN-VXLAN spine/leaf fabric with MP-BGP EVPN.
2. Provider MPLS L3VPN between the three enterprise sites.
3. Controller-managed SD-WAN with dual transports and application-aware policy.
4. NGFW policy inspection and logging.
5. ZTNA/SASE application-level remote access.
6. WLC/CAPWAP wireless with corporate and guest segmentation.

The core lab remains the baseline for VLANs, campus routing, DHCP/DNS,
segmentation, QoS, and automation. Advanced features are separate overlays
or service blocks connected at defined handoff points.

## Important execution constraint

The user's known host has 8 GB RAM. Do **not** start the complete advanced
topology at once. Use the staged order below and stop unused nodes between
stages. The manifest describes a target architecture, not a claim that all
nodes have been emulated or tested.

## Stages

| Stage | Feature | Minimum practical scope | Gate |
|---|---|---|---|
| A | EVPN-VXLAN | 2 spines + 2 leaves + 2 test hosts | MP-BGP EVPN up; remote MAC/IP learned; same-VNI traffic |
| B | MPLS L3VPN | PE1-P-PE2 + PE3 as needed | LDP/IGP up; VPNv4 peers up; VRF route and site-to-site traffic |
| C | SD-WAN | 2 edges + controller components | Edges onboarded; control connections up; policy path selection |
| D | NGFW | one firewall + two test zones | allow/deny, stateful return, logs, fail-closed test |
| E | ZTNA/SASE | identity + connector + one private app | authenticated user can reach only authorized app |
| F | Wireless | WLC + 1 lightweight AP + clients | AP joined via CAPWAP; SSID VLAN mapping; guest isolation |

Stages A and B are the most useful network-engineering demonstrations.
Stages C-F depend strongly on vendor platform, licensing, controller software,
and image resources.

## Addressing

See `topology.yaml`. All ranges are private RFC1918 ranges and are disjoint
from the core lab's 10.10.0.0/16, 10.20.0.0/16 and 10.30.0.0/16 site blocks.
These are lab-only addresses; do not advertise them to a real ISP.

## Platform selection

- EVPN-VXLAN: Arista vEOS-lab is the reference syntax in
  `configs/evpn_vxlan/`; another vendor image needs a vendor-specific rewrite.
- MPLS L3VPN: Cisco IOS-XE/CSR1000v is the reference syntax in
  `configs/mpls_l3vpn/`; confirm MPLS, LDP and VRF support in the exact image.
- SD-WAN: requires licensed SD-WAN edge and controller/orchestrator images.
  Ordinary IOSv + GRE/IPsec is not controller-based SD-WAN.
- NGFW: requires a supported firewall appliance image and licenses.
- ZTNA/SASE: requires identity, connector/broker and private application.
- Wireless: requires a WLC and lightweight AP images that support CAPWAP.

No vendor images, controller licenses, credentials, or secrets are stored here.

## Validate the design manifest

From repository root:

```powershell
python tools/validate_advanced_lab.py
python -m pytest -q
```

The validator checks manifest structure and subnet overlaps only. It does not
validate vendor CLI syntax, controller onboarding, or packet forwarding.

## Build/run policy

1. Keep the core lab stopped while running an advanced stage on an 8 GB host.
2. Start with Stage A only; use 2 spines, 2 leaves and 2 lightweight test hosts.
3. Save device configs and command outputs under a local evidence folder that
   is gitignored. Never commit generated secrets or licensed images.
4. Capture positive and negative tests listed in `docs/acceptance_tests.md`.
5. Mark a feature as deployed only after its runtime acceptance tests pass.

## Integration points with core

- HQ fabric border leaf pair connects to the existing HQ routed campus core.
- MPLS PE handoffs connect to each site's edge router using dedicated
  point-to-point links; do not reuse the core lab's documentation-only ISP
  /30s without changing and revalidating the address plan.
- SD-WAN edges connect to site LAN handoff VLANs and two independent transports.
- NGFW is inserted at the designated Internet/application boundary.
- WLC management and AP CAPWAP reachability use the management/service VRF;
  SSIDs map to existing corporate and guest segmentation intent.
