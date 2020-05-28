# 杭州6米站将AE转换为XY，输出dat文件，实现天线的驱动

import math

PI = math.pi
xy_list = []

with open('hz1.txt', 'r') as fi:
    lines = fi.readlines()

for line in lines:
    line_list = line.split(' ')
    line_list = [i for i in line_list if i != '']
    Az = float(line_list[-3])
    El = float(line_list[-2])
    # Az和El转换为XY轴的值
    Xz = math.atan(
        math.sin(math.pi * Az / 180) /
        math.tan(math.pi * El / 180)) * 180 / math.pi + 90
    Yz = math.asin(
        math.cos(PI * Az / 180) * math.cos(PI * El / 180)) * 180 / PI + 90
    # Xz = '%.3f' % Xz
    Xz = '{:.2f}'.format(Xz)
    Yz = '%.3f' % Yz
    # Xz = round(Xz, 3)
    # Yz = round(Yz, 3)
    # 拼接格式
    yyyy = line_list[0] + ' '
    mm = line_list[1] + ' '
    dd = line_list[2] + ' '
    hh = line_list[3] + ' '
    mm = line_list[4] + ' '
    ss = line_list[5].split('.')[0]
    if len(ss) < 2:
        ss = ' ' + line_list[5].split('.')[0] + '   '
    else:
        ss = line_list[5].split('.')[0] + '   '
    # xxx = str(Xz) + '  '
    xxx = Xz + '  '

    # yyy = str(Yz) + '  '
    yyy = Yz + '  '

    aaa = line_list[-3] + '  '
    eee = line_list[-2]
    lineXY = yyyy + mm + dd + hh + mm + ss + xxx + yyy + aaa + eee + '\n'
    xy_list.append(lineXY)
    with open('XY.dat', 'w') as fo:
        fo.writelines(xy_list)
    print(lineXY)
    print(Xz)
    print(Yz)
    print(line_list)