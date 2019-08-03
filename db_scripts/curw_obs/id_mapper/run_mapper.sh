#!/usr/bin/env bash

cd /home/uwcc-admin/curwid-curwobs-mapper
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
if [ ! -f "id_mapper.log" ]
then
    echo "Installing mysql-connector"
    pip install mysql-connector-python
    echo "Installing mysqladapter"
    pip install git+https://github.com/CUrW-SL/curw_db_adapter.git
fi

echo "Run id_mapper.py"
python id_mapper.py >> id_mapper.log 2>&1

# Deactivating virtual environment
echo "Deactivating virtual environment"
deactivate