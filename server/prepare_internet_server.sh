#!/usr/bin/env bash
# Run in an Ubuntu test host, eth0 -> ISP-A Gi0/4. Console only.
set -euo pipefail
[[ $(id -u) -eq 0 ]] || { echo 'Run as root with sudo.'; exit 1; }
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y dnsmasq iproute2 python3
ip link set eth0 up
ip addr replace 192.0.2.18/30 dev eth0
ip route replace default via 192.0.2.17 dev eth0
cat >/etc/dnsmasq.d/tvi-internet.conf <<'EOF'
no-resolv
server=1.1.1.1
listen-address=192.0.2.18
bind-dynamic
address=/internet.tvi.lab/192.0.2.18
EOF
systemctl enable --now dnsmasq
systemctl restart dnsmasq
mkdir -p /opt/tvi-www
echo 'TVI TEST INTERNET SERVICE OK' >/opt/tvi-www/index.html
cat >/etc/systemd/system/tvi-internet-http.service <<'EOF'
[Unit]
Description=TVI training-lab HTTP web server
After=network.target
[Service]
Type=simple
WorkingDirectory=/opt/tvi-www
ExecStart=/usr/bin/python3 -m http.server 80 --bind 192.0.2.18
Restart=on-failure
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now tvi-internet-http
systemctl --no-pager status tvi-internet-http
