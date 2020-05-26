'''
卷积编码
'''

import numpy
from numpy import array
import commpy.channelcoding.convcode as cc


# 编码函数
# todo：G2反相；打孔
def encode(message: bytes, gen: list, m: int, g2reverse = False):
    '''
    卷积编码,返回编码后字节
    :param message:待编码字节
    :param gen:生成多项式列表
    :param m:寄存器个数
    :param g2reverse:g2是否反相
    '''
    # 将输入字节变为比特数组
    array_bits_message = numpy.unpackbits(bytearray(message))
    # 构造生成树
    memory = array([m])
    g_matrix = array([gen])
    trellis = cc.Trellis(memory, g_matrix)
    # print(trellis.next_state_table)
    # 编码,返回比特数组
    # 可选的参数termination，对应编码过程中的尾码，选择‘term’输出尾码，选择'cont'咬尾，不输出尾码
    array_bits_convcoded = cc.conv_encode(array_bits_message,
                                          trellis,
                                          termination='term')
    print(array_bits_convcoded, len(array_bits_convcoded))
    if g2reverse:
        for i in range(int(len(array_bits_convcoded)/2)):
            array_bits_convcoded[2*i+1] -= 1
    array_bits_convcoded = abs(array_bits_convcoded)
    print(array_bits_convcoded, len(array_bits_convcoded))
    
    # 将比特数组转换为字节数组
    array_bytes_convcoded = numpy.packbits(array_bits_convcoded)
    # 转换为字节
    bytes_convcoded = bytes(array_bytes_convcoded)
    # 返回编码结果，字节形式
    return bytes_convcoded


if __name__ == "__main__":
    ms_bytes = b'\xd8'
    # 目前看生成多项式反着写？？？还需要验证
    gen = [0b11001, 0b10111]
    # gen = [0b10011, 0b11101]

    # 寄存器个数，可以多写，不能少写
    m = 4
    bytes_encoded = encode(ms_bytes, gen, m, g2reverse=True)
    print(bytes_encoded)
