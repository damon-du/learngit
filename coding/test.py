from numpy import array
import numpy
import math

# data = [[1,2],[3,4],[5,6]]
# x = numpy.array(data)
# print(x)
# print(x[0,1])
# print(x[numpy.ix_([0,1],[1,0])])
# print(x.swapaxes(1,0))
# print(x.transpose(1,0))
# print(x.T)

x = numpy.ones((1,2)) #创建一维长度为2，二维长度为3的二维0数组
print(x)

# y = numpy.arange(6)
# print(y)
# z = y.reshape((2,3))
# print(z)
# print(z[[0,1],[0,1]])

# x = numpy.array([[1, 2, 3], [4, 5, 6]])
# y = numpy.array([[7, 8, 9], [10, 11, 12]])
# print(numpy.concatenate([x,y],axis=0))
# print(numpy.concatenate([x,y],axis=1))
# print(numpy.vstack((x,y)),'vstack')
# print(numpy.hstack((x,y)))
# print('dstack',numpy.dstack((x,y)))
# print(numpy.split(x,2,axis=0))
# print(numpy.split(x,3,axis=1))
# # 数组元素的重复操作
# print(numpy.tile(x,(2,2)))
# print(numpy.tile(x,2))
p = numpy.array([[1, 1, 0], [1, 0, 1]])
print('p is ')
print(p)
print('组合')
print(p.T.flatten())  # 组合起来，然后对数据打孔
pm = p.T.flatten()
# puncture_m = numpy.where(pm>0,True,False)
# 构造bool数组
p_m = pm > 0
print('p_m is', p_m)
ms_bytes = b'\xaa'
ms_bits = numpy.unpackbits(bytearray(ms_bytes))
# ms_bits = numpy.arange(10)

print(ms_bits)
times = math.ceil(len(ms_bits) / len(p_m))
p_m = numpy.tile(p_m, times)[:len(ms_bits)]
print(p_m)
print(ms_bits[p_m])

if p.any():
    print('puncture')
else:
    print('nothing')


# print(p.transpose())
