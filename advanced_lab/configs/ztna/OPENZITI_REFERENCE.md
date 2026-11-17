# ZTNA reference implementation — OpenZiti-style overlay

This provides a concrete, software-defined ZTNA direction without treating
a site-to-site VPN or broad subnet route as Zero Trust. Select a supported
OpenZiti release and follow its official installation/CLI documentation;
exact command syntax and container images are versioned externally.

## Lab components

- Controller: identity, enrollment, service policy and edge-router metadata.
- Edge router: reachable connector point inside the TVI private network.
- Private application: one HTTP test service at 10.43.10.10.
- Remote client: enrolled user/device outside the enterprise LAN.
- Audit: controller/router events and service access logs.

## Service and identity policy

- Publish one named service, `tvi-inventory`, mapped to TCP/8080 on
  10.43.10.10.
- Define a test identity group `TVI-STAFF`.
- Permit only `TVI-STAFF` to dial `tvi-inventory`.
- Permit only the designated edge-router identity to host the service.
- Do not advertise or expose 10.43.0.0/16 as a routable remote subnet.
- Deny identities outside the group and record policy decisions.

## Deployment sequence

1. Install the controller and one edge router on a dedicated lab host.
2. Enroll the edge router and remote test client using one-time enrollment
   material stored locally; never commit tokens or private keys.
3. Create the private service mapping to 10.43.10.10:8080.
4. Create identity and service policies with least-privilege dial/bind roles.
5. Test from an enrolled authorized client.
6. Test from an unenrolled client and a different identity; both must fail.
7. Confirm the remote client cannot ping or route to unrelated private
   subnets, even though the named application is reachable.
8. Export sanitized audit events.

## Resource and security notes

Run this as a separate stage, not alongside the entire core lab on an 8 GB
host. Use current vendor documentation for installation, TLS/certificate
rotation, controller backup and supported versions. Do not expose the
controller admin API to the public Internet.

## Acceptance

Use E01-E05 in `advanced_lab/docs/acceptance_tests.md`. ZTNA is accepted
only when the named application works for an authorized identity and
unrelated subnet access remains unavailable.
