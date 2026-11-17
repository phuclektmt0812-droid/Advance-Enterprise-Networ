# TechViet Innovations (TVI) — Enterprise Network Lab

**Assignment 2: Advanced Enterprise Network Design & Implementation**  
GNS3 / EVE-NG Cisco IOSv + IOSvL2 project, with Python Netmiko automation, test cases, and a report draft.

> **Status:** The address plan and generated configuration structure have been tested in Python. **No Cisco IOSv or IOSvL2 virtual devices are available in this environment**, so the actual networking CLI, tunnel formation, WAN failover, DHCP relay, QoS counters, and end-to-end packet forwarding **have not been validated on real images**. You must run the live tests below. Some commands may need adjustment for your licensed image release.
>
> This implements a demonstrable *core 10-step lab*, not a full production deployment of managed SD-WAN, SASE/ZTNA, NGFW, WLC/CAPWAP, or an EVPN-VXLAN spine/leaf fabric. These are addressed in the architecture/report as scope gaps. Confirm what your lecturer expects before submission.

## 1. Prerequisites

- **GNS3 with GNS3 VM**, or **EVE-NG**, with working virtual acceleration (VT-x/AMD-V).
- Cisco IOSv **L3 router** images (8 instances: 6 enterprise + 2 ISP).
- Cisco IOSvL2 **switch** images (6 instances), with **8 or more GigabitEthernet0/x** ports for SW1.
- Two Ubuntu minimal/Linux service hosts for `HQ-DHCP-DNS` and `INTERNET-TEST`.
- A third Linux host for **automation**, with Python 3.10+; can be your Windows PC when its routing to `10.x` management ranges is available.
- Six VPCS or Linux client instances (one corp + one guest per site); optionally additional IoT/Voice clients.
- Recommended >=32 GB host RAM, >=8 CPU cores, SSD storage. The 16 GB stated in the assignment is a *minimum* and this 22+ node project may exceed it if everything is started simultaneously.
- Windows/Linux Python 3.10+ and `pip`. Validly licensed network images must be sourced separately.

**Important:** Vendor image names and NIC enumeration vary. The generated device configs target `GigabitEthernet0/0` through `GigabitEthernet0/7`. Confirm ports with `show ip interface brief` or `show interfaces status` and adapt the configs when using a different image.

## 2. Project files

| Path | Purpose |
|---|---|
| `network_plan.yaml` | Source of truth for 3 site blocks, VLSM VLANs, WAN IPs, GRE/IPsec tunnels |
| `tools/validate_plan.py` | Checks address allocations and overlaps |
| `tools/build_lab.py` | Generates IOS router/switch config + auto inventory + dnsmasq + IP schema |
| `tools/generate_topology.py` | Generates editable Draw.io network diagram and SVG |
| `build/Configurations/` | **Generated 14 Cisco configs** and `.bootstrap.txt` console paste scripts |
| `build/services/dnsmasq.conf` | Central DHCP/DNS pools for all three sites |
| `build/secrets.local.env` | Auto-generated disposable lab-only SSH credentials and IPsec key |
| `automation/auto_provision.py` | Step 9 Netmiko automated baseline/VLANs/backup/logging |
| `automation/inventory.yaml` | Device roles, management addresses, ports |
| `automation/vlans.yaml` | VLAN payload; VLAN 140 is added to demonstrate a real automation change |
| `tools/verify_live.py` | SSH-based read-only evidence capture; *not a substitute for manual checks* |
| `server/` | Ubuntu scripts for real DHCP/DNS, local NTP/syslog, test HTTP server |
| `docs/interface_matrix.csv` | Exact virtual device interfaces and cables |
| `docs/ip_schema.csv` | IPv4 VLSM and IPv6 site/VLAN plan |
| `docs/TVI_Logical_Topology.drawio` | Editable logical topology file for draw.io |
| `docs/TVI_Physical_Topology.drawio` | Editable physical topology / site equipment placement |
| `docs/physical_topology.md` | Physical placement, WAN demarcation and resiliency notes |
| `docs/enterprise_extensions.md` | Requirement-by-requirement compliance register and extension architecture |
| `docs/config_templates/IOSv_Zone_Based_Firewall_OPTIONAL.txt` | Opt-in stateful firewall template; not in default bootstrap |
| `docs/testcases.md` | Manual and automated tests with expected results |
| `docs/demo_script.md` | 15-minute lecturer demonstration plan |
| `docs/Technical_Explanation_Report_DRAFT.md` | Report draft; real test evidence must be added |
| `tests/` | Self-contained pytest suite (mocked automation + design checks) |

## 3. Set up Python and VS Code (Windows)

The repository supports Python 3.10+. For the simplest Windows setup, use
**64-bit CPython 3.12** from python.org rather than an MSYS2/MinGW Python
build. The latter can require platform-specific compiled packages, especially
for Paramiko/Cryptography. Do not install a second interpreter if your current
interpreter already works.

1. Install Python 3.12 (64-bit) and select **Add Python to PATH** in the
   installer. Install the Microsoft **Python** extension in VS Code.
2. Clone this repository and check out the `Advance-GWork` branch.
3. Open the repository root folder in VS Code.
4. Open **Terminal → New Terminal** and use PowerShell:

```powershell
py -3.12 --version
py -3.12 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip check
```

5. In VS Code press **Ctrl+Shift+P**, choose **Python: Select Interpreter**,
   and select the interpreter inside this repository's `.venv` folder.
6. Run the complete local test suite:

```powershell
python -m pytest -v
```

7. Run the project validators and generate the core lab configuration:

```powershell
python tools/validate_plan.py
python tools/validate_advanced_lab.py
python tools/build_lab.py
python tools/generate_topology.py
```

The Python dependencies are declared in `requirements.txt`:
- `netmiko`: SSH automation of Cisco IOS devices.
- `PyYAML`: reads the network plan, inventory and VLAN data.
- `pytest`: runs the automated tests.

Pip installs Netmiko's runtime dependencies as well (including Paramiko,
Cryptography, PySerial, TextFSM, NTC Templates, Rich and SCP). On a normal
64-bit CPython Windows installation, install the complete set with
`python -m pip install -r requirements.txt`; do not install these packages
one by one unless pip reports a specific failure.

**Important distinction:** `python -m pytest -v` runs local tests with mocked
network connections. It does not require GNS3 and does not connect to routers.
A successful test run validates the Python logic, not the live network.

For a more detailed Windows walkthrough and the separate live-lab procedure,
see [docs/SETUP_WINDOWS_VSCODE.md](docs/SETUP_WINDOWS_VSCODE.md).

## 4. Create and wire nodes

1. Open `docs/TVI_Logical_Topology.drawio` in [diagrams.net](https://app.diagrams.net/) to see the architecture.
2. Create **8 IOSv routers** named `HCMC-R1/R2`, `HANOI-R1/R2`, `DANANG-R1/R2`, `ISP-A/B`.
3. Create **6 IOSvL2 switches** named `HCMC-SW1/SW2`, `HANOI-SW1/SW2`, `DANANG-SW1/SW2`.
4. Create Linux `HQ-DHCP-DNS`, `INTERNET-TEST`, and `AUTOMATION` nodes.
5. Create `HCMC-CORP-CLIENT`, `HCMC-GUEST-CLIENT`, `HANOI-CORP-CLIENT`, `HANOI-GUEST-CLIENT`, `DANANG-CORP-CLIENT`, and `DANANG-GUEST-CLIENT`.
6. **Wire every link exactly as listed in `docs/interface_matrix.csv`.** ISP-A must expose `GigabitEthernet0/4`, and enterprise SW1 devices must expose `GigabitEthernet0/7`. The WAN tunnels are *logical*, not extra cables.
7. Add optional IoT endpoints on site SW1 `Gi0/6` and voice endpoints on SW1 `Gi0/7`; those access ports are preconfigured.

**Cable summary:**

- Every R1 `Gi0/0` -> SW1 `Gi0/0`; every R2 `Gi0/0` -> SW2 `Gi0/0` (802.1Q).
- Same-site R1 `Gi0/2` <-> R2 `Gi0/2` (OSPF + iBGP transit).
- SW1 `Gi0/1,Gi0/2` <-> SW2 `Gi0/1,Gi0/2`, one-to-one (LACP Port-channel 1).
- Site R1 `Gi0/1` -> ISP-A ports `Gi0/0` HCMC, `Gi0/1` Hanoi, `Gi0/2` Da Nang.
- Site R2 `Gi0/1` -> ISP-B ports `Gi0/0` HCMC, `Gi0/1` Hanoi, `Gi0/2` Da Nang.
- ISP-A `Gi0/3` <-> ISP-B `Gi0/3`; ISP-A `Gi0/4` -> `INTERNET-TEST` eth0.
- HQ DNS `eth0` -> HCMC-SW1 `Gi0/4`; automation `eth0` -> HCMC-SW1 `Gi0/5`.

## 5. Load router and switch CLI configurations

From the GNS3/EVE-NG **console** of each device:

1. Wait until IOS has fully booted. If it asks for a configuration dialog, select `no`.
2. Use its corresponding `build/Configurations/<SITE>/<HOSTNAME>.bootstrap.txt` file. Paste the complete file into the IOS console *with a paste delay if your console drops commands*.
3. The file enters enable/config mode, creates network policies, exits to privileged EXEC, generates an RSA key, and saves to NVRAM.
4. Check for CLI errors (`% Invalid input`, `Incomplete command`) rather than assuming that the paste succeeded. Vendor image feature sets differ.
5. Repeat for all 14 network devices. When the file ends, run `show running-config`, `show ip interface brief`, `show ip bgp summary`, and `show standby brief` on relevant nodes.
6. Generated `*.cfg` files are also included for reference. They explicitly close configuration submodes with `exit` to make them pasteable in a console.

The RSA key is generated *inside the device*. It cannot simply be supplied in a vendor-neutral static config. Re-run `crypto key generate rsa modulus 2048` only when necessary; some IOS images will ask to replace an existing key.

## 6. Configure the Linux service nodes

Both scripts assume Ubuntu/Debian and interface **`eth0`**, and must be run from their **console**, not over SSH (they replace the default route). If your interface is `ens3`, adjust the `eth0` references first.

On `HQ-DHCP-DNS`:

```bash
sudo bash server/prepare_hq_server.sh
```

This configures `10.10.60.10/24`, gateway `10.10.60.1`, installs **dnsmasq**, provides **central DHCP/DNS**, **chrony NTP**, a basic IoT inventory HTTP service on `10.10.60.20:8080`, and an **rsyslog UDP 514 receiver** for device logs. The DHCP ranges are generated from all sites in the network plan. Verify DHCP and DNS with `systemctl status dnsmasq`, `journalctl -u dnsmasq`, and `dig @10.10.60.10 inventory.tvi.lab`.

On `INTERNET-TEST`:

```bash
sudo bash server/prepare_internet_server.sh
```

It configures `192.0.2.18/30`, gateway `192.0.2.17`, local DNS for `internet.tvi.lab`, and an HTTP service on TCP/80. **This is a simulated internet host, not the real global Internet.**

On `AUTOMATION` Linux host:

```bash
sudo ip link set eth0 up
sudo ip addr add 10.10.99.50/24 dev eth0
sudo ip route replace default via 10.10.99.1 dev eth0
python -m pip install -r requirements.txt
```

Place/copy the project folder on the automation host, or give another SSH-capable machine a route to `10.10.99.50` and branch management networks. Open `build/secrets.local.env` locally and use its username/password **only in this isolated lab**.

## 7. First real checks before running automation

- Check all router LAN and WAN interfaces are `up/up`: `show ip interface brief`.
- Check LACP: `show etherchannel summary` should show Port-channel1 bundled and member links `(P)`.
- Check STP: `show spanning-tree root` (SW1 expected primary in each site).
- Check HSRP: `show standby brief` (R1 normally active, R2 standby).
- Check OSPF R1-R2: `show ip ospf neighbor` should show FULL.
- Check BGP: `show ip bgp summary` should show *established* IPv4 peers (numeric PfxRcd); check IPv6 address-family separately.
- Check GRE/IPsec: `show interfaces tunnel 10` or `11/20/21`, plus `show crypto isakmp sa` and `show crypto ipsec sa`.
- Check DHCP at a client. In VPCS: `ip dhcp` then `show ip`. Branch DHCP will not work until IPsec/BGP paths reach HQ.
- Check management reachability from AUTOMATION to all enterprise management addresses in `automation/inventory.yaml`.

## 8. Run network automation (Step 9)

```bash
python automation/auto_provision.py
```

It prompts for SSH username/password (unless `TVI_USERNAME`/`TVI_PASSWORD` are provided via environment variables). It connects to **12 enterprise routers and switches** (not ISP devices), captures `show running-config` and `show ip interface brief` both before and after changes, configures missing AAA/NTP/Syslog/banner settings, and dynamically provisions VLANs 10/20/30/99 and demo VLAN 140 **on switches only**. It saves snapshots in `build/automation_results/backups/`, and error/success events in `build/automation_results/logs/automation.log`.

**Repeat the exact command.** The second run should report zero configuration changes if all desired state is already present. If a node is disconnected, the script logs an error and continues to the next node. Running on partially configured nodes does not create the actual underlay/overlay; load and test base configs first.

To target a single switch:

```bash
python automation/auto_provision.py --only HCMC-SW1
```

## 9. Run verification and collect evidence

```bash
python -m pytest -q
python tools/verify_live.py
python tools/verify_live.py --only HCMC-R1 HANOI-R1 HCMC-SW1
```

The first command tests Python logic with mock devices; **it does not prove routers are running**. The second collects read-only CLI evidence from actual lab devices under `build/evidence/<UTC timestamp>/`, with JSON results. The live-check script deliberately marks some items for manual review rather than pretending that a captured command always means success. Follow **all** `docs/testcases.md` manual steps (including negative security tests and failover).

## 10. Security hardening additions

Generated switch access ports now enable sticky Port Security with a maximum
of two secure MAC addresses and violation mode restrict. Router/switch trunks
are not treated as endpoint access ports. DHCP Snooping and DAI trust remains
on the router-facing and switch-peer uplinks; host-facing ports remain
untrusted. Initial router/switch configurations include local AAA login
baseline. Verify with:

```text
show port-security
show port-security interface GigabitEthernet0/3
show port-security address
show ip dhcp snooping
show ip arp inspection
```

The optional Zone-Based Firewall template is in
docs/config_templates/IOSv_Zone_Based_Firewall_OPTIONAL.txt. It is deliberately
not enabled in the default config because ZBF behavior and command support
depend on the exact IOSv image and can interrupt routing/tunnel control-plane
traffic if misapplied. Apply only on a disposable router after the core tests
pass, following its pre-check and rollback procedure.

For the advanced enterprise targets (EVPN-VXLAN, controller SD-WAN, MPLS,
NGFW, ZTNA/SASE and WLC/CAPWAP), see docs/enterprise_extensions.md. These are
not falsely represented as deployed in the IOSv core lab.

## 11. Submission and limitations

- Submit the **Technical Explanation Report PDF** after replacing `NOT TESTED` placeholders with actual screenshots, logs, and measured results.
- Submit *startup-config exports from running devices*, along with generated initial configuration files and automation source code. Generated bootstrap config files alone are **not proof** that devices accepted the commands.
- Present a **15-minute live demo**, including baseline connectivity, shutdown failover, and Python automation. Suggested order: `docs/demo_script.md`.
- WAN public-looking IPs (`198.51.100.0/24`, `203.0.113.0/24`, `192.0.2.0/24`) are TEST-NET documentation ranges; all traffic is inside the emulator.
- A real production-grade lab would require a resilient HQ service tier, full NGFW and ZTNA/SASE integration, true controller-based SD-WAN and a verified spine/leaf EVPN-VXLAN fabric. The provided image families and 10-step scoring rubric do not define all of those implementations. **Do not claim these have been implemented.**

**Security note:** `build/secrets.local.env` and configs under `build/` contain **disposable lab credentials**. They are never hardcoded in Python source. Do not post those files publicly or reuse the credentials on actual equipment.


## Optional advanced enterprise extension

The separate `advanced_lab/` folder contains the staged design for
EVPN-VXLAN, MPLS L3VPN, controller-based SD-WAN, NGFW, ZTNA/SASE and
WLC/CAPWAP. It is intentionally isolated from the core 14-device lab.
Start with `advanced_lab/README.md`; validate its address and topology
manifest with:

```powershell
python tools/validate_advanced_lab.py
```

These are design/configuration artifacts, not proof of live deployment.
The advanced stages require compatible licensed images and, for controller-
based services, the corresponding controller software and licenses.


### Advanced implementation pack (Advance-GWork)

The separate `advanced_lab/` directory now includes:
- Arista EOS EVPN-VXLAN two-spine/two-leaf starter configs and addressing/cabling map.
- IOS-XE MPLS L3VPN provider/PE configuration examples with OSPF, LDP, VPNv4 and a shared customer VRF.
- Controller-based SD-WAN implementation runbook and application policy matrix.
- NGFW zones, default-deny policy blueprint and deployment order.
- OpenZiti-style ZTNA reference architecture and least-privilege service policy.
- Catalyst 9800 WLC/CAPWAP deployment reference.
- Core QoS policy explanation and verification steps in `docs/config_templates/IOS_QOS_VOICE_VIDEO.txt`.

Run:
```bash
python tools/validate_advanced_lab.py
python -m pytest -q
```

The advanced configs require matching licensed images/controllers. They are
not generated into the default 14-device core bootstrap and must be deployed
as isolated stages. See `advanced_lab/README.md` before starting them.
