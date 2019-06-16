#!/usr/bin/env bash

echo "Changing into ~/rfield_extractor"
cd /home/uwcc-admin/rfield_extractor
echo "Inside `pwd`"

echo "Flushing older rfield files"
sudo rm /var/www/html/wrf/v4/rfield/d03/past/*
sudo rm /var/www/html/wrf/v4/rfield/d03/future/*

echo "Generating rfield files for WRF v4"
sudo python gen_rfield_d03_wrfv4.py
#!/usr/bin/env bash