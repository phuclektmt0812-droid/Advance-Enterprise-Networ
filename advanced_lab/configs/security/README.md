# NGFW insertion plan

The existing IOS ACL and optional IOS Zone-Based Firewall are useful baseline
controls, but they are not equivalent to a dedicated NGFW.

## Logical zones

- TRUST: approved enterprise application/server networks.
- GUEST: guest client network; Internet-only by default.
- DMZ: published application connector or externally reachable services.
- UNTRUST: Internet/provider-facing interfaces.

## Required policy behavior

1. Default deny between zones; add explicit business-flow allow rules.
2. Permit stateful return traffic for approved sessions.
3. Restrict firewall administration to the management network.
4. Enable only licensed inspection features supported by the selected image.
5. Log both policy denies and security inspection events.
6. Define and test fail-open/fail-closed behavior before insertion.

## Deployment order

Build the firewall off-path, validate routes and policies with test clients,
then insert it at the Internet/DMZ boundary during a controlled lab change.
Keep console access and a documented rollback path.

Exact configuration is intentionally platform-specific. Select the NGFW
vendor/image and version before writing CLI commands; a generic template
could otherwise be syntactically wrong or create an unintended bypass.
