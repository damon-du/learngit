# -*- coding: UTF-8 -*-
'''
sniff实验
'''
from scapy.all import *


def pack_callback(packets):
    print('start sniff...')
    # print(packets[UDP].name)
    # print(packets[Raw].load)
    # print(packets[UDP].payload) # 返回udp包内数据
    # ss = packets[UDP].payload
    # ssstr = str(ss)
    # print(type(ss))
    # if packets[IP].sport == 977:
    # sd = packets[TCP].payload # 直接返回字符串类型bytes
    # print(packets[IP].sport)
    # print(packets[TCP]) # 返回包内udp部分数据
    # print(packets.payload) # 返回整包数据
    # print(packets[IP].src)
    # print(packets.payload.name)
    # print(packets.payload)
    # print(packets.summary()) # 返回概要
    # print(hexdump(packets)) # 返回整包数据的16进制表示
    # print(type(packets))
    # print(packets.dst) # 返回二层信息
    # print(packets.show())

if __name__ == "__main__":
    # sniff(iface='Realtek PCIe GBE Family Controller',filter='ip src 172.17.53.28',prn=pack_callback,count=0,store=0)
    sniff(iface='Realtek PCIe GBE Family Controller',filter='ip dst 172.17.53.28',prn=pack_callback,count=0,store=0)
    # sniff(iface='Realtek PCIe GBE Family Controller',filter='ip dst 172.17.57.28',prn=pack_callback,count=0,store=0)
    # sniff(iface='Realtek PCIe GBE Family Controller',filter='ip src 172.17.57.28',prn=pack_callback,count=0,store=0)
    # sniff(iface='Realtek PCIe GBE Family Controller',prn=pack_callback,count=0,store=0)
    # sniff(iface='Intel(R) I350 Gigabit Network Connection',prn=pack_callback,count=10,store=0)

