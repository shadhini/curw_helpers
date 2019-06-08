#!/usr/bin/env bash

echo `date`

echo "Changing into ~/curw_sim_utils"
cd /home/uwcc-admin/curw_sim_utils
echo "Inside `pwd`"


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
if [ ! -f "curw_sim_fcst_flo2d_250.log" ]
then
    echo "Installing PyMySQL"
    pip install PyMySQL
    echo "Installing PyYAML"
    pip install PyYAML
    echo "Installing db adapter"
    pip install git+https://github.com/shadhini/curw_db_adapter.git
fi


# Update fcst data in curw_sim for flo2d grids
echo "Running update_obs_rainfall_flo2d_250.py"
python update_fcst_rainfall_flo2d_250.py >> curw_sim_fcst_flo2d_250.log 2>&1

# Deactivating virtual environment
echo "Deactivating virtual environment"
deactivate
