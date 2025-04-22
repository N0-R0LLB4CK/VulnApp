#!/bin/bash

# Navigate to the working directory
# cd /home/ubuntu/webapp || exit

# Start the DDoS protection tool in the background
sudo nohup ./ddos.py > ddos.log 2>&1 & echo $! > ddos.pid

# Start the Flask server using Gunicorn in the background
sudo nohup ./server.py > server.log 2>&1 & echo $! > server.pid

# Keep the script running
tail -f /dev/null

