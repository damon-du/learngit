from commpy.utilities import *
import commpy.channelcoding.turbo as tb

int_n = 0x8F55

ba = dec2bitarray(int_n,8)
print(ba)

bi = bitarray2dec(ba)
print(bi)