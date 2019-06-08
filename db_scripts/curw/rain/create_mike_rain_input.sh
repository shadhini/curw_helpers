#!/usr/bin/env bash

echo "Changing into ~/mike_input"
cd /home/uwcc-admin/mike_input
echo "Inside `pwd`"

#echo "Flushing older rain files"
#sudo rm /var/www/html/wrf/v3/rfield/*

echo "Generating run files for MIKE"
sudo python 2d_obs_3d_fcst_rain_15min.py
