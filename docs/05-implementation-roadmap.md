# 05 -- Implementation Roadmap

## Phase 1: Design and Repository Preparation

-   [x] Select Cisco Packet Tracer as the initial simulator.
-   [x] Select Python + Netmiko as the intended automation approach,
    pending compatibility test.
-   [x] Establish three-site architecture baseline.
-   [x] Establish initial VLAN and IPv4 addressing plan.
-   [ ] Confirm assignment rubric requirements for VPN, IPv6,
    redundancy, and QoS.
-   [ ] Confirm Packet Tracer version and available device models.
-   [ ] Assign physical interface numbers and cable connections.

## Phase 2: Build the Topology

-   [ ] Add the HQ edge router, core Layer 3 switch, and two access
    switches.
-   [ ] Add the Hanoi router and two access switches.
-   [ ] Add the Da Nang router and one access switch.
-   [ ] Add the ISP router.
-   [ ] Add the central DHCP/DNS server.
-   [ ] Connect devices and label links.
-   [ ] Save the Packet Tracer project.

## Phase 3: Implement LAN

-   [ ] Configure hostnames and basic device settings.
-   [ ] Create VLANs.
-   [ ] Configure access ports.
-   [ ] Configure trunk links.
-   [ ] Configure HQ SVIs and branch router subinterfaces.
-   [ ] Configure management addressing.
-   [ ] Verify local VLAN and inter-VLAN connectivity.

## Phase 4: Implement Routing and WAN

-   [ ] Configure routed transit links.
-   [ ] Configure OSPF Area 0.
-   [ ] Verify OSPF neighbors and route tables.
-   [ ] Configure eBGP between HQ and ISP.
-   [ ] Verify external route/default-route behavior.
-   [ ] Configure NAT/PAT.
-   [ ] Verify inter-site and simulated external connectivity.

## Phase 5: Implement Services and Security

-   [ ] Configure DHCP scopes.
-   [ ] Configure DHCP relay.
-   [ ] Configure DNS service and records.
-   [ ] Verify DHCP and DNS from each site.
-   [ ] Define and apply Guest/Corporate/IoT ACL policies.
-   [ ] Verify both permitted and denied traffic.
-   [ ] Attempt DHCP Snooping and DAI only if supported by selected
    devices.

## Phase 6: Automation and QoS

-   [ ] Verify whether Packet Tracer devices can accept external
    SSH/Netmiko sessions.
-   [ ] If supported, test a minimal Netmiko connection and read-only
    command.
-   [ ] If unsupported, agree on an alternative automation deliverable
    with the instructor or use a clearly documented
    configuration-generation/backup workflow.
-   [ ] Implement and test the selected automation task.
-   [ ] Implement QoS only after confirming simulator support and the
    required traffic model.

## Phase 7: Final Validation and Submission

-   [ ] Run end-to-end connectivity tests.
-   [ ] Verify routing, services, security, and automation.
-   [ ] Save final Packet Tracer project and device configurations.
-   [ ] Capture genuine test evidence.
-   [ ] Complete the technical report and README.
-   [ ] Rehearse the live demonstration.

## Priority Under a Short Deadline

1.  Topology and addressing.
2.  VLANs and local connectivity.
3.  OSPF and inter-site connectivity.
4.  eBGP and simulated ISP connectivity.
5.  DHCP, DNS, NAT, and ACL.
6.  Automation compatibility and minimum viable implementation.
7.  VPN, QoS, IPv6, redundancy, and advanced Layer 2 security according
    to rubric priority and remaining time.

Do not start a later phase until the previous phase has a working
baseline.
