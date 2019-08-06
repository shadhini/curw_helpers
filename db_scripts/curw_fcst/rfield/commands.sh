chmod +x gen_rfield_kelani_basin_parallelized.py
chmod +x gen_rfield_d03_parallelized.py

chmod +x venv

nohup ./rfield_extractor/gen_rfield_kelani_basin_parallelized.py -m "WRF_A,WRF_C,WRF_E,WRF_SE" -v "4.0" -s evening_18hrs 2>&1 /home/uwcc-admin/rfield_extractor/rfield.log




# working parallelized
nohup python3 /home/uwcc-admin/rfield_extractor/gen_rfield_d03_parallelized.py -m "WRF_A,WRF_C,WRF_E,WRF_SE" -v v4 -s "evening_18hrs" 2>&1 /home/uwcc-admin/rfield_extractor/rfield.log
nohup python3 /home/uwcc-admin/rfield_extractor/gen_rfield_kelani_basin_parallelized.py -m "WRF_A,WRF_C,WRF_E,WRF_SE" -v v4 -s "evening_18hrs" 2>&1 /home/uwcc-admin/rfield_extractor/rfield.log