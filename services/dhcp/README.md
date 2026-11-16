# DHCP Service

## Objective
Provide centralized IPv4 address assignment from the HCMC services network to approved client VLANs at all sites.

## Design
- Host the DHCP service in the HCMC Server VLAN.
- Create one scope per client subnet after VLSM is finalized.
- Configure each scope with the correct network mask, default gateway, DNS server and lease policy.
- Exclude gateway, server, network-device and other statically assigned addresses.
- Configure DHCP relay on every remote Layer 3 gateway whose clients are served centrally.
- Do not provide DHCP to Management by default; use static management addresses unless the design explicitly requires otherwise.

## Validation
1. Confirm the DHCP service is reachable from each site.
2. Renew a test client lease in each client VLAN.
3. Verify assigned address, mask, gateway and DNS.
4. Confirm the lease belongs to the correct scope.
5. Confirm unauthorized/guest segments cannot obtain access to restricted internal services.

## Status
Design documentation only. Scope ranges and relay commands remain pending final VLSM and device selection.
