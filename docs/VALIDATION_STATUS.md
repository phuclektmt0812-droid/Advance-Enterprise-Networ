# Validation Results — 13 November 2026

## Update — 17 November 2026

The GWork branch has since been extended with:
- AAA local authentication baseline in generated device configurations.
- Sticky access-port Port Security (maximum two MAC addresses, violation restrict).
- A test assertion for endpoint ports remaining untrusted for DHCP Snooping/DAI.
- Live verification collection for Port Security interface state.
- Editable physical topology diagram and physical placement notes.
- An opt-in IOSv Zone-Based Firewall template with pre-check and rollback guidance.
- An enterprise extension/compliance register for EVPN-VXLAN, SD-WAN, MPLS,
  NGFW, ZTNA/SASE and WLC/CAPWAP.
- GitHub Actions static validation workflow.

**Latest static CI — 17 November 2026, commit 9d40d380048dc04f7a6af3f102341a0b2da72f89: PASS.**
GitHub Actions completed the following steps successfully:
- python tools/validate_plan.py
- python tools/build_lab.py (12 enterprise configs, 2 ISP configs, 4 GRE/IPsec tunnel pairs)
- python -m pytest -q — **23 passed**
- python -m compileall -q tools automation
- bash -n server/prepare_hq_server.sh server/prepare_internet_server.sh

Workflow evidence: https://github.com/phuclektmt0812-droid/Advance-Enterprise-Networ/actions/runs/44018635167

This is static CI on Ubuntu, not a run on the user's Windows machine or on
live IOSv/IOSvL2 devices. The emulator/runtime checks below remain pending.

## What was actually checked in this environment

- `python tools/validate_plan.py` — **PASS**: IPv4 VLANs, loopback/link and GRE tunnels do not overlap; IPv6 VLAN/tunnel prefixes do not overlap.
- `python tools/build_lab.py` — **PASS**: Generated **12 enterprise network device configurations** (6 routers + 6 switches), **2 ISP router configurations**, **4 IPsec-over-GRE tunnel pairs**, full router/switch console bootstrap files, a YAML automation inventory, CSV addressing/cabling tables, and a centralized dnsmasq configuration.
- `python tools/generate_topology.py` — **PASS**: Generated editable Draw.io topology and SVG.
- `python tools/render_report_diagram.py` — **PASS**: Generated report graphics.
- `pytest -q` — **PASS: 22 local tests** covering subnet overlaps, addressing size, expected routing/service features, HSRP preemption, VLAN names, safe CLI mode transitions, Draw.io XML, mocked Netmiko provisioning, backup creation, idempotency, and injected SSH failure handling.
- `python -m compileall -q tools automation` — **PASS** (Python syntax).
- `bash -n server/prepare_hq_server.sh server/prepare_internet_server.sh` — **PASS** (shell syntax).
- Report conversion to PDF with XeLaTeX/Pandoc — **PASS**; the draft PDF was rendered to images for layout review.

## What was NOT tested (must be done in GNS3/EVE-NG)

- Whether any particular licensed IOSv/IOSvL2 image accepts every configuration statement.
- Whether OSPF and IPv6 OSPF neighbors reach FULL.
- Whether ISP eBGP, enterprise iBGP and GRE/IPsec eBGP reach Established.
- Whether GRE/IPsec tunnels negotiate SAs and forward IPv4/IPv6 traffic.
- Whether client DHCP relays at Hanoi and Da Nang work end-to-end to HCMC Linux dnsmasq.
- Whether ACLs block Guest/IoT traffic, including real client IPv6 behavior.
- Whether edge PAT translates addresses/ports and real HTTP works.
- Whether QoS counters show appropriate policy behavior under congestion.
- Whether HSRP/LACP failover and restoration pass under a measured 3-minute convergence threshold.
- Whether physical traffic capacity meets 10/40 Gbps or annual availability reaches 99.99%.

**Conclusion:** This is a code-complete **core lab candidate**, not a verified running enterprise network. Do not submit the draft report as proof of testing; attach actual device evidence and correct any platform-specific syntax errors.

## Explicitly unimplemented production features

Controller-based SD-WAN, EVPN-VXLAN spine-and-leaf, vendor NGFW, true ZTNA/SASE, and WLC/CAPWAP Wi-Fi infrastructure are not deployed. The assignment's requirements name them, but reproducing them requires compatible images, product licenses, additional nodes, and instructor agreement on lab scope.

## Advance-GWork advanced extension — 17 November 2026

A separate advanced-lab pack has been added under `advanced_lab/` without
changing the core generator or its 14-device topology. It includes a topology
manifest, address pools, staged designs/configuration skeletons for EVPN-VXLAN
and MPLS L3VPN, implementation plans for SD-WAN, NGFW, ZTNA/SASE and
WLC/CAPWAP, acceptance tests, and a static manifest validator.

**Validation status:** the advanced manifest and new tests have been added to
the GitHub Actions workflow for the `Advance-GWork` branch. A passing CI run
for this branch has not yet been confirmed. Run
`python tools/validate_advanced_lab.py` and `python -m pytest -q` locally,
or inspect the branch's Actions run before treating the static checks as PASS.

No advanced feature has been validated on live vendor images or controllers.


## Advance-GWork implementation additions — 17 November 2026

Added implementation artifacts on the separate `Advance-GWork` branch:
- `advanced_lab/configs/evpn_vxlan/DEVICE_CONFIGS.md`: two-spine/two-leaf
  Arista EOS starter, routed OSPF underlay, MP-BGP EVPN route reflection,
  Vxlan1 and VLAN-to-VNI mappings.
- `advanced_lab/configs/mpls_l3vpn/DEVICE_CONFIGS.md`: IOS-XE PE/P examples,
  OSPF underlay, LDP, VPNv4 MP-BGP and customer VRF/route-target plan.
- `advanced_lab/configs/sdwan/IMPLEMENTATION_RUNBOOK.md`: controller,
  onboarding, dual transport and application-aware policy workflow.
- `advanced_lab/configs/security/NGFW_POLICY_BLUEPRINT.md`: zone model,
  stateful allow/deny rules, logging and safe insertion order.
- `advanced_lab/configs/ztna/OPENZITI_REFERENCE.md`: named private application,
  identity/service policy and no broad subnet exposure.
- `advanced_lab/configs/wireless/CISCO_9800_REFERENCE.txt`: WLC/AP join,
  CAPWAP discovery, SSID-to-VLAN and guest isolation workflow.
- `docs/config_templates/IOS_QOS_VOICE_VIDEO.txt`: documents the QoS policy
  already emitted by the core generator and how to verify class counters.

A new test file checks the presence and key configuration elements of these
artifacts. The existing core generator and 14-device topology are unchanged.

**Important limits:** The EVPN and MPLS files are platform-specific starter
configurations and require licensed feature-capable images plus final interface
mapping. SD-WAN requires a vendor controller/edge stack; NGFW requires a
selected firewall appliance; ZTNA requires a controller/connector deployment;
wireless requires a compatible WLC and lightweight AP. These artifacts are
implementation-ready design/configuration references, not proof of a running
advanced lab. 10/40-Gbps capacity and 99.99% availability measurements remain
intentionally out of scope for this pass.


## Latest Advance-GWork static CI — 17 November 2026

**PASS** on branch head `cfb4eb6728ef1b32c1f8e8c31c905eac6a4d8e3d`.
Workflow: https://github.com/phuclektmt0812-droid/Advance-Enterprise-Networ/actions/runs/44026389689

- Core IPv4 plan validation — PASS.
- Advanced manifest validation — PASS.
- Core config generation — PASS (12 enterprise + 2 provider configs).
- Pytest — **32 passed**.
- Python compileall — PASS.
- Linux service shell syntax — PASS.

This is static CI only. The EOS/IOS-XE/OPNsense/SD-WAN/WLC/ZTNA stages have
not been booted as virtual appliances in this CI run. The branch now includes
a runnable minimum configuration set for EVPN (2 spines + 2 leaves) and
MPLS L3VPN (P/PE plus CE handoff examples), while controller- and
appliance-dependent stages remain platform setup guides. Actual image
compatibility and end-to-end traffic still require the user's emulator lab.
