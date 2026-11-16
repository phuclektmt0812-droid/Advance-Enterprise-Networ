# DNS Service

## Objective
Provide centralized name resolution for approved enterprise clients and services.

## Design
- Place the primary lab DNS service in the HCMC Server VLAN.
- Document internal zones, records, forwarders and administrative ownership before implementation.
- Configure DHCP scopes to advertise the approved DNS resolver.
- Permit DNS queries only from intended client and server networks.
- Use a secondary resolver only when a real second service endpoint is configured.

## Validation
- Resolve internal service records from each site.
- Verify forward resolution and, where configured, reverse lookup.
- Confirm clients receive the intended resolver through DHCP.
- Verify guest clients cannot resolve or access restricted internal-only services unless explicitly allowed.

## Status
Design documentation only; DNS server software and records have not yet been deployed.
