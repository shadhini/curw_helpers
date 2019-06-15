#!/usr/bin/env bash

#!/usr/bin/env bash

echo `date`

echo "Changing into ~/flo2d_raincell"
cd /home/uwcc-admin/flo2d_raincell
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
if [ ! -f "raincell.log" ]
then
    echo "Installing PyMySQL"
    pip install PyMySQL
#    echo "Installing PyYAML"
#    pip install PyYAML
#    echo "Installing db adapter"
#    pip install git+https://github.com/shadhini/curw_db_adapter.git
fi


# Update grid mappings in curw_sim
echo "Running prepare_raincell.py"
python prepare_raincell.py >> raincell.log 2>&1

# Deactivating virtual environment
echo "Deactivating virtual environment"
deactivate
