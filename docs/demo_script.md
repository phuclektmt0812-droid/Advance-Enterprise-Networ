# 15-minute TVI Live Demonstration — Presenter Script

| Time | Demonstrate | Recommended evidence |
|---|---|---|
| 0:00–1:30 | Company scenario and 3-site Draw.io design, VLAN security zones, redundancy | Draw.io logical topology, `ip_schema.csv` |
| 1:30–3:00 | HCMC/Hanoi/Da Nang VLANs, trunks, LACP, Port Security and STP | `show vlan brief`, `show etherchannel summary`, `show spanning-tree root`, `show port-security` |
| 3:00–4:30 | IPv4 VLSM, dual-stack, HSRP and centralized DHCP | `show standby brief`; VPCS `ip dhcp`; inspect lease settings |
| 4:30–6:30 | OSPF, provider eBGP and GRE over IPsec overlays | `show ip ospf neighbor`, `show ip bgp summary`, `show crypto ipsec sa` |
| 6:30–8:00 | Ping between sites; NAT translation; Guest ACL deny and Internet allow | Ping, `show ip nat translations`, deny counters |
| 8:00–9:00 | QoS EF voice treatment and traffic policy | `show policy-map interface` and traffic counters |
| 9:00–11:30 | HSRP / WAN failover: continuous ping, `shutdown` HANOI-R1 Gi0/1, observe backup route, restore | Record convergence time and brief outage; must recover within 3 min target |
| 11:30–13:30 | Run Python automation on switch, VLAN140 create, before/after backups, repeat showing idempotency | Shell output; backups; automation.log |
| 13:30–15:00 | Final technical explanation: why OSPF+BGP, ACLs, centralized DHCP, limitations and questions | Report + limitations |

## Failover commands (console only)

On `HANOI-R1`:

```text
configure terminal
interface GigabitEthernet0/1
shutdown
end
show standby brief
show ip bgp summary
```

From a Hanoi client, maintain an ongoing ping to a verified HQ server or routed management destination. If VPCS continuous ping behavior differs, use a Linux client with `ping -i 0.2 10.10.60.10`. Record packet loss and when replies resume.

Restore:

```text
configure terminal
interface GigabitEthernet0/1
no shutdown
end
show standby brief
```

**Never shut down the only live interface providing your presenter/automation console access.** Use the emulator's local console for maintenance tests.

## Likely lecturer questions

- What is the difference between physical underlay routing and GRE/IPsec overlay routing?
- Why have two routers and LACP/STP when a simple switch/router could provide basic connectivity?
- How does the standby HSRP router take over when the primary's WAN interface goes down?
- Why are guest clients blocked from HQ resources even when inter-site routing is working?
- Why is NAT for external access but not applied to traffic routed into IPsec tunnels?
- How do IPv6 ACLs protect guest access, and why is a separate IPv6 routing plan required?
- What causes DHCP Relay to be needed at branches?
- Which parts of a full enterprise deployment are not simulated and how would they be added?
- What safeguards prevent automated changes from being repeated or applied with plaintext passwords?
