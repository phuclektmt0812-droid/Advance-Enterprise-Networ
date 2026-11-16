
# 05 -- Implementation Roadmap

## 1. Implementation Overview

The TVI project is organized into implementation phases following the assignment's six-week timeline and ten-step implementation process.

The implementation covers:

1. Requirement analysis and logical topology.
2. IPv4 VLSM and IPv6 addressing.
3. Layer 2 infrastructure and STP.
4. First Hop Redundancy and IP services.
5. Underlay routing.
6. Overlay routing and WAN edge.
7. Security and hardening.
8. Quality of Service.
9. Network automation.
10. Testing, verification, and documentation.

Each phase must be verified before the project proceeds to the next dependent phase.

## 2. Phase 1 -- Requirement Analysis and Design

Related assignment step: Step 1

Tasks:

- [ ] Review TVI's three-site requirements.
- [ ] Identify HQ, Hanoi, and Da Nang network requirements.
- [ ] Identify user, IoT, guest, server, and management networks.
- [ ] Define the logical network topology.
- [ ] Define the WAN and ISP connectivity model.
- [ ] Identify Layer 2 and Layer 3 boundaries.
- [ ] Identify redundant links and devices.
- [ ] Prepare the logical topology diagram using Visio or Draw.io.
- [ ] Label devices, links, interfaces, and network boundaries.
- [ ] Confirm the selected lab platform and available network images.

Expected deliverables:

- Logical network topology diagram.
- Requirement summary.
- Initial device and connection inventory.

## 3. Phase 2 -- IP Addressing and Subnetting

Related assignment step: Step 2

Tasks:

- [ ] Allocate hierarchical IPv4 address blocks to the three sites.
- [ ] Calculate IPv4 VLSM subnet sizes based on host requirements.
- [ ] Account for the expected growth of internal users and IoT endpoints.
- [ ] Allocate IPv6 prefixes hierarchically.
- [ ] Assign `/64` prefixes to normal LAN VLANs.
- [ ] Allocate routed transit networks.
- [ ] Document network addresses, prefix lengths, subnet masks, and gateways.
- [ ] Check for overlapping subnets.
- [ ] Prepare the Excel or Markdown IP schema.
- [ ] Confirm addressing consistency with the topology.

Expected deliverables:

- IPv4 VLSM allocation table.
- IPv6 addressing table.
- VLAN and gateway mapping.
- Routed transit addressing table.

## 4. Phase 3 -- Lab Environment and Topology Deployment

Tasks:

- [ ] Select EVE-NG, GNS3, or Cisco Modeling Labs (CML).
- [ ] Confirm hardware resources and virtualization support.
- [ ] Install and configure the selected lab platform.
- [ ] Import supported Cisco, Arista, or Juniper network images.
- [ ] Add the required HQ, Hanoi, and Da Nang network devices.
- [ ] Add ISP and WAN nodes.
- [ ] Add the management and automation node.
- [ ] Connect devices according to the approved topology.
- [ ] Assign device hostnames.
- [ ] Label interfaces and links.
- [ ] Save the initial lab project.

Cisco Packet Tracer may only be used if EVE-NG/GNS3 hardware requirements cannot be met and the instructor gives prior approval.

Expected deliverables:

- Working virtual lab.
- Device inventory.
- Saved topology project.

## 5. Phase 4 -- Layer 2 Infrastructure and STP

Related assignment step: Step 3

Tasks:

- [ ] Configure device hostnames and basic settings.
- [ ] Create the required VLANs.
- [ ] Configure access ports.
- [ ] Configure 802.1Q trunk links.
- [ ] Configure EtherChannel using LACP.
- [ ] Configure Rapid PVST+ or MSTP.
- [ ] Select primary and secondary STP root bridges.
- [ ] Assign unused ports to VLAN 999.
- [ ] Administratively shut down unused access ports.
- [ ] Verify VLAN membership and trunk operation.
- [ ] Verify EtherChannel status.
- [ ] Verify STP root bridge selection and loop prevention.

Expected deliverables:

- Layer 2 configurations.
- VLAN and trunk verification.
- EtherChannel and STP verification evidence.

## 6. Phase 5 -- First Hop Redundancy and IP Services

Related assignment step: Step 4

Tasks:

- [ ] Configure Layer 3 interfaces and VLAN gateways.
- [ ] Configure HSRP or VRRP.
- [ ] Configure primary gateway priority and preemption.
- [ ] Configure centralized DHCP services at HQ.
- [ ] Create DHCP scopes for required VLANs.
- [ ] Configure DHCP Relay at branch gateways.
- [ ] Configure centralized DNS services.
- [ ] Verify client address assignment.
- [ ] Verify DNS resolution.
- [ ] Test gateway failover.

Expected deliverables:

- HSRP/VRRP configurations.
- DHCP and DNS configurations.
- DHCP Relay verification.
- Gateway redundancy test results.

## 7. Phase 6 -- Underlay Routing

Related assignment step: Step 5

Tasks:

- [ ] Configure routed transit interfaces.
- [ ] Configure OSPF for internal site routing.
- [ ] Configure OSPF Area 0 or the approved area design.
- [ ] Configure OSPFv3 for IPv6 routing where supported.
- [ ] Configure Loopback0 interfaces where required.
- [ ] Configure passive interfaces on user-facing networks.
- [ ] Verify OSPF neighbor relationships.
- [ ] Verify route installation.
- [ ] Verify loopback reachability within each site.
- [ ] Test inter-site reachability.

Expected deliverables:

- OSPF and OSPFv3 configurations.
- Routing table outputs.
- Neighbor verification evidence.
- Inter-site connectivity results.

## 8. Phase 7 -- Overlay Routing and WAN Edge

Related assignment step: Step 6

Tasks:

- [ ] Configure the ISP simulation.
- [ ] Configure eBGP between the enterprise edge and ISP.
- [ ] Configure iBGP or the selected BGP overlay design where required.
- [ ] Evaluate MP-BGP EVPN for the Data Center fabric.
- [ ] Configure branch-to-HQ overlay connectivity.
- [ ] Implement IPsec tunnels where required and supported.
- [ ] Document SD-WAN transport paths.
- [ ] Configure route filtering and summarization.
- [ ] Configure default-route behavior.
- [ ] Verify external and inter-site routing.
- [ ] Test WAN path behavior and failover where implemented.

Expected deliverables:

- BGP configurations.
- WAN and overlay topology.
- IPsec configuration where implemented.
- BGP and WAN verification evidence.

## 9. Phase 8 -- Security and Hardening

Related assignment step: Step 7

Tasks:

- [ ] Define Corporate, Guest, IoT, Server, and Management security zones.
- [ ] Configure ACLs to isolate Guest traffic from Corporate resources.
- [ ] Restrict IoT communication to required services.
- [ ] Configure NAT overload for permitted Internet-bound traffic.
- [ ] Configure Port Security.
- [ ] Configure DHCP Snooping where supported.
- [ ] Configure Dynamic ARP Inspection (DAI) where supported.
- [ ] Evaluate Zone-based Firewall policies.
- [ ] Apply secure management access using SSH.
- [ ] Disable insecure management protocols where applicable.
- [ ] Document ZTNA principles and remote-access design.
- [ ] Test permitted and denied traffic.

Expected deliverables:

- Security policy documentation.
- ACL and hardening configurations.
- NAT verification.
- Security test evidence.

## 10. Phase 9 -- Quality of Service

Related assignment step: Step 8

Tasks:

- [ ] Identify voice and video traffic.
- [ ] Define QoS classification and marking policies.
- [ ] Apply EF marking for voice traffic.
- [ ] Apply AF31 marking for video traffic where required.
- [ ] Configure queuing and prioritization on WAN interfaces.
- [ ] Verify QoS policy counters and traffic behavior.
- [ ] Document simulator limitations if QoS behavior cannot be fully reproduced.

Expected deliverables:

- QoS policy configurations.
- QoS verification outputs.
- Traffic test results.

## 11. Phase 10 -- Network Automation

Related assignment step: Step 9

Choose one implementation approach:

- Python using Netmiko or NAPALM.
- Ansible using supported network modules.

### 11.1 Inventory and Credentials

- [ ] Create an external `inventory.yaml` or Ansible inventory file.
- [ ] Define hostname, management IP, device type, and SSH port.
- [ ] Obtain credentials through environment variables, interactive `getpass()`, or Ansible Vault.
- [ ] Ensure no plaintext passwords are stored in scripts or configuration files.

### 11.2 Automated Baseline and VLAN Provisioning

- [ ] Automate baseline AAA configuration.
- [ ] Automate NTP configuration.
- [ ] Automate Syslog configuration.
- [ ] Automate the login banner.
- [ ] Create and name VLAN 10: Executive.
- [ ] Create and name VLAN 20: Engineering.
- [ ] Create and name VLAN 30: Logistics.
- [ ] Create and name VLAN 99: Management.

The VLAN IDs and names must remain consistent with the assignment's Step 9 requirements.

### 11.3 State Capture and Configuration Backup

- [ ] Capture `show running-config` before configuration changes.
- [ ] Capture `show ip interface brief` before configuration changes.
- [ ] Apply the required configuration.
- [ ] Capture `show running-config` after configuration changes.
- [ ] Capture `show ip interface brief` after configuration changes.
- [ ] Save timestamped output files in `/backups/`.
- [ ] Log successful executions and SSH errors in `automation.log`.
- [ ] Implement error handling for unreachable devices and authentication failures.
- [ ] Ensure repeated runs do not apply unnecessary changes.

Expected deliverables:

- `inventory.yaml` or Ansible inventory.
- Python script or Ansible playbook.
- Timestamped configuration backups.
- Automation log.
- Execution and error-handling evidence.

## 12. Phase 11 -- Testing, Verification, and Documentation

Related assignment step: Step 10

Tasks:

- [ ] Verify end-to-end IPv4 connectivity.
- [ ] Verify IPv6 connectivity where implemented.
- [ ] Verify inter-VLAN routing.
- [ ] Verify inter-site routing.
- [ ] Verify DHCP and DNS.
- [ ] Verify NAT/PAT.
- [ ] Verify ACL and security policies.
- [ ] Verify BGP and OSPF operation.
- [ ] Verify QoS behavior.
- [ ] Verify automation execution.
- [ ] Perform failover testing by shutting down a primary core link or gateway.
- [ ] Capture genuine CLI output and screenshots.
- [ ] Save all router and switch startup configurations.
- [ ] Complete the Technical Explanation Report.
- [ ] Prepare the 15-minute live demonstration.

Expected deliverables:

- Technical Explanation Report in PDF.
- Configuration and code files.
- Testing evidence.
- Saved lab project.
- Live demonstration.

## 13. Six-Week Project Timeline

| Week | Milestone | Main Deliverables |
|---|---|---|
| Week 1 | Design and IP Schema | Logical topology and IP addressing plan |
| Week 2 | Layer 2 and IP Services | VLANs, LACP, STP, HSRP/VRRP, DHCP |
| Week 3 | Internal Routing | OSPF and internal reachability |
| Week 4 | WAN, BGP and Security | BGP/IPsec, NAT and edge ACLs |
| Week 5 | Automation and QoS | Automation scripts and QoS policies |
| Week 6 | Final Submission and Demo | Technical report, configurations and live demonstration |

## 14. Implementation Rules

- Complete and verify prerequisites before implementing dependent phases.
- Keep device configurations consistent with the documented topology and IP plan.
- Do not mark a feature as implemented until it has been configured and tested.
- Document platform and device-image limitations.
- Save configuration backups before and after significant changes.
- Use genuine command outputs and test results in the final report.
- Keep all project documentation updated when topology or addressing decisions change.
