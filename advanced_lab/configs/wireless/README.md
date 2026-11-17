# WLC/CAPWAP wireless extension

This stage requires a wireless LAN controller and lightweight AP images or
physical devices that support the same CAPWAP implementation. IOSvL2 alone
does not emulate a WLC/AP system.

## Logical design

- WLC management: 10.43.20.0/24.
- Corporate SSID: maps to VLAN 110 (CORP_APP) for this lab demonstration.
- Guest SSID: maps to VLAN 150 (GUEST), isolated from corporate services.
- AP management and CAPWAP control reach the WLC through the management
  network; permit only the controller/AP discovery and control flows required
  by the selected platform.
- Use the selected platform's supported WPA2/WPA3-Enterprise and RADIUS
  integration when available.

## Deployment sequence

1. Configure management addressing, DNS and time synchronization.
2. Configure switch trunk and allowed VLANs to the WLC/AP infrastructure.
3. Configure WLC management and AP join policy.
4. Verify AP discovery and CAPWAP join before creating SSIDs.
5. Map SSIDs to VLANs and verify DHCP and policy enforcement.
6. Test guest isolation and AP/controller restart recovery.

Wi-Fi 6/7 throughput and RF coverage require physical radio hardware and a
site survey; they cannot be certified by a packet emulator alone.
