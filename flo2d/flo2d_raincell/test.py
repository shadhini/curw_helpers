with open('/home/shadhini/dev/repos/shadhini/curw_helpers/flo2d/flo2d_raincell/RAINCELL.DAT', 'r') as f:
    line = f.readline()
    cnt = 1
    while line:
       print("Line {}: {}".format(cnt, line.strip()))
       line = f.readline()
       cnt += 1