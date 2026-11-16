# 03 -- VLAN and IPv4 Addressing Plan

## 1. Addressing Rules

-   Private enterprise addressing uses `10.0.0.0/8`.
-   Each site receives a separate `10.x.0.0/16` block.
-   Each VLAN uses a `/24` subnet for simple planning and
    troubleshooting.
-   `.1` is reserved for the default gateway.
-   `.2` to `.49` are reserved for infrastructure and static addresses.
-   `.100` to `.199` are the planned DHCP client range.
-   Remaining addresses are reserved for future use.

## 2. VLAN Definitions

    VLAN ID Name         Purpose
  --------- ------------ --------------------------------------
         10 CORPORATE    Employee devices
         20 GUEST        Guest devices
         30 IOT          IoT devices
         40 SERVER       Central servers; HQ only in baseline
         99 MANAGEMENT   Network device management

## 3. HCMC Headquarters

Site block: `10.10.0.0/16`

    VLAN Network         Mask            Gateway
  ------ --------------- --------------- ------------
      10 10.10.10.0/24   255.255.255.0   10.10.10.1
      20 10.10.20.0/24   255.255.255.0   10.10.20.1
      30 10.10.30.0/24   255.255.255.0   10.10.30.1
      40 10.10.40.0/24   255.255.255.0   10.10.40.1
      99 10.10.99.0/24   255.255.255.0   10.10.99.1

Static assignments:

  Device                                  VLAN Address
  ------------------------------------- ------ ----------------
  SW-HQ-Core SVI                            99 10.10.99.2/24
  SW-HQ-A1 management SVI                   99 10.10.99.3/24
  SW-HQ-A2 management SVI                   99 10.10.99.4/24
  DHCP/DNS Server                           40 10.10.40.10/24
  SW-HQ-Core routed transit interface      N/A 10.10.254.2/30
  R-HQ routed transit interface            N/A 10.10.254.1/30

The core-to-router transit network is `10.10.254.0/30`.

## 4. Hanoi Branch

Site block: `10.20.0.0/16`

    VLAN Network         Mask            Gateway
  ------ --------------- --------------- ------------
      10 10.20.10.0/24   255.255.255.0   10.20.10.1
      20 10.20.20.0/24   255.255.255.0   10.20.20.1
      30 10.20.30.0/24   255.255.255.0   10.20.30.1
      99 10.20.99.0/24   255.255.255.0   10.20.99.1

## 5. Da Nang Branch

Site block: `10.30.0.0/16`

    VLAN Network         Mask            Gateway
  ------ --------------- --------------- ------------
      10 10.30.10.0/24   255.255.255.0   10.30.10.1
      20 10.30.20.0/24   255.255.255.0   10.30.20.1
      30 10.30.30.0/24   255.255.255.0   10.30.30.1
      99 10.30.99.0/24   255.255.255.0   10.30.99.1

## 6. WAN and Transit Networks

  -----------------------------------------------------------------------
  Link              Network           Endpoint A        Endpoint B
  ----------------- ----------------- ----------------- -----------------
  HQ -- Hanoi       10.255.0.0/30     R-HQ: 10.255.0.1  R-HN: 10.255.0.2

  HQ -- Da Nang     10.255.0.4/30     R-HQ: 10.255.0.5  R-DN: 10.255.0.6

  HQ -- Core        10.10.254.0/30    R-HQ: 10.10.254.1 SW-HQ-Core:
                                                        10.10.254.2

  HQ -- ISP         203.0.113.0/30    R-HQ: 203.0.113.1 ISP: 203.0.113.2
  -----------------------------------------------------------------------

`203.0.113.0/24` is a documentation/test range (TEST-NET-3), not a real
public Internet allocation.

## 7. DHCP Address Pool Convention

For client VLANs, the planned DHCP range is `.100`--`.199`.

Example for HCMC Corporate VLAN:

-   Network: `10.10.10.0/24`
-   Default gateway: `10.10.10.1`
-   DHCP range: `10.10.10.100`--`10.10.10.199`
-   DNS server: `10.10.40.10`

Exclude gateway and statically assigned addresses from DHCP pools. The
Server VLAN may use static addressing for servers.

## 8. DHCP Relay

The Layer 3 gateway for each remote subnet must relay DHCP requests to
the central server at `10.10.40.10`.

-   At HQ, configure relay on client VLAN SVIs where the DHCP server is
    in a different subnet.
-   At branches, configure relay on the router subinterfaces for VLANs
    10, 20, and 30.
-   VLAN 99 relay is optional and should be enabled only if management
    devices use central DHCP; static management addressing is preferred
    for the initial baseline.

## 9. Addressing Validation Checklist

-   [ ] No overlapping subnets.
-   [ ] Every VLAN has one documented gateway.
-   [ ] Every routed point-to-point link uses a unique subnet.
-   [ ] Server addresses are static and excluded from DHCP.
-   [ ] DHCP scopes match the documented network, mask, gateway, and DNS
    server.
-   [ ] All device configurations match this document.
