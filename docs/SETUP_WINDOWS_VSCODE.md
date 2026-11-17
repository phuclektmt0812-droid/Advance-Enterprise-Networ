# Windows + VS Code Setup and GNS3 Runbook

This guide separates three activities that are often confused:

1. **Local Python setup and automated tests** — does not require GNS3 or Cisco images.
2. **Core GNS3/EVE-NG lab deployment** — boots the network devices and services.
3. **Live Netmiko automation and verification** — requires reachable SSH management interfaces.

The commands below use Windows PowerShell from the repository root.

## 1. Install the workstation tools

Install:

- Git.
- Visual Studio Code.
- The Microsoft **Python** extension in VS Code.
- 64-bit CPython 3.12 (recommended for a consistent Windows setup; the project requires Python 3.10+).
- GNS3 GUI and GNS3 VM, plus a supported hypervisor for the VM (follow the GNS3 installation guide for the supported version combination).

Cisco IOSv/IOSvL2 and other vendor images are not included in this repository. Obtain and use them only if you are licensed/authorized to do so.

For Windows, prefer the standard CPython installer from python.org. MSYS2/MinGW Python builds can require platform-specific compiled dependencies; they are not the default setup path in this guide.

## 2. Clone and open the correct branch

If the repository has not been cloned:

```powershell
git clone https://github.com/phuclektmt0812-droid/Advance-Enterprise-Networ.git
cd Advance-Enterprise-Networ
git switch Advance-GWork
```

If it is already cloned:

```powershell
git switch Advance-GWork
git pull
```

Open this repository folder in VS Code (**File → Open Folder**). Do not open only the `tests` or `automation` subfolder.

## 3. Create the Python virtual environment

In VS Code, open **Terminal → New Terminal** and select PowerShell.

```powershell
py -3.12 --version
py -3.12 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip check
```

If `py -3.12` is not available, install CPython 3.12 (64-bit), enable **Add Python to PATH**, restart VS Code, and repeat. Do not create a second virtual environment if a working `.venv` already exists; activate it and install the requirements into that environment.

In VS Code press **Ctrl+Shift+P** → **Python: Select Interpreter** → select `.venv\Scripts\python.exe`.

### What gets installed

The root `requirements.txt` is the authoritative Python package list:

- `netmiko` — SSH connection and configuration automation.
- `PyYAML` — YAML inventory, VLAN and network-plan parsing.
- `pytest` — automated test runner.

Installing Netmiko also installs its required runtime dependencies, including Paramiko, Cryptography, PySerial, TextFSM, NTC Templates, Rich and SCP. Normally, one command is sufficient:

```powershell
python -m pip install -r requirements.txt
```

Do not install these dependencies individually unless pip reports a specific installation problem. Do not use `--no-deps` for a normal Windows CPython setup.

## 4. Run local tests (no GNS3 required)

From the repository root, with `.venv` active:

```powershell
python -m pytest -v
```

A passing result means the local Python tests passed. The automation tests use mocked/fake device connections. This command does **not** connect to routers or switches and does not prove that a GNS3 topology is running.

Useful additional static checks:

```powershell
python tools/validate_plan.py
python tools/validate_advanced_lab.py
python -m compileall -q tools automation
```

Generate the core device configuration and topology artifacts when needed:

```powershell
python tools/build_lab.py
python tools/generate_topology.py
```

The build script creates local generated files under `build/`, including disposable lab credentials in `build/secrets.local.env`. Do not commit or share this file or generated configs containing credentials.

## 5. Prepare the core GNS3 topology

The core lab is separate from the optional advanced lab.

The core network requires these network devices:

- 8 IOSv routers: HCMC-R1/R2, HANOI-R1/R2, DANANG-R1/R2, ISP-A and ISP-B.
- 6 IOSvL2 switches: SW1/SW2 at each of the three sites.
- Linux service nodes: HQ-DHCP-DNS and INTERNET-TEST.
- Six VPCS/Linux client nodes (corporate and guest at each site).
- An automation host. This may be the Windows PC if it has a route to all management subnets, or a Linux node inside the lab.

Use the exact port-to-port links in `docs/interface_matrix.csv`. The logical and physical diagrams are in `docs/TVI_Logical_Topology.drawio` and `docs/TVI_Physical_Topology.drawio`.

Start with the **core 14-device topology only**. Do not start all optional EVPN/MPLS/SD-WAN/NGFW/WLC/ZTNA nodes at the same time. The advanced lab is staged separately in `advanced_lab/README.md`. The repository notes an 8 GB host; that is constrained for a large multi-node topology. Start a small subset first, monitor RAM/CPU, and stop unused nodes between stages. The README's higher RAM recommendation is for running the full core topology more comfortably.

After creating the nodes:

1. Start the GNS3 VM and confirm it is connected to the GNS3 GUI.
2. Add the authorized IOSv and IOSvL2 images to the GNS3 appliance templates.
3. Create the 8 routers and 6 switches with the required interfaces.
4. Add the Linux/VPCS nodes.
5. Cable the devices according to `docs/interface_matrix.csv`.
6. Start nodes and wait for IOS to finish booting.
7. From each router/switch console, paste the corresponding generated bootstrap file from `build/Configurations/<SITE>/<HOSTNAME>.bootstrap.txt`. The two ISP routers have their own provider configuration files.
8. Check console output for rejected or incomplete commands. Confirm interface names against the actual image; adapt the configuration if the image uses different interface numbering.
9. Configure and start the two Linux service nodes using `server/prepare_hq_server.sh` and `server/prepare_internet_server.sh` from their Linux consoles. These scripts assume Ubuntu/Debian and an interface named `eth0`; adjust the interface name if the VM uses another name.

Detailed node placement, cabling and first routing checks are in `README.md`, `docs/physical_topology.md` and `docs/testcases.md`.

## 6. Prepare SSH management before running automation

The automation inventory contains **12 enterprise devices** (the six site routers and six site switches). It intentionally excludes ISP-A and ISP-B.

The inventory addresses are:

- HCMC: `10.10.99.2`, `.3`, `.11`, `.12`.
- Hanoi: `10.20.99.2`, `.3`, `.11`, `.12`.
- Da Nang: `10.30.99.2`, `.3`, `.11`, `.12`.

These are planned management addresses, not devices that exist automatically on the Windows PC. The lab must be booted, the management interfaces configured, and a route from the automation host to those subnets must exist.

From Windows PowerShell, test one device first:

```powershell
Test-NetConnection 10.10.99.11 -Port 22
```

Proceed only when `TcpTestSucceeded : True`. Repeat for the remaining inventory addresses. If it is `False`, fix the GNS3 link, IP address, routing, SSH configuration or host-side route before trying Netmiko.

Before enabling AAA automation, ensure every target device already has a valid local administrator account and that the account can enter privileged EXEC mode. The current script applies `aaa new-model` and local AAA authentication but does **not** create the local administrator account. The script also uses the supplied password as the enable secret; ensure this matches the device's enable credential or adjust the script/device configuration deliberately before deployment.

## 7. Run live Netmiko automation

Only after SSH reachability has been confirmed, run a one-device canary first:

```powershell
python automation/auto_provision.py --only HCMC-SW1
```

The script prompts for SSH username and password if `TVI_USERNAME` and `TVI_PASSWORD` are not set. The password prompt is hidden. Do not put credentials in source code or commit them.

If the canary succeeds and the resulting device configuration/backup has been reviewed, run all 12 enterprise devices:

```powershell
python automation/auto_provision.py
```

The script captures `show running-config` and `show ip interface brief` before and after, checks VLANs on switches, applies missing AAA/NTP/Syslog/banner settings, adds the desired VLANs, saves configuration, and writes logs/backups under:

- `build/automation_results/backups/`
- `build/automation_results/logs/automation.log`

The VLAN list includes VLAN140 (`DEMO_AUDIT`) as a demonstration change. This is not part of the normal VLAN set in the core network plan.

## 8. Verify and collect live evidence

After automation:

```powershell
python tools/verify_live.py
```

For a smaller sample:

```powershell
python tools/verify_live.py --only HCMC-R1 HANOI-R1 HCMC-SW1
```

Also run the manual commands and traffic tests in `docs/testcases.md`: VLAN/trunk/EtherChannel/STP, OSPF/BGP, HSRP, GRE/IPsec, DHCP/DNS, ACL deny cases, NAT/PAT, QoS, and failover. Save command output, screenshots and timestamps. Do not mark a live test PASS from generated configuration alone.

## 9. Troubleshooting meanings

| Symptom | Meaning / next check |
|---|---|
| `ModuleNotFoundError` during import | Activate the intended `.venv`; install `requirements.txt` into that interpreter. |
| `pip check` reports missing Netmiko dependency | Re-run `python -m pip install -r requirements.txt`; inspect the specific package installation error. |
| `NetmikoTimeoutException: TCP connection to device failed` | TCP endpoint is unreachable; check that GNS3 nodes are running, IP/port 22, management routing and host firewall. This is not a wrong-password diagnosis. |
| `AuthenticationException` / authentication failure | TCP/SSH reached the device; verify username/password and device AAA configuration. |
| IOS reports invalid/incomplete command | The selected IOS image may not support that syntax or may use different interface names/features; inspect the device console and adapt the config. |
| Automation fails after enabling AAA | Use the local device console; confirm a valid local admin account exists before retrying. |

