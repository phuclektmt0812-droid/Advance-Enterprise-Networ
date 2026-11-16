# Security Test Plan

| ID | Test | Expected Result | Evidence |
|---|---|---|---|
| SEC-01 | Guest attempts corporate access | Denied | Endpoint result and ACL counter |
| SEC-02 | IoT attempts unauthorized server access | Denied | Endpoint result and policy counter |
| SEC-03 | Approved IoT service access | Allowed | Application test |
| SEC-04 | Untrusted access port DHCP behavior | Rogue DHCP response blocked where snooping supported | Snooping counters/log |
| SEC-05 | ARP validation | Invalid ARP rejected where DAI supported | DAI counters/log |
| SEC-06 | Management access from unapproved host | Denied | Connection test and ACL counter |
| SEC-07 | IPv6 policy enforcement | Same intended segmentation as IPv4 | IPv6 ACL/firewall test |

## Execution Record
Use isolated lab endpoints. Record test setup and actual results; do not claim a control is effective solely because its configuration command was accepted.
