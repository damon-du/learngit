from reedsolo import RSCodec

# rsc = RSCodec(prim=0x13,c_exp=4)
rsc = RSCodec(10)
print(rsc.gf_log)
# msg_encoded = rsc.encode([1, 2, 3, 4])
# print(msg_encoded)

msg_coded = rsc.encode(b'hello world')
print(msg_coded)
# b'hello world\xed%T\xc4\xfd\xfd\x89\xf3\xa8\xaa'

msd_dcd = b'hello world\xed%T\xe4\xfd\xcd\x99\xf3\xa9\xbb'
msg_decoded = rsc.decode(msd_dcd)  # 能纠正5个字节的错误
# 返回三个变量
# 1.the decoded (corrected) message
# 2.the decoded message and error correction code (which is itself also corrected)
# 3.and the list of positions of the errata (errors and erasures)
# (bytearray(b'hello world'), bytearray(b'hello world\xed%T\xc4\xfd\xfd\x89\xf3\xa8\xaa'), bytearray(b'\x14\x13\x11\x10\x0e'))
# print(msg_decoded[0])

print(msg_decoded)
print('错误位置：', list(msg_decoded[2]))

# rsc.decode(b'helXXXXXXXXXXy\xb2XX\x01q\xb9\xe3\xe2=', erase_pos=[3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 16])[0]  # 12 erasures - OK
# b'hello world'
# This shows that we can decode twice as many erasures (where we provide the location of errors ourselves) than errors (with unknown locations). This is the cost of error correction compared to erasure correction.

rsc = RSCodec(32, c_exp=8)
# rsc = RSCodec(32,nsize=256)
print(rsc.gf_log)
print(rsc.maxerrata(verbose=True))  # 最大纠错数量

# 初始化计算表
import reedsolo as rs
rs.init_tables(prim=0x13, generator=2, c_exp=4)  # 默认值000100011101 GF(2^8)
print(rs.gf_log)
print(rs.gf_log.hex())
# Pro tip: if you get the error: ValueError: byte must be in range(0, 256), 
# please check that your prime polynomial is correct for your field. 
# Pro tip2: by default, you can only encode messages of max length and max symbol value = 256. 
# If you want to encode bigger messages, please use the following (where c_exp is the exponent of your Galois Field, eg, 12 = max length 2^12 = 4096):

# 获取本原多项式，如果已经本原多项式的构成，直接在初始化表的参数中写入
prim = rs.find_prime_polys(c_exp=4, fast_primes=True, single=True)  # 返回整形，变为二进制就是生成多项式的系数
rs.init_tables(c_exp=4,prim=prim)

# 返回所有的生成多项式
# 返回值是字典，key值就是ecc的长度
gen = rs.rs_generator_poly_all(15) 
print(gen)

# encode
# n = 255
# nsym = 32 # length of ecc
# mes = 'a'*(n-nsym)
# mseecc = rs.rs_encode_msg(mes,nsym,gen=gen[nsym])