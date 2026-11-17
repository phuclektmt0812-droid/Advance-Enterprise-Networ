# Advanced lab acceptance tests

Record command output, timestamps, topology snapshot and traffic test results
for each test. Use the exact command equivalent supported by the selected
vendor image; command names vary by release.

## A — EVPN-VXLAN

- A01: all spine/leaf underlay adjacencies are up and loopbacks are reachable.
- A02: each leaf has the expected MP-BGP EVPN peer state (Established).
- A03: all VTEPs are up and each configured VLAN maps to the intended VNI.
- A04: a MAC/IP learned behind LEAF1 is visible remotely behind LEAF2.
- A05: hosts in the same VNI on different leaves can communicate.
- A06: hosts in different VNIs cannot communicate unless an explicit L3
  gateway/policy permits it.
- A07: shut one spine-facing link; traffic reconverges through the remaining
  path and EVPN routes remain usable.

## B — MPLS L3VPN

- B01: provider IGP adjacency and loopback reachability are stable.
- B02: LDP sessions are operational and labels exist for PE loopbacks.
- B03: PE VPNv4 MP-BGP sessions are Established.
- B04: each customer VRF imports only its intended route targets.
- B05: approved HCMC/Hanoi/Da Nang prefixes are reachable across the VPN.
- B06: a route from an unrelated VRF is not leaked into the customer VRF.

## C — SD-WAN

- C01: each edge is authenticated/onboarded to the controller.
- C02: control connections and policy distribution are healthy.
- C03: voice policy selects the measured lower-latency path.
- C04: bulk-backup policy selects its configured preferred/cost path.
- C05: induce loss/latency on the preferred transport; traffic moves according
  to policy and telemetry records the event.
- C06: restore transport; verify stable failback and no persistent route loop.

## D — NGFW

- D01: approved application flow is allowed and logged.
- D02: unapproved inbound flow is denied and logged.
- D03: return traffic for an established session is handled statefully.
- D04: management plane is reachable only from the management segment.
- D05: failure/bypass test confirms the selected fail-open/fail-closed design.

## E — ZTNA/SASE

- E01: valid identity completes the configured authentication flow.
- E02: authorized identity can access only the published private application.
- E03: unauthenticated identity is denied.
- E04: authorized user cannot directly reach unrelated server subnets.
- E05: policy decision and access event are visible in audit logs.

## F — WLC/CAPWAP

- F01: AP discovers and joins the controller.
- F02: CAPWAP control channel is established.
- F03: corporate SSID maps to the corporate VLAN and receives intended DHCP.
- F04: guest SSID maps to guest VLAN and cannot reach protected corporate services.
- F05: AP/controller restart recovery is recorded.

## Evidence record template

For every test, record: test ID, image/version, device names, exact commands,
expected result, actual result, timestamp, screenshot/log path, pass/fail and
any deviation. Do not mark PASS from a configuration snippet alone.
