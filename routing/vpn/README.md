# Site-to-Site VPN

## Objective
Provide encrypted inter-site transport where the approved WAN design requires IPsec.

## Design Requirements
- Identify tunnel endpoints and protected subnets.
- Select a platform-supported IKE/IPsec profile.
- Use strong supported cryptographic settings and unique credentials stored outside source control.
- Define routing over the tunnel and prevent unintended clear-text fallback.
- Keep VPN traffic separate from Internet PAT as required.
- Document any platform limitation.

## Validation
Verify IKE and IPsec security associations, counters, protected-subnet reachability and behavior after tunnel interruption. Confirm test traffic is actually encrypted; a routed point-to-point link alone is not a VPN.

## Status
Design documentation only. No tunnel is claimed as configured or verified.
