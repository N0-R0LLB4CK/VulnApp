#!/bin/bash

# Function to show the current iptables rules
show_rules() {
    echo "[*] Current iptables rules:"
    sudo iptables -L -n
    echo "[✔] Rules displayed!"
}

# Function to delete a single IP from iptables
delete_ip() {
    IP=$1
    echo "[*] Removing IP: $IP from iptables..."
    sudo iptables -D INPUT -s $IP -j DROP
    echo "[✔] IP $IP removed!"
}

# Function to clear all iptables rules
clear_all() {
    echo "[⚠] Clearing ALL iptables rules..."
    sudo iptables -F
    sudo iptables -X
    echo "[✔] All iptables rules cleared!"
}

# Usage Instructions
if [[ "$1" == "--show" ]]; then
    show_rules
elif [[ "$1" == "--clear-all" ]]; then
    clear_all
elif [[ "$1" == "--delete" && -n "$2" ]]; then
    delete_ip "$2"
else
    echo "Usage:"
    echo "  $0 --show              # Shows current iptables rules"
    echo "  $0 --clear-all         # Clears all iptables rules"
    echo "  $0 --delete <IP>       # Deletes a specific blocked IP"
    exit 1
fi
