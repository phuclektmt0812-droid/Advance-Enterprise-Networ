# TVI Physical Topology and Cabling Plan

This physical view complements TVI_Logical_Topology.drawio. It describes
equipment placement, physical roles and cable termination; exact interface
names are maintained in interface_matrix.csv.

## HQ — Ho Chi Minh City

| Physical block | Equipment | Role |
|---|---|---|
| MDF / Network Room | HCMC-R1, HCMC-R2 | Redundant WAN edge / L3 gateway pair |
| MDF / Network Room | HCMC-SW1, HCMC-SW2 | Collapsed distribution/access pair; RSTP and LACP |
| Server rack | HQ-DHCP-DNS | DHCP, DNS, NTP, Syslog and inventory HTTP |
| Management segment | AUTOMATION | Netmiko control node |
| User access | Corporate, Guest, IoT and Voice endpoints | Segmented access VLANs |

## Hanoi — R&D and Engineering

| Physical block | Equipment | Role |
|---|---|---|
| Network room | HANOI-R1, HANOI-R2 | Redundant WAN edge / L3 gateway pair |
| Campus wiring closet | HANOI-SW1, HANOI-SW2 | L2 access/distribution pair |
| User/compute access | Engineering, Guest, IoT and Voice endpoints | Segmented access VLANs |

## Da Nang — Logistics and Distribution

| Physical block | Equipment | Role |
|---|---|---|
| Network room | DANANG-R1, DANANG-R2 | Redundant WAN edge / L3 gateway pair |
| Warehouse wiring closet | DANANG-SW1, DANANG-SW2 | L2 access/distribution pair |
| Warehouse access | Logistics, Guest, IoT and Voice endpoints | Segmented access VLANs |

## WAN and demarcation

- ISP-A terminates all R1 WAN uplinks; ISP-B terminates all R2 WAN uplinks.
- ISP-A and ISP-B have a simulated inter-provider link.
- ISP-A has a dedicated simulated Internet test-host link.
- Four logical GRE/IPsec tunnel pairs connect HQ to Hanoi and Da Nang; these
  are overlays and do not require extra physical cables.
- In production, ISP circuits should enter diverse carrier demarcation devices
  and separate building entrances/ducts where possible.

## Physical resiliency caveat

The teaching topology still has shared site power, a shared emulator host,
single-attachment Linux services, and limited access endpoints. Two routers
and two switches reduce some network-device single points of failure but do
not prove end-to-end four-nines availability. Production design needs diverse
power, cooling, cabling, service-host HA, dual access paths and measured
recovery objectives.

## Emulator mapping

Use docs/interface_matrix.csv as the authoritative cable list. Before loading
configuration, confirm every selected image exposes the expected interface
names and sufficient Ethernet ports. Save the actual node-to-port map with
the demo evidence because image interface enumeration can differ.
