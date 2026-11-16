# Dynamic ARP Inspection

## Objective
Validate ARP messages on supported access switches using trusted DHCP Snooping bindings or configured static ARP ACLs.

## Prerequisites
- DHCP Snooping must be correctly configured for dynamic clients.
- Static-address devices need a documented static binding/ARP ACL approach.
- Trusted uplinks must match the actual topology.
- Confirm feature support before applying platform-specific commands.

## Validation
Verify legitimate ARP communication continues. In an isolated lab test, confirm invalid ARP claims are rejected and counters/logs increment as expected. Do not enable DAI without a valid binding strategy for static devices.

## Status
Implementation pending switch support and DHCP Snooping configuration.
