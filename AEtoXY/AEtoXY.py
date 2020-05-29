# 杭州6米站将AE转换为XY，输出dat文件，实现天线的驱动

import math
import numpy as np

PI = math.pi
# 最终结果列表
xy_value_list = []
# 中间计算过程列表
xy_list = []
# xy轴值列表
xz_list = []
yz_list = []
az_list = []
el_list = []
# 插值后的列表
xz_value8_list = []
yz_value8_list = []
az_value8_list = []
el_value8_list = []

with open('HZ052923.RAE', 'r') as fi:
    lines = fi.readlines()

for line in lines:
    line_list = line.split(' ')
    line_list = [i for i in line_list if i != '']
    # print(line_list)

    Az = float(line_list[-3])
    az_list.append(Az)
    El = float(line_list[-2])
    el_list.append(El)
    # Az和El转换为XY轴的值
    Xz = math.atan(
        math.sin(math.pi * Az / 180) /
        math.tan(math.pi * El / 180)) * 180 / math.pi + 90
    Yz = math.asin(
        math.cos(PI * Az / 180) * math.cos(PI * El / 180)) * 180 / PI + 90
    # 加入列表
    xz_list.append(Xz)
    yz_list.append(Yz)
    # 转换为固定长度的字符串
    Xz = '{:.3f}'.format(Xz)
    Xz = Xz.rjust(7, ' ')
    Yz = '%.3f' % Yz
    Yz = Yz.rjust(7, ' ')
    # 拼接格式
    # 年
    yyyy = line_list[0] + ' '
    # 月
    month = line_list[1]
    if '0' in month:
        month = month.replace('0', ' ')
    month = month + ' '
    # 日
    dd = line_list[2]
    if dd[0] == '0':
        dd = dd.replace('0', ' ')
    dd = dd + ' '
    # 时
    hh = line_list[3]
    if hh[0] == '0':
        hh = hh.replace('0', ' ')
    hh = hh + ' '
    # 分
    mm = line_list[4]
    if mm[0] == '0':
        mm = mm.replace('0', ' ')
    mm = mm + ' '
    # 秒
    ss = line_list[5].split('.')[0]
    ss = ss.rjust(2, ' ') + '   '
    # # XY轴
    # xxx = Xz + '  '
    # yyy = Yz + '  '
    # # AE角度
    # aaa = line_list[-3].rjust(8, ' ') + '  '
    # eee = line_list[-2].rjust(7, ' ')
    # 构成字符串
    lineXY = yyyy + month + dd + hh + mm + ss + '\n'
    xy_list.append(lineXY)

# 将列表复制8份
xy_list = [v for v in xy_list for i in range(8)]

# 插值
print(len(xz_list))
for i in range(len(xz_list)):
    if i < len(xz_list) - 1:
        step = xz_list[i + 1] - xz_list[i]
        stepy = yz_list[i + 1] - yz_list[i]
        stepa = az_list[i + 1] - az_list[i]
        stepe = el_list[i + 1] - el_list[i]
        # 计算插值，生成列表
        xz_interp_list = np.arange(xz_list[i], xz_list[i + 1], step / 8)
        # 转换为字符串列表
        xz_interp_list = [
            '{:.3f}'.format(v).rjust(7, ' ') for v in xz_interp_list
        ]
        yz_interp_list = np.arange(yz_list[i], yz_list[i + 1], stepy / 8)
        yz_interp_list = [
            '{:.3f}'.format(v).rjust(7, ' ') for v in yz_interp_list
        ]
        az_interp_list = np.arange(az_list[i], az_list[i + 1], stepa / 8)
        az_interp_list = [
            '{:.4f}'.format(v).rjust(8, ' ') for v in az_interp_list
        ]
        el_interp_list = np.arange(el_list[i], el_list[i + 1], stepe / 8)
        el_interp_list = [
            '{:.4f}'.format(v).rjust(7, ' ') for v in el_interp_list
        ]
        # 填入列表
        xz_value8_list.extend(xz_interp_list)
        yz_value8_list.extend(yz_interp_list)
        az_value8_list.extend(az_interp_list)
        el_value8_list.extend(el_interp_list)
    # if i == len(xz_list) - 1:
    #     l = []
    #     l.append(xz_list[i])
    #     xz_value8_list.extend(l * 8)
    #     l = []
    #     l.append(yz_list[i])
    #     yz_value8_list.extend(l*8)
print(len(az_value8_list))
print(len(yz_value8_list))
print(len(az_value8_list))
print(len(el_value8_list))
# print(xz_value8_list)
# 用插值后的列表元素替换引导文件中的字段
for i in range(len(xz_value8_list)):
    line = xy_list[i]
    # print(i)
    line = line[:22] + xz_value8_list[i] + '  ' + yz_value8_list[
        i] + '  ' + az_value8_list[i] + '  ' + el_value8_list[i]+'\n'
    xy_value_list.append(line)
# for i in range(len(xz_value8_list)):
# xy_list[6] =
# 写入文件
with open('XY.dat', 'w') as fo:
    fo.writelines(xy_value_list)
