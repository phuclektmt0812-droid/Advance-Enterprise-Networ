# Dual-WAN routing fallback for the core lab

This is an implementable WAN-resiliency fallback using the existing Core Lab
routing design. It is **not controller-based SD-WAN** and must not be reported
as such. It is useful while a licensed SD-WAN controller/edge platform is
unavailable.

## Existing implementation

The core configuration generator already provisions dual ISP uplinks, eBGP
to the provider ASNs, route tracking/HSRP tracking and GRE/IPsec tunnels for
inter-site connectivity. Use the generated per-site router configs as the
source of truth; do not paste a second set of static routes over them.

## Validation sequence

1. Confirm both ISP-facing interfaces are up and each expected eBGP neighbor
   is Established.
2. Confirm the preferred default route and backup path in the RIB.
3. Run continuous pings between the site test loopbacks and to the simulated
   Internet test host.
4. Shut only the primary lab WAN interface during a controlled test.
5. Verify route withdrawal/backup path selection and inter-site reachability.
6. Restore the interface and verify stable route recovery.
7. Repeat with the other WAN path and record convergence time.

## Commands

IOS/IOS-XE command equivalents:
```text
show ip bgp summary
show ip route 0.0.0.0
show ip route <remote-site-prefix>
show standby brief
show interface description
show crypto ikev2 sa
show crypto ipsec sa
```

## What remains necessary for true SD-WAN

A true controller-managed SD-WAN deployment still needs a compatible vendor
edge image, manager/orchestrator, control-plane components, authenticated
device onboarding, centralized templates/policies, application/SLA-aware
path selection and telemetry. The dual-WAN fallback above proves routing
resiliency only; it does not satisfy those controller requirements.
