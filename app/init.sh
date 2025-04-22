#!/bin/bash

# Set iptables rules
iptables -F

# Allow SSH (port 22)
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow HTTP (port 80)
iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# Drop all other inbound traffic
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Start SSH service
service ssh start

# Setup python virtual environment
if [ -e "./venv" ]; then
    rm -rf ./venv
fi

python3 -m venv venv
source venv/bin/activate
pip install flask

venv/bin/python3 server.py
