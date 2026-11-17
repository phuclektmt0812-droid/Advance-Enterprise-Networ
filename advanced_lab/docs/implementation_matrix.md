# Advanced implementation matrix

| Feature | Target lab component | Reference platform | Configuration artifact | Runtime proof required |
|---|---|---|---|---|
| EVPN-VXLAN | 2 spine + 2 leaf minimum HQ fabric | Arista vEOS-lab | `configs/evpn_vxlan/SPINE1.cfg`, `SPINE2.cfg`, `LEAF1.cfg`, `LEAF2.cfg` | Underlay reachability, EVPN peers, VTEPs, remote MAC/IP, host traffic |
| MPLS L3VPN | 2 P + 3 PE + 3 CE handoffs | IOS-XE/CSR1000v | `configs/mpls_l3vpn/P1.cfg`, `P2.cfg`, `PE-*.cfg`, `CE-*.cfg`, `CE_HANDOFF.md` | IGP/LDP, VPNv4, VRF routes, inter-site traffic and isolation |
| SD-WAN | 3 site edges + dual transports + controllers | Licensed SD-WAN platform | `configs/sdwan/IMPLEMENTATION_RUNBOOK.md`, `configs/sdwan/DUAL_WAN_ROUTING_FALLBACK.md` | Onboarding, control connections, app policy, brownout failover |
| NGFW | Internet/DMZ boundary | OPNsense for lab demonstration; commercial NGFW for full vendor feature set | `configs/security/OPNSENSE_LAB_GUIDE.md`, `NGFW_POLICY_BLUEPRINT.md` | Stateful policy, IDS alerts, logs, negative tests |
| ZTNA/SASE | Remote user -> broker -> private app | Identity/SASE platform | `configs/ztna/OPENZITI_REFERENCE.md`, `deploy/ztna/prepare-openziti.ps1` | MFA/posture if supported, app-only access, denied lateral access |
| WLC/CAPWAP | WLC + lightweight AP | Supported WLC/AP images | `configs/wireless/C9800_CLI_TEMPLATE.txt`, `configs/wireless/README.md` | AP join, CAPWAP, SSID/VLAN, guest isolation |

## Order of work

1. EVPN-VXLAN fabric (Stage A).
2. MPLS L3VPN service (Stage B).
3. NGFW insertion and policy (Stage D).
4. SD-WAN (Stage C).
5. Wireless (Stage F).
6. ZTNA/SASE (Stage E).

This order validates routing and segmentation before adding controller- and
identity-dependent systems. The order can change if the available licensed
images dictate otherwise.

## Non-goals

- This branch does not claim production 10/40-Gbps throughput or 99.99%
  availability from an emulator.
- It does not store vendor images, controller licenses, API tokens, passwords,
  certificates, or IPsec keys.
- It does not change the core lab's default topology or generated configs.
