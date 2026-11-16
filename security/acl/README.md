# Access Control Lists

## Objective
Enforce least-privilege communication between enterprise security zones.

## Policy Baseline
- Guest: Internet-only; deny internal corporate, server and management networks.
- IoT: permit only required application, DNS, DHCP and management destinations.
- Management: allow administrative protocols only from approved admin hosts.
- Server: permit required application flows; deny unnecessary inbound access.
- Corporate user VLANs: permit business services according to role.

## Implementation Notes
Use named ACLs or firewall policies with documented source, destination, protocol, port and business reason. Apply rules at the appropriate Layer 3 SVI, routed interface or firewall zone boundary. Account for IPv6 separately; IPv4 ACLs do not secure IPv6 traffic.

## Validation
Test both allowed and denied flows from representative VLANs. Record command output and endpoint results. Review rule order and implicit deny behavior.

## Status
Policy baseline only; exact ACLs depend on approved service flows and final subnets.
