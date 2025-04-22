#!/home/ubuntu/webapp/venv/bin/python3
import os
import time
import scapy.all as scapy
from collections import defaultdict

# Configuration
MONITORED_PORTS = {80, 443}  # Ports to monitor
THRESHOLD = 50  # Max requests per minute before blocking
CHECK_INTERVAL = 30  # Check every 60 seconds
UNBLOCK_TIME =  60 # Time to unblock IPs (in seconds)

# Store request counts
ip_request_count = defaultdict(int)
blocked_ips = {}

def packet_callback(packet):
    """ Callback function to analyze packets """
    if packet.haslayer(scapy.IP):
        src_ip = packet[scapy.IP].src
        if packet.haslayer(scapy.TCP) and packet[scapy.TCP].dport in MONITORED_PORTS:
            ip_request_count[src_ip] += 1

def block_ip(ip):
    """ Blocks an IP using iptables """
    if ip not in blocked_ips:
        os.system(f"sudo iptables -A INPUT -s {ip} -p tcp --dport 80 -j DROP")
        os.system(f"sudo iptables -A INPUT -s {ip} -p tcp --dport 443 -j DROP")
        blocked_ips[ip] = time.time()
        print(f"❌ Blocked IP: {ip}")
        with open("blocked_ips.log", "a") as log:
            log.write(f"{ip} blocked at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

def unblock_ips():
    """ Unblocks IPs after UNBLOCK_TIME """
    print("EXECUTING")
    current_time = time.time()
    for ip, block_time in list(blocked_ips.items()):
        if current_time - block_time >= UNBLOCK_TIME:
            os.system(f"sudo iptables -D INPUT -s {ip} -p tcp --dport 80 -j DROP")
            os.system(f"sudo iptables -D INPUT -s {ip} -p tcp --dport 443 -j DROP")
            del blocked_ips[ip]
            print(f"✅ Unblocked IP: {ip}")

def monitor_traffic():
    """ Runs the traffic monitoring loop """
    print("[*] DDoS Protection Active. Monitoring traffic...")
    while True:
        # Start sniffing packets in the background
        scapy.sniff(prn=packet_callback, store=0, timeout=CHECK_INTERVAL)

        # Check for abusive IPs
        for ip, count in list(ip_request_count.items()):
            if count > THRESHOLD:
                print(f"🚨 Detected abuse from {ip}: {count} requests")
                block_ip(ip)
            del ip_request_count[ip]  # Reset count

        unblock_ips() # Unblock expired ips

        time.sleep(1)  # Avoid excessive CPU usage

if __name__ == "__main__":
    monitor_traffic()
