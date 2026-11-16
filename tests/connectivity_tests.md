# Connectivity Test Plan

| ID | Test | Expected Result | Evidence |
|---|---|---|---|
| CON-01 | Client obtains DHCP lease in each client VLAN | Correct scope, gateway and DNS | Lease details |
| CON-02 | Client reaches its default gateway | Successful ping/neighbor resolution | Client output |
| CON-03 | Inter-VLAN permitted flow | Reachability follows policy | Ping/application test |
| CON-04 | Guest to internal server/management | Denied | Failed test plus ACL counter |
| CON-05 | Hanoi to approved HQ service | Reachable | Traceroute and service test |
| CON-06 | Da Nang to approved HQ service | Reachable | Traceroute and service test |
| CON-07 | DNS resolution from each site | Correct record returned | nslookup/dig output |
| CON-08 | IPv6 reachability where deployed | Correct route and response | IPv6 ping/route output |

## Execution Record
For each test record date, topology version, source/destination, command, actual result, pass/fail and evidence path. Mark tests Not Run until executed; do not fabricate results.
