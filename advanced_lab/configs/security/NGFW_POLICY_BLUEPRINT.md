# TVI NGFW policy blueprint

This is the policy specification for a dedicated NGFW appliance. The
existing IOS ACLs and optional IOS Zone-Based Firewall are retained as the
core fallback; they are not described as a dedicated NGFW.

## Interface/zone model

| Zone | Connected networks | Default policy |
|---|---|---|
| TRUST | Corporate application and server networks | Allow explicitly approved business flows |
| GUEST | VLAN 50 / advanced guest segment | Internet only; deny private networks |
| IOT | VLAN 70 | DNS/NTP and approved IoT application only |
| DMZ | Published connector/application subnet | No direct initiation into TRUST |
| UNTRUST | ISP/transit links | Deny unsolicited inbound |
| MGMT | Management subnet | Admin protocols only from approved admin hosts |

## Rule order (top to bottom)

1. Allow established/related return traffic (state table).
2. Allow MGMT-to-firewall administration from the designated admin subnet.
3. Allow TRUST to approved DNS, NTP, application and Internet destinations.
4. Allow GUEST to approved public DNS and Internet; deny RFC1918/private ranges.
5. Allow IOT to the inventory application and required DNS/NTP only.
6. Allow DMZ connector to its named private application and required identity
   endpoints only.
7. Deny and log all other inter-zone traffic.
8. Deny unsolicited UNTRUST-to-TRUST and UNTRUST-to-MGMT traffic.

## Required appliance configuration

Before writing vendor CLI/XML, select the exact NGFW product and release.
Create interfaces/VLANs, zones, aliases/address groups, service groups,
stateful rules, NAT, logging, admin-plane restrictions and backup/rollback.
Enable IPS/application control only when the selected licensed image supports
the feature and its signatures can be updated.

## Safe deployment order

1. Deploy firewall off-path with console access and a saved configuration.
2. Add interface addressing and static/dynamic routes.
3. Add zone and policy objects; keep a final deny/log rule.
4. Test each positive and negative flow from isolated test clients.
5. Insert firewall into the lab path only after policies pass.
6. Confirm routing, VPN and management access; retain an immediate rollback.

## Acceptance

Use tests D01-D05 in `advanced_lab/docs/acceptance_tests.md`. Include the
firewall model/version, policy export, session table and deny/allow logs.
Do not claim NGFW deployment from an ACL or policy spreadsheet alone.
