# Advanced implementation matrix

| Feature | Target lab component | Reference platform | Configuration artifact | Runtime proof required |
|---|---|---|---|---|
| EVPN-VXLAN | 2 spine + 4 leaf HQ fabric | Arista vEOS-lab | `configs/evpn_vxlan/` | Underlay reachability, EVPN peers, VTEPs, remote MAC/IP, host traffic |
| MPLS L3VPN | PE/P provider cloud between 3 sites | IOS-XE/CSR1000v | `configs/mpls_l3vpn/` | IGP/LDP, VPNv4, VRF routes, inter-site traffic and isolation |
| SD-WAN | 3 site edges + dual transports + controllers | Licensed SD-WAN platform | `configs/sdwan/README.md` | Onboarding, control connections, app policy, brownout failover |
| NGFW | Internet/DMZ boundary | Licensed NGFW appliance | `configs/security/README.md` | Stateful policy, inspection, logs, negative tests |
| ZTNA/SASE | Remote user -> broker -> private app | Identity/SASE platform | `configs/ztna/README.md` | MFA/posture if supported, app-only access, denied lateral access |
| WLC/CAPWAP | WLC + lightweight AP | Supported WLC/AP images | `configs/wireless/README.md` | AP join, CAPWAP, SSID/VLAN, guest isolation |

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
