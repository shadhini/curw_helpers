chmod +x gen_rfield_kelani_basin_parallelized_optimized_with_past_future.py
chmod +x gen_rfield_d03_parallelized_optimized_with_past_future.py

chmod +x venv

nohup ./rfield_extractor/gen_rfield_kelani_basin_parallelized_optimized_with_past_future.py -m "WRF_A,WRF_C,WRF_E,WRF_SE" -v "4.0" -s evening_18hrs 2>&1 /home/uwcc-admin/rfield_extractor/rfield.log




# working parallelized
nohup python3 /home/uwcc-admin/rfield_extractor/gen_rfield_d03_parallelized_optimized_with_past_future.py -m "WRF_A,WRF_C,WRF_E,WRF_SE" -v v4 -s "evening_18hrs" 2>&1 /home/uwcc-admin/rfield_extractor/rfield.log
nohup python3 /home/uwcc-admin/rfield_extractor/gen_rfield_kelani_basin_parallelized_optimized_with_past_future.py -m "WRF_A,WRF_C,WRF_E,WRF_SE" -v v4 -s "evening_18hrs" 2>&1 /home/uwcc-admin/rfield_extractor/rfield.log



# tar - czvf
# rfield_A.tar.gz. / WRF_A_ *
# 2002
# ls
# 2003
# mv
# rfield_A.tar.gz / mnt / disks / wrf_nfs / wrf / 4.0 / rfield / d03 / future /