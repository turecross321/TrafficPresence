#!/bin/bash

echo Running Car Rich Presence...
cd /home/ture/TrafficPresence/
sudo -b su -c "rfcomm connect hci0 00:04:3E:1F:16:64 1 &"
python car_obd.py --model skoda-octavia