'''
卷积编码
'''

import numpy
from numpy import array
import commpy.channelcoding.convcode as cc
import math


# 编码函数
def encode(message: bytes, gen: list, m: int, g2reverse = False, puncture_matrix = None):
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
    # 没找到G2反相的参数，先编码，再对G2反相，再打孔
    # 可选的参数termination，对应编码过程中的尾码，选择‘term’输出尾码，选择'cont'咬尾，不输出尾码
    array_bits_convcoded = cc.conv_encode(array_bits_message,
                                          trellis,
                                          termination='term')
    print(array_bits_convcoded, len(array_bits_convcoded))
    # 如果G2反相，进行处理
    if g2reverse:
        for i in range(int(len(array_bits_convcoded)/2)):
            array_bits_convcoded[2*i+1] -= 1
    array_bits_convcoded = abs(array_bits_convcoded)
    print(array_bits_convcoded, len(array_bits_convcoded))
    
    # 打孔处理
    if puncture_matrix is not None:
        # 构建打孔矩阵
        try:
            p = numpy.array(puncture_matrix)
        except:
            print('打孔矩阵不正确,请检查')
        # 组合起来，构建bool列表，实现打孔
        pm = p.T.flatten()
        P_m_bool = pm > 0
        times = math.ceil(len(array_bits_convcoded) / len(P_m_bool))
        # 扩展bool矩阵到数据长度
        P_m_bool = numpy.tile(P_m_bool, times)[:len(array_bits_convcoded)]
        # 打孔
        puncture_result = array_bits_convcoded[P_m_bool]
        array_bits_convcoded = puncture_result
        print(array_bits_convcoded)

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
    pun_matrix = [[1,1,0], [1,0,1]]
    bytes_encoded = encode(ms_bytes, gen, m, g2reverse=True,puncture_matrix=pun_matrix)
    print(bytes_encoded)
