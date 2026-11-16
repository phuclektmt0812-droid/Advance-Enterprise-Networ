# TechViet Innovations (TVI)
# Advanced Enterprise Network Design & Implementation

## 1. Project Overview
This project designs an enterprise network for TechViet Innovations (TVI), connecting:
- HCMC: Headquarters, Data Center and Executive Offices.
- Hanoi: R&D and Engineering Campus.
- Da Nang: Logistics and Distribution Hub.

The assignment targets 4,000+ internal users, 10,000+ IoT endpoints and growth to 10,000+ users by 2030. These are design targets; a small virtual lab cannot prove production-scale capacity or 99.99% availability.

## 2. Repository Structure

| Path | Purpose |
|---|---|
| `docs/project_scope.md` | Project scope and assignment requirements |
| `docs/network_architecture.md` | Multi-site logical architecture |
| `docs/design_decisions.md` | Design choices, assumptions and open issues |
| `docs/01-project-scope.md` through `docs/06-design-decisions.md` | Original numbered design documents retained for traceability |
| `topology/network_topology.drawio` | Editable logical topology diagram |
| `topology/lab/enterprise_network.gns3` | Empty GNS3 project starter; appliances and links must be added |
| `configs/` | Device-specific configuration templates (to be completed after interface mapping) |
| `services/` | DHCP, DNS and NAT design notes |
| `security/` | ACL, DHCP Snooping and DAI design notes |
| `routing/` | OSPF, BGP and VPN design notes |
| `qos/README.md` | QoS design and validation notes |
| `automation/main.py` | SSH backup and optional VLAN baseline automation |
| `automation/inventory.yaml` | Example device inventory; devices disabled by default |
| `automation/requirements.txt` | Python dependencies |
| `tests/` | Connectivity, routing, security and QoS test plans |
| `evidence/` | Directories for genuine lab evidence |

## 3. Design Baseline
- Three sites: HCMC, Hanoi and Da Nang.
- IPv4 VLSM and IPv6 Dual-Stack.
- VLAN segmentation, 802.1Q trunks, LACP and STP.
- HSRP or VRRP where supported.
- OSPF for internal routing and BGP for ISP/overlay routing.
- Central DHCP/DNS at HCMC with DHCP relay at branches.
- ACLs, Layer 2 security, NAT/PAT and QoS.
- Spine-and-Leaf EVPN-VXLAN and SD-WAN as design targets subject to image/platform support.

Proposed site IPv4 blocks are HCMC `10.10.0.0/16`, Hanoi `10.20.0.0/16`, Da Nang `10.30.0.0/16`, and WAN transit `10.255.0.0/16`. Final VLSM must use actual endpoint counts; do not assume every VLAN is a /24. `203.0.113.0/24` and `2001:db8::/32` are documentation ranges, not production allocations.

## 4. Automation

From the `automation/` directory:

1. Install dependencies with `python -m pip install -r requirements.txt`.
2. Edit `inventory.yaml` with actual management IPs and supported Netmiko device types.
3. Confirm SSH access and set `enabled: true` only for devices intentionally included.
4. Run `python main.py` to collect timestamped running-config and interface-status backups.
5. Run `python main.py --apply-vlans` only after reviewing the inventory and VLAN policy. The script backs up before and after configuration by default.

Credentials are prompted interactively or read from `TVI_NET_USERNAME` and `TVI_NET_PASSWORD`; never commit credentials. Test against a lab device before using this script on any shared environment.

## 5. Lab Platform
The assignment identifies EVE-NG, GNS3 or CML as primary platforms. The GNS3 file in this repository is only an empty starter project: add compatible appliances and links before opening the lab. Device images are not included.

Verify OSPFv3, BGP/EVPN, IPsec, HSRP/VRRP, LACP, security features, QoS and SSH automation against the selected images.

## 6. Status and Evidence
The repository contains design documentation, test plans and starter automation. It does not imply that network services, routing, security policies, QoS or WAN overlays have already been deployed.

Use these statuses:
- Planned: design exists, not configured.
- In Progress: configuration or testing has started.
- Verified: implemented and passed tests with evidence.
- Deferred: postponed with reason.
- Not Supported: unavailable on the selected platform.

Store actual outputs and screenshots under `evidence/`. Never fabricate test results or claim production capabilities from a small virtual lab.
