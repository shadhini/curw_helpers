#!/usr/bin/env bash

echo "Changing into ~/rfield_extractor"
cd /home/uwcc-admin/rfield_extractor
echo "Inside `pwd`"

echo "Flushing older rfield files"
sudo rm /var/www/html/wrf/v3/rfield/*

echo "Generating rfield files for WRF v3"
sudo python gen_rfield_wrfv3.py
