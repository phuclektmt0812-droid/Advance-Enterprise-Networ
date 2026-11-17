# TVI Test Cases and Verification Matrix

**Meaning of status:** `STATIC CHECK` means verified by Python/tests only. `LAB REQUIRED` means a real IOSv/IOSvL2 GNS3/EVE-NG implementation must be operating first. **No lab-required test is represented as having passed yet.** All commands below assume Cisco IOSv/IOSvL2 CLI; equivalent CLI may differ by image/version.

## A. Automated local tests

| ID | Type | Procedure | Expected output |
|---|---|---|---|
| S01 | STATIC CHECK | `python tools/validate_plan.py` | No IPv4/IPv6 address overlaps |
| S02 | STATIC CHECK | `python tools/build_lab.py` | 12 enterprise + 2 ISP configs, 4 GRE/IPsec tunnel pairs, DHCP config |
| S03 | STATIC CHECK | `python -m pytest -q` | All Python unit tests pass |
| S04 | STATIC CHECK | `python tools/generate_topology.py` | `.drawio` file opens and editable topology appears |
| S05 | STATIC CHECK | Run automation with fake devices (`test_idempotency_and_backup_files`) | First run applies changes; second run makes none |
| S06 | STATIC CHECK | Run automation with injected connection failure (`test_error_handling_does_not_abort_next_device`) | Error logged; unaffected next device processed |

## B. Network Layer 2 tests

| ID | Type | Source | Command / action | Expected result |
|---|---|---|---|---|
| L01 | LAB REQUIRED | HCMC-SW1 | `show vlan brief` | VLAN 10,20,30,50,60,70,80,99,999 present; access ports correct |
| L02 | LAB REQUIRED | HANOI-SW1 | `show interfaces trunk` | Gi0/0 and Po1 trunk, 802.1Q VLANs carried |
| L03 | LAB REQUIRED | Each SW1/SW2 | `show etherchannel summary` | Po1(SU) and both Gi member interfaces `(P)` |
| L04 | LAB REQUIRED | SW1/SW2 | `show spanning-tree root` | SW1 is primary root for intended VLANs, SW2 secondary |
| L05 | LAB REQUIRED | HANOI-SW1 | Shut one of Gi0/1 or Gi0/2 *within Port-channel1* | Port-channel remains up via surviving member; re-enable afterward |
| L06 | LAB REQUIRED | SW1 | `show ip dhcp snooping` / `show ip arp inspection` | Required VLANs and trusted uplinks configured |
| L07 | LAB REQUIRED | SW1 | Plug untrusted rogue DHCP server into a test access port | Rogue DHCP offers blocked; legitimate HQ DHCP still functions |
| L08 | LAB REQUIRED | Each access switch | Run show port-security interface Gi0/3 and connect a second unauthorized MAC on an isolated test port | Port Security enabled, maximum 2, violation restrict; violation counter increments without shutting the port |
| L09 | LAB REQUIRED | Each access switch | Run show port-security address and show port-security | Sticky secure MAC addresses are learned on intended endpoint ports; trunks/uplinks are not configured as access-port security |

## C. Routing, IPv6, redundancy

| ID | Type | Source | Command / action | Expected result |
|---|---|---|---|---|
| R01 | LAB REQUIRED | HCMC-R1 | `show ip ospf neighbor` | Neighbor HCMC-R2 reaches FULL |
| R02 | LAB REQUIRED | HANOI-R2 | `show ip route ospf` | OSPF-learned loopback and relevant other-router site routes when present |
| R03 | LAB REQUIRED | HCMC-R1 | `ping 10.20.99.11 source 10.10.99.2` | Success after BGP/IPsec and LAN come up |
| R04 | LAB REQUIRED | HCMC-R1 | `show ip bgp summary` | ISP-A, HANOI tunnel, DANANG tunnel, iBGP R2 peers established (numeric PfxRcd) |
| R05 | LAB REQUIRED | HCMC-R2 | `show ip bgp summary` | ISP-B, HANOI tunnel, DANANG tunnel, iBGP R1 peers established |
| R06 | LAB REQUIRED | Branch-R1 | `show crypto isakmp sa` / `show crypto ipsec sa` | SA present; counters increment following cross-site traffic |
| R07 | LAB REQUIRED | HCMC-R1 | `show bgp ipv6 unicast summary` | IPv6 tunnel/iBGP peers established (image-specific CLI) |
| R08 | LAB REQUIRED | HCMC-R1 | `ping ipv6 2001:db8:20:99::2` | IPv6 reply from HANOI-R1 VLAN99 subinterface (requires IPv6 BGP over GRE/IPsec) |
| R09 | LAB REQUIRED | Each R1/R2 | `show standby brief` | R1 Active, R2 Standby normally; virtual gateway `.1` |
| R10 | LAB REQUIRED | HANOI-R1 | `interface GigabitEthernet0/1` → `shutdown`; continuous client ping to HQ | HSRP R2 takes over; reachability returns over B tunnel and ISP-B within the demo budget |
| R11 | LAB REQUIRED | HANOI-R1 | `no shutdown` on G0/1 | Original primary reclaims role via preempt after restoration |
| R12 | LAB REQUIRED | HCMC-R1 | `show ip route 10.30.99.11` | Overlay-learned route to Da Nang, not default to ISP |

**IPv6 note:** The switch management SVIs in this lab are IPv4-only; use IPv6 router subinterfaces as IPv6 ping destinations until you configure IPv6 SVIs. The address `2001:db8:20:99::2` belongs to HANOI-R1.

## D. Central IP services and security

| ID | Type | Source | Command / action | Expected result |
|---|---|---|---|---|
| D01 | LAB REQUIRED | HCMC-CORP-CLIENT | `ip dhcp` (VPCS) | IP within `10.10.8.0/22`, gateway `10.10.8.1`, HQ DNS `10.10.60.10` |
| D02 | LAB REQUIRED | HANOI-CORP-CLIENT | `ip dhcp` | IP within `10.20.16.0/21`, gateway `10.20.16.1`, HQ DNS `10.10.60.10` |
| D03 | LAB REQUIRED | DANANG-CORP-CLIENT | `ip dhcp` | IP within `10.30.32.0/22`, gateway `10.30.32.1`, HQ DNS `10.10.60.10` |
| D04 | LAB REQUIRED | HANOI-GUEST-CLIENT | `ip dhcp` | IP within `10.20.50.0/24`, DNS `192.0.2.18`, gateway `10.20.50.1` |
| D05 | LAB REQUIRED | HANOI-GUEST-CLIENT | `ping 10.10.60.10` | **Blocked** by Guest IPv4 ACL |
| D06 | LAB REQUIRED | HANOI-GUEST-CLIENT | `ping 192.0.2.18` | **Allowed**, with NAT/PAT translation at the branch edge |
| D07 | LAB REQUIRED | HANOI-R1 | `show ip nat translations` after D06 | Inside local `10.20.50.x` translated to WAN outside address `198.51.100.6` (or R2 `203.0.113.6` if failover) |
| D08 | LAB REQUIRED | Internet test Linux | `curl -s http://192.0.2.18/` from corp/guest Linux client | `TVI TEST INTERNET SERVICE OK` |
| D09 | LAB REQUIRED | HCMC DNS Linux | `dig @10.10.60.10 inventory.tvi.lab` | Resolves `10.10.60.20` |
| D10 | LAB REQUIRED | Branch IoT client | Ping/telnet to unauthorized executive IP (`10.10.8.x`) | **Blocked** by IoT ACL; `curl http://10.10.60.20:8080/` should succeed from the IoT client |
| D11 | LAB REQUIRED | Branch Guest IPv6 client | `ping -6 2001:db8:10:10::2` | **Blocked** by IPv6 Guest ACL |
| D12 | LAB REQUIRED | HCMC-R1 | `show access-lists` and `show ipv6 access-list` | Deny counters increase during rejected guest/IoT tests |
| D13 | LAB REQUIRED | Untrusted access switchport | Attempt ARP spoofing from a separate authorized test machine | DAI drops invalid ARP after DHCP snooping bindings exist; do this only inside isolated lab |

## E. QoS, automation, and live demonstration

| ID | Type | Action | Expected result |
|---|---|---|---|
| Q01 | LAB REQUIRED | Create marked EF traffic from voice VLAN; generate WAN congestion; inspect `show policy-map interface GigabitEthernet0/1` | Voice class counter increases and policy prioritizes EF where IOS applies policy before encapsulation; document crypto/QoS interaction |
| Q02 | LAB REQUIRED | Generate AF31-marked video traffic | AF31 class matches and configured bandwidth treatment appears |
| A01 | LAB REQUIRED | `python automation/auto_provision.py --only HCMC-SW1` | No SSH failure, snapshots saved, VLAN 140 created, success log |
| A02 | LAB REQUIRED | Repeat A01 unchanged | `Applied 0 config commands`, demonstrating idempotency |
| A03 | LAB REQUIRED | Disconnect HANOI-SW1 management interface and run full automation | One failure logged, other nodes still processed |
| A04 | LAB REQUIRED | `python tools/verify_live.py` | JSON and text evidence generated; failed/unknown checks reviewed manually |
| F01 | LAB REQUIRED | Controlled shutdown of primary WAN `Gi0/1` on HANOI-R1 while sending continuous pings | Convergence and end-to-end return via backup path within 3 minutes; include times and packet-loss measurement |
| F02 | LAB REQUIRED | Restore primary interface; repeat ping | Expected primary path and gateway role restored |

### Recommended evidence capture

For each case record **Case ID, date/time, device/source, exact command, expected result, actual result, PASS/FAIL, screenshot or CLI output file, and any troubleshooting**. Put results in the PDF report appendix. Every `LAB REQUIRED` case is **pending until personally observed** in the actual emulation environment.

**Known scope gaps:** No full EVPN-VXLAN spine/leaf fabric; no vendor SD-WAN orchestrator, WLC/CAPWAP, NGFW, or real ZTNA provider; no true 40 Gbps throughput/99.99% uptime certification. Explain these honestly during evaluation and agree a graded minimum with the lecturer.
