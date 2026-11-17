# ZTNA/SASE implementation plan

A site-to-site VPN, ACL, or ordinary remote-access VPN alone does not satisfy
application-aware Zero Trust access.

## Components

- Identity provider with a test user group and MFA where supported.
- ZTNA access broker/controller.
- Private application connector inside the TVI service network.
- One test application (manifest address 10.43.10.10).
- Remote test client outside the enterprise LAN.
- Central audit logs.

## Access policy

- Publish only the named test application, not a broad private subnet.
- Require authenticated identity and the selected device posture conditions.
- Deny direct access to unrelated server networks.
- Apply least-privilege group-to-application mapping.
- Log authentication, policy decision, application session and denial events.

## Acceptance

Use tests E01-E05 in `advanced_lab/docs/acceptance_tests.md`. Choose a
supported vendor/SASE platform before producing API payloads or CLI config.
No credentials, tokens or certificates belong in this repository.
