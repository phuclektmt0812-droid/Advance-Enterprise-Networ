# Controller-based SD-WAN implementation plan

A dual-ISP GRE/IPsec design is not a managed SD-WAN deployment. This stage
requires a licensed platform with edge devices and controller/orchestrator
components (for example, a vendor SD-WAN virtual lab).

## Required components

- Three site edges (HCMC, Hanoi, Da Nang).
- Two independent transports per site (INET_A and INET_B).
- Vendor control/management components and an orchestrator.
- Central policy defining application classes, preferred transport, SLA
  thresholds, failover and failback behavior.
- Telemetry collection for latency, loss and jitter.

## Policy intent

| Application | Preferred path | Fallback |
|---|---|---|
| Voice/video | Path meeting lowest latency/jitter SLA | Other healthy transport |
| Business applications | Primary transport while SLA is met | Secondary transport |
| Bulk backup | Lower-cost transport | Remaining available transport |

## Implementation sequence

1. Deploy controller components in the vendor's supported order.
2. Create a lab organization/site identity and secure device onboarding.
3. Onboard one edge first; verify control-plane reachability and certificates.
4. Add the second transport and validate underlay reachability.
5. Attach the edge to a centralized policy.
6. Add remaining sites after the first edge passes.
7. Generate controlled loss/latency and verify application-aware path changes.
8. Save controller policy exports and telemetry screenshots as evidence.

Do not substitute static routes or manually configured GRE tunnels and call
that SD-WAN. Exact CLI/API steps must be generated for the selected vendor
release and controller version.
