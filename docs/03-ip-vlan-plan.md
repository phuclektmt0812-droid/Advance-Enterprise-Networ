
# 03 -- VLAN and IP Addressing Plan

## 1. Addressing Design Objectives

The TVI network must use hierarchical IPv4 subnetting (VLSM) and IPv6 allocation across all three geographical sites.

The addressing plan must support:

- HCMC Headquarters and Data Center.
- Hanoi R&D and Engineering Campus.
- Da Nang Logistics and Distribution Hub.
- 4,000+ internal users.
- 10,000+ IoT endpoints.
- External guest networks.
- Growth to 10,000+ users by 2030.
- Centralized DHCP services at HQ and DHCP Relay at branch sites.
- IPv4/IPv6 Dual-Stack deployment.

The final IP schema must be documented in an Excel or Markdown table.

## 2. IPv4 Addressing Architecture

The proposed private IPv4 addressing space is `10.0.0.0/8`.

Each geographical site receives a separate address block:

| Site | IPv4 Address Block | Purpose |
|---|---|---|
| HCMC HQ | `10.10.0.0/16` | Headquarters and Data Center |
| Hanoi | `10.20.0.0/16` | R&D and Engineering Campus |
| Da Nang | `10.30.0.0/16` | Logistics and Distribution Hub |
| WAN Transit | `10.255.0.0/16` | Routed inter-site links |

These blocks are proposed planning allocations. They must be checked against the final topology before implementation.

### 2.1 VLSM Allocation Rules

VLSM must allocate subnet sizes according to the actual number of required hosts in each network.

The allocation process is:

1. Identify the required number of hosts for every VLAN and routed segment.
2. Include expected growth in the host requirement.
3. Sort subnet requirements from largest to smallest.
4. Select the smallest subnet that can accommodate the required hosts.
5. Allocate subnets without overlap.
6. Record the network address, prefix length, subnet mask, usable range, and gateway.

For an IPv4 subnet:

`2^h - 2 >= required_hosts`

Where `h` is the number of host bits.

The prefix length is:

`32 - h`

The actual host requirements must be determined from the site and VLAN endpoint estimates. A fixed `/24` allocation for every VLAN is not assumed to be the final VLSM result.

### 2.2 VLSM Planning Worksheet

The following table is the allocation worksheet. Prefix lengths and address ranges must be finalized after the endpoint requirements are confirmed.

| Site | VLAN | Network Purpose | Required Hosts | Prefix | Network Address | Default Gateway |
|---|---:|---|---:|---|---|---|
| HCMC | 10 | Executive / Finance | TBD | TBD | TBD | TBD |
| HCMC | 20 | R&D / Engineering | TBD | TBD | TBD | TBD |
| HCMC | 30 | Logistics Operations | TBD | TBD | TBD | TBD |
| HCMC | 40 | Servers | TBD | TBD | TBD | TBD |
| HCMC | 50 | Guest | TBD | TBD | TBD | TBD |
| HCMC | 60 | IoT | TBD | TBD | TBD | TBD |
| HCMC | 70 | Voice | TBD | TBD | TBD | TBD |
| HCMC | 99 | Management | TBD | TBD | TBD | TBD |
| Hanoi | 10 | Executive / Finance | TBD | TBD | TBD | TBD |
| Hanoi | 20 | R&D / Engineering | TBD | TBD | TBD | TBD |
| Hanoi | 30 | Logistics Operations | TBD | TBD | TBD | TBD |
| Hanoi | 50 | Guest | TBD | TBD | TBD | TBD |
| Hanoi | 60 | IoT | TBD | TBD | TBD | TBD |
| Hanoi | 70 | Voice | TBD | TBD | TBD | TBD |
| Hanoi | 99 | Management | TBD | TBD | TBD | TBD |
| Da Nang | 10 | Executive / Finance | TBD | TBD | TBD | TBD |
| Da Nang | 20 | R&D / Engineering | TBD | TBD | TBD | TBD |
| Da Nang | 30 | Logistics Operations | TBD | TBD | TBD | TBD |
| Da Nang | 50 | Guest | TBD | TBD | TBD | TBD |
| Da Nang | 60 | IoT | TBD | TBD | TBD | TBD |
| Da Nang | 70 | Voice | TBD | TBD | TBD | TBD |
| Da Nang | 99 | Management | TBD | TBD | TBD | TBD |

VLANs that are not required at a particular site should not be configured there merely because they appear in this planning worksheet.

## 3. VLAN Design

The assignment's Network Automation example specifies the following VLANs:

| VLAN ID | VLAN Name | Purpose |
|---:|---|---|
| 10 | EXEC_FINANCE | Executive and Finance devices |
| 20 | RND_ENGINEERING | R&D and Engineering devices |
| 30 | LOGISTICS_OPS | Logistics and warehouse operations |
| 99 | MANAGEMENT | Network device management |

These four VLAN IDs and names should remain consistent with the automation configuration.

The following additional VLANs are proposed to support the assignment's traffic-segmentation requirements. Their final use and deployment at each site must be confirmed in the topology.

| VLAN ID | VLAN Name | Purpose |
|---:|---|---|
| 40 | SERVER | Data Center and enterprise servers |
| 50 | GUEST | Guest and visitor devices |
| 60 | IOT | IoT tracking and automation endpoints |
| 70 | VOICE | IP phones and voice traffic |
| 999 | BLACKHOLE | Unused access ports |

Guest, IoT, and Corporate traffic must be isolated using appropriate ACLs and security policies.

VLAN 999 is reserved for unused access ports and must not be used for normal endpoint connectivity.

## 4. HCMC Headquarters Addressing

Site address block: `10.10.0.0/16`

HCMC contains the Headquarters campus and Data Center.

The proposed VLAN subnet assignments are recorded in the VLSM worksheet in Section 2.2.

### 4.1 Network Infrastructure

The following infrastructure addresses are retained as initial lab planning values:

| Device | Interface / Purpose | IPv4 Address |
|---|---|---|
| SW-HQ-Core | Management SVI | `10.10.99.2` |
| SW-HQ-A1 | Management SVI | `10.10.99.3` |
| SW-HQ-A2 | Management SVI | `10.10.99.4` |
| DHCP/DNS Server | Server VLAN | `10.10.40.10` |
| SW-HQ-Core | Routed transit interface | `10.10.254.2` |
| R-HQ | Routed transit interface | `10.10.254.1` |

The core-to-router transit network is:

- Network: `10.10.254.0/30`
- R-HQ: `10.10.254.1`
- SW-HQ-Core: `10.10.254.2`

These initial values must be reconciled with the final VLSM allocation and actual device interfaces.

## 5. Hanoi Branch Addressing

Site address block: `10.20.0.0/16`

Hanoi provides connectivity for R&D and Engineering users, high-bandwidth compute resources, and AI lab infrastructure.

The required VLANs and subnet allocations must be determined using the VLSM worksheet.

The site must have:

- Engineering user segmentation.
- Management network connectivity.
- Guest isolation where guest access is provided.
- IoT segmentation where IoT endpoints are deployed.
- Voice segmentation where IP telephony is deployed.
- Routed connectivity to HQ and the Data Center.

## 6. Da Nang Branch Addressing

Site address block: `10.30.0.0/16`

Da Nang provides connectivity for Logistics and Distribution operations.

The required VLANs and subnet allocations must be determined using the VLSM worksheet.

The site must have:

- Logistics and warehouse user segmentation.
- IoT tracking and automation network segmentation.
- Management network connectivity.
- Guest isolation where guest access is provided.
- Voice segmentation where IP telephony is deployed.
- Routed connectivity to HQ and the Data Center.

The IoT subnet must be sized according to the expected number of endpoints and future growth.

## 7. WAN and Routed Transit Networks

The following point-to-point networks are proposed for the initial lab topology.

| Link | Network | Endpoint A | Endpoint B |
|---|---|---|---|
| HQ -- Hanoi | `10.255.0.0/30` | R-HQ: `10.255.0.1` | R-HN: `10.255.0.2` |
| HQ -- Da Nang | `10.255.0.4/30` | R-HQ: `10.255.0.5` | R-DN: `10.255.0.6` |
| HQ -- Core | `10.10.254.0/30` | R-HQ: `10.10.254.1` | SW-HQ-Core: `10.10.254.2` |
| HQ -- ISP | `203.0.113.0/30` | R-HQ: `203.0.113.1` | ISP: `203.0.113.2` |

`203.0.113.0/24` is a documentation and testing range (TEST-NET-3). It is not a real public Internet allocation.

The final WAN design must account for the assignment's SD-WAN requirement, dual-ISP broadband and MPLS underlays.

Additional WAN links and addresses must be added when the final topology is defined.

## 8. IPv6 Addressing Architecture

The assignment requires IPv4/IPv6 Dual-Stack deployment and hierarchical IPv6 allocation across all sites.

The final IPv6 plan must:

- Allocate a separate site-level prefix to each geographical site.
- Allocate subnet prefixes to individual VLANs.
- Use `/64` prefixes for normal LAN VLANs.
- Provide separate prefixes for routed infrastructure links where required.
- Document IPv6 gateways and device addresses.
- Ensure IPv6 routing is supported by the selected network devices.

### 8.1 Proposed IPv6 Planning Structure

For documentation and lab planning, the following structure illustrates hierarchical allocation:

| Site | Example Site Prefix | Purpose |
|---|---|---|
| HCMC HQ | `2001:db8:10::/48` | Headquarters and Data Center |
| Hanoi | `2001:db8:20::/48` | R&D and Engineering Campus |
| Da Nang | `2001:db8:30::/48` | Logistics and Distribution Hub |

`2001:db8::/32` is reserved for documentation. These example prefixes are not production IPv6 allocations and must be replaced with an assigned prefix for a real deployment.

### 8.2 IPv6 VLAN Allocation Worksheet

Each VLAN receives a separate `/64` subnet from its site's `/48` allocation.

| Site | VLAN ID | Purpose | Example IPv6 Prefix |
|---|---:|---|---|
| HCMC | 10 | EXEC_FINANCE | `2001:db8:10:10::/64` |
| HCMC | 20 | RND_ENGINEERING | `2001:db8:10:20::/64` |
| HCMC | 30 | LOGISTICS_OPS | `2001:db8:10:30::/64` |
| HCMC | 40 | SERVER | `2001:db8:10:40::/64` |
| HCMC | 50 | GUEST | `2001:db8:10:50::/64` |
| HCMC | 60 | IOT | `2001:db8:10:60::/64` |
| HCMC | 70 | VOICE | `2001:db8:10:70::/64` |
| HCMC | 99 | MANAGEMENT | `2001:db8:10:99::/64` |
| Hanoi | 10 | EXEC_FINANCE | `2001:db8:20:10::/64` |
| Hanoi | 20 | RND_ENGINEERING | `2001:db8:20:20::/64` |
| Hanoi | 30 | LOGISTICS_OPS | `2001:db8:20:30::/64` |
| Hanoi | 50 | GUEST | `2001:db8:20:50::/64` |
| Hanoi | 60 | IOT | `2001:db8:20:60::/64` |
| Hanoi | 70 | VOICE | `2001:db8:20:70::/64` |
| Hanoi | 99 | MANAGEMENT | `2001:db8:20:99::/64` |
| Da Nang | 10 | EXEC_FINANCE | `2001:db8:30:10::/64` |
| Da Nang | 20 | RND_ENGINEERING | `2001:db8:30:20::/64` |
| Da Nang | 30 | LOGISTICS_OPS | `2001:db8:30:30::/64` |
| Da Nang | 50 | GUEST | `2001:db8:30:50::/64` |
| Da Nang | 60 | IOT | `2001:db8:30:60::/64` |
| Da Nang | 70 | VOICE | `2001:db8:30:70::/64` |
| Da Nang | 99 | MANAGEMENT | `2001:db8:30:99::/64` |

Only deploy VLANs that are required at the corresponding site.

The IPv6 prefixes above are planning examples. They must be checked against the final topology and actual IPv6 allocation.

## 9. DHCP Address Pool Convention

DHCP services are centralized at HCMC HQ.

The DHCP design must provide:

- Separate scopes for each client VLAN.
- Correct network and subnet mask.
- Correct default gateway.
- DNS server information.
- Exclusion of static infrastructure addresses.
- DHCP Relay at remote branch gateways.

The final DHCP ranges must be calculated after VLSM allocation is completed.

The existing HCMC server planning address is `10.10.40.10`.

This address must be verified against the final Server VLAN subnet before configuring DHCP.

## 10. DHCP Relay

The assignment requires DHCP servers to be centralized at HQ with DHCP Relay at branches.

The design must include:

- DHCP Relay on the Layer 3 gateway of each remote client subnet.
- Relay forwarding to the centralized DHCP server.
- Correct routing between branch gateways and HQ.
- DHCP scopes corresponding to the actual branch VLAN subnets.

Management VLAN DHCP is optional in the initial lab design. Static management addressing may be used where appropriate.

## 11. Addressing Validation Checklist

- [ ] Every site has a separate hierarchical IPv4 address block.
- [ ] IPv4 VLSM is calculated using actual host requirements.
- [ ] The address plan accounts for future endpoint growth.
- [ ] No IPv4 subnets overlap.
- [ ] Every VLAN has a documented IPv4 gateway.
- [ ] IPv6 prefixes are allocated hierarchically.
- [ ] IPv6 LAN VLANs use the planned `/64` prefix length.
- [ ] IPv4 and IPv6 Dual-Stack connectivity is tested.
- [ ] Every routed point-to-point link has a unique subnet.
- [ ] Static server and infrastructure addresses are excluded from DHCP.
- [ ] DHCP scopes match the documented subnet, mask, gateway, and DNS settings.
- [ ] DHCP Relay works from Hanoi and Da Nang to the centralized HQ DHCP server.
- [ ] VLAN IDs and names match the network configuration and automation scripts.
- [ ] All device configurations match the final approved addressing plan.
