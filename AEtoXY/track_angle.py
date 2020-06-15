# 转换生成测角数据

with open('hz2.txt','r') as fi:
    lines = fi.readlines()

for line in lines:
    line_list = line.split(' ')
    line_list = [i for i in line_list if i != '']
    # 获取Az和El
    Az = float(line_list[-3])
    El = float(line_list[-2])
    ZT = 