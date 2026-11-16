# NAT/PAT Service

## Objective
Translate approved internal IPv4 traffic at the Internet edge.

## Design
- Perform NAT/PAT at the designated HCMC Internet-facing edge router or firewall.
- Identify inside and outside interfaces from the final topology.
- Use an explicit ACL/policy to define permitted source networks.
- Exclude internal VPN/inter-site traffic from Internet PAT where required.
- Use static NAT only for services that are intentionally published and protected by firewall policy.
- Do not use TEST-NET-3 addresses as real public addresses.

## Validation
1. Confirm internal routing before testing NAT.
2. Verify permitted clients can reach the lab's simulated external destination.
3. Inspect translation and hit counters.
4. Confirm unauthorized VLANs are not unintentionally translated or permitted.
5. Verify inter-site traffic follows the intended private path.

## Status
Design documentation only. Device-specific NAT commands require final interface mapping and ISP simulation details.
