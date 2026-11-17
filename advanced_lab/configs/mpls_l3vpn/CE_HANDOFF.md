# MPLS L3VPN customer-edge handoff

The provider uses dedicated /30 CE-PE handoffs. They do not reuse the core
lab's ISP /30s or replace its GRE/IPsec overlay.

| Site | PE interface address | CE interface address | CE AS | Test loopback |
|---|---|---|---|---|
| HCMC | 10.43.0.1/30 | 10.43.0.2/30 | 65010 | 10.10.250.1/32 |
| Hanoi | 10.43.0.5/30 | 10.43.0.6/30 | 65020 | 10.20.250.1/32 |
| Da Nang | 10.43.0.9/30 | 10.43.0.10/30 | 65030 | 10.30.250.1/32 |

## Exact device files

- HCMC: `CE-HCMC.cfg` connects to `PE-HCMC.cfg`.
- Hanoi: `CE-HANOI.cfg` connects to `PE-HANOI.cfg`.
- Da Nang: `CE-DANANG.cfg` connects to `PE-DANANG.cfg`.

Each CE advertises its site /16 summary and a dedicated Loopback100 test
prefix through eBGP to its local PE. The /16 Null0 route is a lab-only
aggregate advertisement anchor. The more-specific Loopback100 prefix is
used for an end-to-end routed test. Do not use these Null0 aggregates as a
substitute for real site routes in production.

## Physical/logical wiring

| Link | Device A | Interface A | Device B | Interface B | Subnet |
|---|---|---|---|---|---|
| Provider core | PE-HCMC | Gi0/0 | P1 | Gi0/0 | 10.41.0.0/31 |
| Provider core | P1 | Gi0/1 | P2 | Gi0/0 | 10.41.0.2/31 |
| Provider core | P2 | Gi0/1 | PE-HANOI | Gi0/0 | 10.41.0.4/31 |
| Provider core | P2 | Gi0/2 | PE-DANANG | Gi0/0 | 10.41.0.6/31 |
| Customer handoff | PE-HCMC | Gi0/1 | CE-HCMC | Gi0/0 | 10.43.0.0/30 |
| Customer handoff | PE-HANOI | Gi0/1 | CE-HANOI | Gi0/0 | 10.43.0.4/30 |
| Customer handoff | PE-DANANG | Gi0/1 | CE-DANANG | Gi0/0 | 10.43.0.8/30 |

## Bring-up order

1. Cable the seven point-to-point links exactly as above.
2. Apply P1/P2 and PE configurations. Confirm provider OSPF neighbors and
   loopback reachability before checking LDP.
3. Confirm LDP sessions and label bindings on all provider-facing links.
4. Apply the three CE configs and confirm each PE-CE eBGP session.
5. Confirm PE-to-PE VPNv4 sessions and the `TVI_ENTERPRISE` VRF routes.
6. Ping between CE Loopback100 addresses to validate the VPN data plane.

## Verification commands

Provider routers:
```text
show ip ospf neighbor
show mpls ldp neighbor
show mpls forwarding-table
show ip route 10.41.250.11
```

PE routers:
```text
show ip bgp vpnv4 all summary
show ip route vrf TVI_ENTERPRISE
show ip bgp vpnv4 vrf TVI_ENTERPRISE
show ip bgp summary
```

CE routers:
```text
show ip bgp summary
show ip route bgp
ping 10.20.250.1 source Loopback100
```

Run the ping from each CE to the other two site loopbacks. A successful
control-plane session alone is not enough; the sourced ping must pass.

## Platform caveats

The configs use classic IOS/IOS-XE `ip vrf` syntax for broad CSR1000v
compatibility. Some IOS-XE releases prefer `vrf definition`; translate
consistently if required by the selected image. Interface numbering must
match the emulated router model. Verify feature support for MPLS, LDP,
VPNv4 and VRF before building the lab.
