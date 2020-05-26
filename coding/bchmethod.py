'''
BCH编码尝试，结果已经验证
'''


def encode(data: bytes, gen=0b11000101, regnum=7):
    '''
    默认为（63，56），生成多项式为X7+X6+X2+1
    默认gen=0b11000101,寄存器个数7
    每次输入7个字节，最终输出7字节+7比特监督码字
    不足7个字节，前补零
    :param data:待编码字节，固定为7字节
    :param gen:生成多项式
    :param regnum:寄存器个数
    '''
    # 数据长度
    datalength = len(data)*8
    # 寄存器初始值为零
    reg = 0
    # 寄存器掩码
    mask = 2 ** regnum - 1
    # 生成多项式的n-1位
    genShort = gen & mask
    # 字节变为数值
    mx = int.from_bytes(data,'big',signed=False)    
    # 初始化寄存器
    reg = mx >> (datalength-regnum)
    # 移动信息序列，作为被除数
    mx = mx << regnum

    for i in range(datalength):
        temp = (reg << 1) & mask
        bt_next = (mx >> (datalength-i-1)) & 0b1
        temp = temp | bt_next
        if (reg >> (regnum-1)) != 0:
            reg = temp ^ genShort
        else:
            reg = temp
        print('待运算值 is: ', bin(temp))
        print('寄存器运算后 is :', bin(reg))

    return reg


def cut(obj, sec):
    return [obj[i:i + sec] for i in range(0, len(obj), sec)]


if __name__ == "__main__":
    # data = 0b1000
    data = b'\x01\x02\x03\x04'
    # reg_value = encode(data, 0b10001001, 7)
    reg_value = encode(data, 0b101001, 5)
    print('reg value:',hex(reg_value))
    # 最终的bch码字
    reg_value = reg_value << 1
    bch_code = data + reg_value.to_bytes(1,'big',signed=False)
    print(bch_code)
