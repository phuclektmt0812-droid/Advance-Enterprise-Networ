# 01 -- Project Scope and Requirements

## 1. Project Scope

The network covers three enterprise locations:

  Site      Role
  --------- -------------------------------------------
  HCMC HQ   Main site, central services, and ISP edge
  Hanoi     Branch office
  Da Nang   Branch office
  ISP       External network simulation

The lab is initially implemented in Cisco Packet Tracer.

## 2. Functional Requirements

  --------------------------------------------------------------------------------
  Area                    Planned capability               Initial status
  ----------------------- -------------------------------- -----------------------
  Network architecture    Three-site enterprise topology   Design baseline

  LAN                     VLANs, access ports, trunk links Planned

  Inter-VLAN routing      Layer 3 switching at HQ;         Planned
                          router-on-a-stick at branches    

  Internal routing        OSPF Area 0                      Planned

  External routing        eBGP between HQ and ISP          Planned

  WAN                     HQ-to-branch connectivity        Design decision to
                                                           verify

  VPN                     Site-to-site VPN if required by  To verify
                          rubric and supported by Packet   
                          Tracer                           

  DHCP                    Central DHCP service at HQ and   Planned
                          relay at remote subnets          

  DNS                     Central DNS service at HQ        Planned

  NAT                     PAT/NAT overload at HQ edge      Planned

  Security                Guest/Corporate/IoT access       Planned
                          restrictions                     

  Layer 2 security        DHCP Snooping and DAI, if        To verify
                          supported                        

  QoS                     WAN traffic                      To verify
                          classification/prioritization,   
                          if supported                     

  Automation              Python automation; Netmiko       To verify
                          compatibility test required      
  --------------------------------------------------------------------------------

## 3. Non-Functional Requirements

-   Use a consistent hostname and IP addressing convention.
-   Avoid overlapping IPv4 subnets.
-   Keep device configurations and documentation synchronized.
-   Prefer features that can be demonstrated reliably in Packet Tracer.
-   Keep the implementation small enough to complete and test within the
    project deadline.

## 4. Out of Scope for the Initial Baseline

The following are not considered completed or mandatory until the
assignment rubric and simulator support are checked:

-   IPv6 deployment.
-   HSRP or other gateway redundancy.
-   IPsec/GRE VPN implementation.
-   Advanced QoS policies.
-   External Netmiko management of Packet Tracer devices.

These items must not be reported as implemented unless they are actually
configured and tested.

## 5. Requirement Tracking Rule

For each requirement, use one of these states:

-   **Planned:** included in the design but not configured.
-   **In progress:** configuration or testing has started.
-   **Verified:** implemented and passed a test.
-   **Deferred:** postponed due to time or simulator limitations.
-   **Not supported:** confirmed unavailable in the selected Packet
    Tracer environment.

A design description alone does not count as implementation evidence.
