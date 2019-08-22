#!/usr/bin/env bash

cd /home/uwcc-admin/data-pusher-curwobs
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
if [ ! -f "pusher.log" ]
then
    echo "Installing pytz"
    pip install pytz
    echo "Installing mysqladapter"
    pip install git+https://github.com/gihankarunarathne/CurwMySQLAdapter.git
    echo "Installing db adapter"
    pip install git+https://github.com/shadhini/curw_db_adapter.git
fi

echo "Running Pusher.py. Logs Available in pusher.log file."
python Pusher.py >> pusher.log 2>&1

# Deactivating virtual environment
echo "Deactivating virtual environment"
deactivate