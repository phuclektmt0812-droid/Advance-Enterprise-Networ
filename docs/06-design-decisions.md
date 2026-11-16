# 06 -- Design Decisions and Open Issues

## 1. Confirmed Decisions

  -----------------------------------------------------------------------
  ID                      Decision                Reason
  ----------------------- ----------------------- -----------------------
  D-01                    Use Cisco Packet Tracer Confirmed by project
                          as the initial          owner
                          simulator               

  D-02                    Use Python + Netmiko as Confirmed as preferred
                          the intended automation approach; compatibility
                          approach                remains unverified

  D-03                    Model three enterprise  Matches project scope
                          sites: HCMC, Hanoi, Da  
                          Nang                    

  D-04                    Use `10.0.0.0/8` for    Structured private IPv4
                          private enterprise      plan
                          addressing              

  D-05                    Use VLAN 10/20/30/40/99 Separates Corporate,
                                                  Guest, IoT, Server, and
                                                  Management

  D-06                    Use OSPF Area 0         Consistent dynamic
                          internally              routing domain

  D-07                    Use eBGP between        Demonstrates external
                          enterprise AS 65010 and routing
                          ISP AS 65000            

  D-08                    Place central DHCP/DNS  Centralized service
                          services at HCMC HQ     design
  -----------------------------------------------------------------------

## 2. Assumptions

-   The lab is an educational simulation, not a production network.
-   Candidate router and switch models will be selected from those
    available in the installed Packet Tracer version.
-   The `203.0.113.0/30` ISP-facing link is for documentation/lab use
    only.
-   The initial design uses a hub-and-spoke logical WAN with HQ as the
    central site.

## 3. Open Issues Requiring Verification

  -----------------------------------------------------------------------
  ID                      Issue                   Required action
  ----------------------- ----------------------- -----------------------
  O-01                    Exact Packet Tracer     Confirm version and
                          version and device      available models
                          models                  

  O-02                    Physical interface      Decide after placing
                          mapping                 devices

  O-03                    VPN requirement         Check assignment
                                                  wording; current
                                                  point-to-point links
                                                  are not encrypted VPNs

  O-04                    Netmiko compatibility   Test external SSH
                                                  access to a simulated
                                                  router

  O-05                    QoS support             Check supported
                                                  commands and traffic
                                                  simulation

  O-06                    DHCP Snooping and DAI   Check selected switch
                          support                 model and command
                                                  availability

  O-07                    IPv6 and gateway        Compare with rubric and
                          redundancy requirements remaining time
  -----------------------------------------------------------------------

## 4. Important Technical Caveats

### Packet Tracer and Netmiko

Netmiko is designed to connect to network devices through supported
management protocols such as SSH. Packet Tracer simulates device
behavior and does not necessarily expose its simulated IOS devices as
externally reachable network endpoints. A real connection test is
required before promising Netmiko-based live configuration.

### WAN and VPN

A routed point-to-point connection is not equivalent to an IPsec VPN. If
VPN is a mandatory rubric item, update the topology and routing/WAN plan
before implementation.

### Feature Support

Packet Tracer implements a subset of real Cisco IOS behavior. A feature
should be marked as verified only after the relevant command is accepted
and the behavior is tested.

## 5. Change Control

When a design decision changes:

1.  Update the relevant document in `docs/`.
2.  Update this decision log.
3.  Update the addressing table if IPs or VLANs change.
4.  Keep Packet Tracer device configurations consistent with the
    documents.
5.  Record the reason for the change.
