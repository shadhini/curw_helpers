#!/usr/bin/env bash

# Print execution date time
echo `date`

echo "Changing into ~/rfield_extractor"
cd /home/uwcc-admin/rfield_extractor
echo "Inside `pwd`"


echo "Flushing older rfield files"
sudo rm ~/rfield_extractor/d01/past/*
sudo rm ~/rfield_extractor/d01/future/*


# If no venv (python3 virtual environment) exists, then create one.
if [ ! -d "venv" ]
then
    echo "Creating venv python3 virtual environment."
    virtualenv -p python3 venv
fi

# Activate venv.
echo "Activating venv python3 virtual environment."
source venv/bin/activate

# Install dependencies using pip.
if [ ! -f "gen_rfield.log" ]
then
    echo "Installing numpy"
    pip install numpy
    echo "Installing netCDF4"
    pip install netCDF4
    echo "Installing cftime"
    pip install cftime
    echo "Installing PyMySQL"
    pip install PyMySQL
    echo "Installing paramiko"
    pip install paramiko
fi

# Generate rfields locally
echo "Running scripts to generate d01 rfields"
python gen_rfield_d01_wrfv4.py >> gen_rfield.log 2>&1

# Deactivating virtual environment
echo "Deactivating virtual environment"
deactivate

