
# 04 -- Routing and WAN Plan

## 1. Routing Architecture Overview

The TVI enterprise network uses an underlay and overlay routing architecture.

The routing design must connect:

- HCMC Headquarters and Data Center.
- Hanoi R&D and Engineering Campus.
- Da Nang Logistics and Distribution Hub.
- External ISP networks.

The assignment specifies:

- OSPF for internal site routing (Underlay).
- BGP for inter-site and external ISP routing (Overlay).
- OSPFv3 and IPv4/IPv6 Dual-Stack technologies.
- SD-WAN concepts, IPsec VPN tunnels, and NAT/PAT.
- eBGP with ISPs and iBGP/EVPN or IPsec tunnels connecting HQ to Hanoi and Da Nang.

The final routing configuration depends on the selected topology and supported network images.

## 2. Autonomous System Design

The following AS numbers are proposed for the lab:

| Network | AS Number | Description |
|---|---:|---|
| TVI Enterprise | 65010 | Private enterprise AS |
| ISP Simulation | 65000 | Simulated external ISP AS |

These are private-use AS numbers for lab simulation.

The final AS assignment must be consistent across all BGP configurations.

## 3. Internal Routing -- OSPF

OSPF provides internal IP reachability within the enterprise network.

### 3.1 OSPF Design

| Parameter | Planned Value |
|---|---|
| IPv4 Routing Protocol | OSPFv2 |
| IPv6 Routing Protocol | OSPFv3 |
| OSPF Process ID | 10 |
| Initial Area Design | Area 0 |
| Enterprise AS | 65010 |

OSPF is used for internal site routing and underlay reachability.

The design must include:

- HCMC HQ routing infrastructure.
- Hanoi branch routing infrastructure.
- Da Nang branch routing infrastructure.
- Routed transit links.
- Loopback interfaces where required.
- Appropriate VLAN and infrastructure network advertisements.

OSPF process IDs are locally significant and do not need to be identical on every router.

### 3.2 OSPF Neighbor Relationships

The initial logical topology expects the following IPv4 OSPF adjacencies:

| Link | Expected Neighbors |
|---|---|
| R-HQ -- SW-HQ-Core | R-HQ and SW-HQ-Core |
| R-HQ -- R-HN | R-HQ and R-HN |
| R-HQ -- R-DN | R-HQ and R-DN |

These relationships are planning assumptions based on the initial hub-and-spoke topology.

The actual neighbor relationships must be updated when the final physical and logical topology is completed.

### 3.3 OSPF Configuration Principles

- Use Area 0 as the initial single-area design.
- Advertise required infrastructure and enterprise networks.
- Configure passive interfaces on user-facing VLANs where no OSPF neighbor is expected.
- Avoid forming OSPF adjacencies with end-user devices.
- Use loopback interfaces for stable router identification where appropriate.
- Verify OSPF neighbor state and route installation.
- Ensure IPv6 routing is handled through OSPFv3 where supported.

The final design must satisfy the assignment's requirement that loopback interfaces be reachable within each site.

## 4. BGP Overlay and External Routing

BGP provides inter-site and external routing.

### 4.1 External eBGP

The initial ISP simulation uses:

| Device | AS Number | Interface Address |
|---|---:|---|
| R-HQ | 65010 | `203.0.113.1` |
| ISP Router | 65000 | `203.0.113.2` |

The proposed ISP-facing network is:

- Network: `203.0.113.0/30`
- R-HQ: `203.0.113.1`
- ISP: `203.0.113.2`

`203.0.113.0/24` is a documentation-only IPv4 range and must not be treated as a real public Internet allocation.

The ISP simulation should provide a default route or a small external test network.

### 4.2 Inter-Site BGP

The assignment requires BGP-based overlay routing or IPsec connectivity between HQ and the two branches.

The final design must evaluate:

- eBGP peering with external ISP networks.
- iBGP for enterprise route distribution where appropriate.
- MP-BGP EVPN for the Data Center fabric where supported.
- Route summarization at branch edges.
- Route filtering and prefix control.

The exact BGP peer relationships must be determined from the final topology.

### 4.3 Route Advertisement Policy

The enterprise routing policy should:

- Advertise only required enterprise prefixes.
- Avoid leaking private internal routes to external ISP networks.
- Use route filtering where appropriate.
- Summarize branch prefixes where the topology permits.
- Control default-route propagation.
- Verify that each site receives the routes it needs.

## 5. WAN and SD-WAN Design

The assignment specifies an SD-WAN deployment connecting HCMC, Hanoi, and Da Nang using:

- Dual-ISP broadband underlays.
- MPLS underlay connectivity.
- Direct cloud access from branch offices where appropriate.

The logical WAN design must provide connectivity between all three geographical sites.

### 5.1 Initial Logical WAN Links

The following links are initial lab planning values:

| Link | IPv4 Network | Endpoint A | Endpoint B |
|---|---|---|---|
| HQ -- Hanoi | `10.255.0.0/30` | R-HQ: `10.255.0.1` | R-HN: `10.255.0.2` |
| HQ -- Da Nang | `10.255.0.4/30` | R-HQ: `10.255.0.5` | R-DN: `10.255.0.6` |

These links represent routed connectivity in the initial logical topology.

They do not automatically provide encryption or constitute an SD-WAN deployment.

### 5.2 SD-WAN Design Considerations

The final design should document:

- WAN transport links.
- Primary and backup paths.
- Dual-ISP connectivity.
- MPLS connectivity where available.
- Application-aware path selection.
- Direct cloud access.
- WAN failover behavior.
- QoS policy application across WAN links.

If the selected lab platform cannot emulate commercial SD-WAN functions, the limitation must be documented and the supported WAN behavior demonstrated.

## 6. IPsec VPN

The assignment includes IPsec VPN tunnels as a WAN technology and requires overlay connectivity between HQ and branch sites.

The final implementation must determine whether IPsec tunnels will be used for:

- HQ-to-Hanoi connectivity.
- HQ-to-Da Nang connectivity.
- Secure transport over an ISP network.

A routed point-to-point link alone is not an IPsec VPN.

The implementation must verify:

- Tunnel establishment.
- Peer reachability.
- Encryption and authentication parameters.
- Routing through the tunnel.
- End-to-end connectivity across the encrypted path.

The exact IPsec configuration depends on device image and platform support.

## 7. Default Route Distribution

The intended external traffic path is:

1. Enterprise clients send non-local traffic to their default gateway.
2. OSPF provides internal enterprise route reachability.
3. The HQ edge router forwards external traffic toward the ISP or selected WAN path.
4. NAT/PAT translates private source addresses where required.
5. Return traffic is routed back through the appropriate edge.

A default route may be configured or learned at the HQ edge and distributed internally when appropriate.

The final route policy must avoid creating routing loops or unintended default-route propagation.

## 8. NAT/PAT

NAT/PAT is planned at the Internet-facing edge router or firewall.

The design includes:

- Inside interfaces connected to enterprise networks.
- Outside interfaces connected to ISP networks.
- NAT overload for internal clients requiring external access.
- Access lists identifying the private networks allowed to use NAT.
- Verification of translation and return traffic.

NAT/PAT must be tested after basic internal and external routing is functional.

Private enterprise routes should not be advertised as public Internet routes.

## 9. Route Summarization

Branch route summarization should be considered to reduce routing table size.

The proposed site IPv4 blocks are:

| Site | Address Block |
|---|---|
| HCMC | `10.10.0.0/16` |
| Hanoi | `10.20.0.0/16` |
| Da Nang | `10.30.0.0/16` |

These summaries may be used only if the actual subnet allocations remain within their respective site blocks and the routing topology supports summarization.

## 10. Routing and WAN Verification

The following tests are required:

### OSPF

- [ ] Intended OSPF neighbors reach FULL state.
- [ ] Required enterprise routes appear in routing tables.
- [ ] Loopback interfaces are reachable within each site.
- [ ] Passive interfaces are configured on user-facing subnets.
- [ ] OSPFv3 provides IPv6 route reachability where implemented.

### BGP

- [ ] eBGP peering with the simulated ISP is established.
- [ ] Required enterprise prefixes are advertised.
- [ ] Route filtering prevents unintended private route advertisement.
- [ ] Branch route summarization works where configured.
- [ ] iBGP/MP-BGP or the selected overlay mechanism operates as designed.

### WAN and IPsec

- [ ] HQ can reach Hanoi and Da Nang.
- [ ] Branches can reach permitted HQ services.
- [ ] IPsec tunnels show an operational state where implemented.
- [ ] WAN failover behavior is tested where redundant paths exist.
- [ ] Direct cloud access is documented or simulated where supported.

### NAT/PAT

- [ ] Internal clients can reach the simulated external network.
- [ ] NAT translations are created correctly.
- [ ] Return traffic reaches the original clients.

All verification results must be supported by genuine command outputs or simulation evidence.
