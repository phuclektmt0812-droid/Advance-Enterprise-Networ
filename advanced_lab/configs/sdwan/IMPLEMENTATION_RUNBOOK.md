# Controller-based SD-WAN — implementation runbook

This runbook defines the minimum controller-managed deployment. The existing
core dual-ISP GRE/IPsec overlay is **not** SD-WAN and remains unchanged.

## Required platform

Select one supported licensed SD-WAN stack before deployment (for example,
Cisco Catalyst SD-WAN with Manager/Controller/Validator and compatible
cEdge/vEdge images). The exact product naming and onboarding workflow varies
by release. Do not apply ordinary IOSv configurations and label them SD-WAN.

## Logical components

- Manager/orchestrator: templates, policy, monitoring and device lifecycle.
- Controller/control-plane: secure control connections and route/policy
  distribution.
- Validator/orchestrator: secure initial onboarding and reachability.
- Three site edge devices: HCMC, Hanoi and Da Nang.
- Two underlay transports per site: INET_A and INET_B.
- Central policy and telemetry collector.

## Site and application policy

| Site | Edge | Primary transport | Secondary |
|---|---|---|---|
| HCMC | SDWAN-HCMC | INET_A | INET_B |
| Hanoi | SDWAN-HANOI | INET_A | INET_B |
| Da Nang | SDWAN-DANANG | INET_A | INET_B |

| Application class | Match | Preferred path | Fallback |
|---|---|---|---|
| Voice | DSCP EF / voice application | Lowest latency/jitter within SLA | Other healthy path |
| Business | Approved business app signatures/prefixes | INET_A | INET_B |
| Bulk backup | Backup server/destination | INET_B | INET_A |
| Guest | Guest segment | Internet local breakout | Deny private prefixes |

## Deployment sequence

1. Install controller components using the vendor's validated order and
   sizing guide; synchronize DNS, NTP and certificates.
2. Create organization identity, site IDs, device templates and onboarding
   credentials locally (never commit them).
3. Configure both underlays and verify reachability to controller endpoints.
4. Onboard HCMC edge only; verify certificate/authentication and control
   connections before adding branches.
5. Apply a feature/device template with both transports and a centralized
   control policy.
6. Configure application-aware routing using measured SLA thresholds for
   loss, latency and jitter; thresholds are lab policy inputs, not claimed
   measured values.
7. Add Hanoi and Da Nang after HCMC passes.
8. Simulate loss/latency on one transport and verify app-specific path
   selection and failback.
9. Export sanitized policy and event evidence.

## Required checks

Use the platform's equivalent of:
- controller inventory/device health;
- control connections and certificate state;
- BFD/session state for each transport;
- application route/policy match;
- SLA class and path-selection counters;
- event/telemetry history during brownout and recovery.

## Not a substitute

Static routes, IP SLA tracking, HSRP, dual ISP or manually configured
GRE/IPsec tunnels can demonstrate WAN redundancy, but they do not provide
controller-based SD-WAN orchestration or application-aware centralized
policy. If the selected image/controller is unavailable, report this stage
as design-ready but not deployed.
