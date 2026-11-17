# OPNsense NGFW-style lab deployment guide

This is a practical open-source firewall option for the teaching lab. It
demonstrates stateful zone policy, NAT, logging and IDS/IPS integration. It
is **not equivalent to every commercial NGFW feature** (vendor threat
intelligence, sandboxing and licensed application inspection may differ).

## Minimum topology

- OPNsense VM with 4 virtual NICs.
- NIC1: WAN / UNTRUST (connect to isolated lab transit).
- NIC2: TRUST (corporate/service network).
- NIC3: GUEST.
- NIC4: DMZ / connector segment.
- Add an IOT VLAN/interface if the virtual NIC and switch trunk design
  supports VLAN tagging.
- Keep the OPNsense web administration interface reachable only from
  the management segment.

Do not connect this lab WAN to an untrusted public network with default
credentials or unreviewed rules. Use an isolated EVE-NG/GNS3 network.

## Interface plan

Use a dedicated non-overlapping subnet from 10.43.0.0/16 for each interface.
Example:
- TRUST: 10.43.30.1/24
- GUEST: 10.43.40.1/24
- DMZ: 10.43.50.1/24
- IOT: 10.43.60.1/24

These are example firewall-segment networks; coordinate them with the final
manifest before connecting them to another router. Do not reuse the core
10.10/16, 10.20/16 or 10.30/16 address blocks.

## GUI implementation sequence

1. Install OPNsense from its official image and assign the four NICs to
   WAN/TRUST/GUEST/DMZ. Rename interfaces clearly.
2. Set interface IPs and gateway. Disable administration from WAN.
3. Create aliases for corporate networks, guest networks, IoT devices,
   approved DNS/NTP servers, DMZ applications and management hosts.
4. Under Firewall > Rules, add rules in this order on each interface:
   - TRUST: allow required DNS/NTP and approved business destinations;
     allow approved outbound traffic; log denies.
   - GUEST: allow DNS and Internet only; explicitly block RFC1918/private
     destination ranges before the general Internet allow.
   - IOT: allow DNS/NTP and the inventory application TCP/8080 only; block
     other private destinations; allow only required outbound services.
   - DMZ: allow the connector to its named private application and required
     identity endpoints; block DMZ-initiated access to other TRUST hosts.
   - WAN: deny unsolicited inbound by default; add only explicit published
     service rules if the lab requires them.
5. Configure outbound NAT using the WAN interface address.
6. Enable logging on allow/deny rules needed for evidence.
7. Install and configure the supported IDS/IPS plugin (Suricata where
   available for the selected release); start in IDS/alert-only mode first.
8. Review alerts, tune false positives, then enable inline blocking only
   after confirming that management and required lab traffic still work.
9. Export a sanitized configuration backup.

## Required tests

- TRUST client can reach only approved internal services and permitted
  outbound destinations.
- GUEST client can reach the simulated Internet but cannot reach any
  10.0.0.0/8 or other private enterprise subnet.
- IOT client can reach DNS/NTP and the named inventory service only.
- DMZ connector cannot initiate arbitrary sessions into TRUST.
- Unsolicited inbound WAN traffic is denied and logged.
- IDS events appear for a controlled benign test signature.

## Rollback

Keep console access. Before inserting OPNsense inline, save its configuration
and record the original cable path. If routing or management fails, disconnect
the firewall and restore the original direct lab connection. Never remove the
last management allow rule during a remote-only session.
