#!/usr/bin/env bash
# Run on Ubuntu HQ DNS/DHCP lab VM connected to HCMC-SW1 Gi0/4.
# WARNING: This changes eth0 addressing. Execute from console, not remote SSH.
set -euo pipefail
[[ $(id -u) -eq 0 ]] || { echo 'Run as root with sudo.'; exit 1; }
command -v apt-get >/dev/null || { echo 'This script expects Ubuntu/Debian.'; exit 1; }
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y dnsmasq iproute2 chrony rsyslog
ip link set eth0 up
ip addr replace 10.10.60.10/24 dev eth0
ip addr replace 10.10.60.20/24 dev eth0
ip route replace default via 10.10.60.1 dev eth0
cp "$(dirname "$0")/../build/services/dnsmasq.conf" /etc/dnsmasq.d/tvi.conf
grep -q '^allow 10.0.0.0/8' /etc/chrony/chrony.conf || echo 'allow 10.0.0.0/8' >>/etc/chrony/chrony.conf
grep -q '^local stratum 10' /etc/chrony/chrony.conf || echo 'local stratum 10' >>/etc/chrony/chrony.conf
cat >/etc/rsyslog.d/30-tvi-network.conf <<'EOF'
module(load="imudp")
input(type="imudp" port="514")
if ($fromhost-ip startswith "10.") then { action(type="omfile" file="/var/log/tvi-network.log"); stop }
EOF
systemctl enable --now chrony rsyslog dnsmasq
systemctl restart chrony rsyslog dnsmasq
mkdir -p /opt/tvi-inventory
printf '%s\n' 'TVI INVENTORY SERVICE OK' >/opt/tvi-inventory/index.html
cat >/etc/systemd/system/tvi-inventory-http.service <<'EOF'
[Unit]
Description=TVI inventory lab service
After=network.target
[Service]
Type=simple
WorkingDirectory=/opt/tvi-inventory
ExecStart=/usr/bin/python3 -m http.server 8080 --bind 10.10.60.20
Restart=on-failure
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now tvi-inventory-http
systemctl --no-pager status dnsmasq
ip -br addr show dev eth0
