import os

try:
    os.system("rm ~/Desktop/temp/WRF_E_v4_*")
except Exception as e:
    print(e)

print("yes")