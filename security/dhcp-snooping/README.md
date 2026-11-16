# DHCP Snooping

## Objective
Reduce rogue DHCP server risk on supported access switches.

## Implementation Checklist
- Confirm the selected switch image supports DHCP Snooping.
- Enable the feature globally and only on required client VLANs.
- Mark only links toward trusted DHCP servers/relay infrastructure as trusted.
- Keep endpoint-facing access ports untrusted.
- Set rate limits appropriate to the lab and platform.
- Persist the configuration where supported.

## Validation
Connect a test client and verify normal DHCP operation. Confirm an untrusted rogue-server path is blocked in a controlled lab test. Capture feature state and binding-table evidence.

## Status
Implementation pending platform and switch-image validation.
