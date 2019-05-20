#!/usr/bin/env bash

echo "Changing into ~/db_scripts"
cd /home/uwcc-admin/db_scripts
echo "Inside `pwd`"

echo "Generating rfield files for WRF v3"
sudo python gen_rfield_wrfv3.py