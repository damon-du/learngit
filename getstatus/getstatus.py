# -*- coding: UTF-8 -*-

from scapy.all import *
import socket
import time
import datetime
import threading
import socket
import struct
import sys
import traceback

dict_status = {}
dict_alarm = {}
dict_dmstatus = {}
dict_xdstatus = {}
dict_acustatus = {}
dict_status['SyW'] = []
dict_alarm['ACU'] = []
dict_alarm['BBE'] = []
dict_alarm['MOD'] = []

def pack_callback(packets):
    # print(packets[UDP].name)
    # print(packets[Raw].load)
    # print(packets[UDP].payload) # 返回udp包内数据
    # ss = packets[UDP].payload
    # ssstr = str(ss)
    # print(type(ss))
    # sd = packets[TCP].load # 直接返回字符串类型bytes
    # print(packets[UDP]) # 返回包内udp部分数据
    # print(packets.payload) # 返回整包数据
    # print(packets[IP].src)
    # print(packets.payload.name)
    # print(packets.payload)
    # print(packets.summary())  # 返回概要
    # print(hexdump(packets)) # 返回整包数据的16进制表示
    # print(type(packets))
    # print(packets.dst) # 返回二层信息
    # print(packets.show())

    # ACU 状态数据
    if packets[IP].src == '172.30.61.26':
        try:
            sd = packets[TCP].load
            pstr = str(sd, encoding='utf8')
            get_acu_status(pstr)
        except Exception as ex:
            pass
            # print(str(ex))
    # 串口服务器传送的信道设备的状态数据
    if packets[IP].src == '172.30.61.32':
        try:
            sd = packets[TCP].load
            pstr = sd.decode()
            get_channel_status(packets[TCP].sport, pstr)
        except Exception as ex:
            # print(str(ex))
            pass


def get_channel_status(sport, pstr=''):
    '''
    获取信道状态
    '''
    pstr = pstr.replace('\r\n', '')
    global dict_acustatus
    dict_acustatus = {}
    if 'CF' in pstr:
        list_convert = pstr.split(',')
        if sport == 954:
            # 数传2-左旋频率
            dt2f = 11000 - \
                float(list_convert[0].split('_')[1].replace('\r\n', ''))
            dict_xdstatus['DT2F'] = str(dt2f)
            # 数传2极化方式-左旋
            dict_xdstatus['DT2P'] = 'Left'
        if sport == 955:
            # 数传1-右旋频率
            dt1f = 11000 - \
                float(list_convert[0].split('_')[1].replace('\r\n', ''))
            dict_xdstatus['DT1F'] = str(dt1f)
            # 数传1极化方式-右旋
            dict_xdstatus['DT1P'] = 'Right'
        # 遥测频率
        if sport == 953:
            tcdf = 11000 - \
                float(list_convert[0].split('_')[1].replace('\r\n', ''))
            dict_xdstatus['TCDF'] = str(tcdf)
        # 遥控频率
        if sport == 952:
            dict_xdstatus['TCUF'] = list_convert[0].split(
                '_')[1].replace('\r\n', '')
        # 跟踪频率
        if sport == 950:
            antf = 11000 - \
                float(list_convert[0].split('_')[1].replace('\r\n', ''))
            dict_xdstatus['AnTF'] = str(antf)
    # 上行极化
    if sport == 956:
        if '0' in pstr:
            dict_xdstatus['TCUP'] = 'L'
        else:
            dict_xdstatus['TCUP'] = 'R'


def get_acu_status(pstr=''):
    '''
    获取ACU状态
    '''
    global dict_acustatus
    dict_acustatus = {}
    list_ACU_status = pstr.split(',')
    # 方位俯仰
    # str_acustatus = '方位值:{0}  俯仰值：{1}  '.format(
    #     list_ACU_status[3], list_ACU_status[4])
    dict_acustatus['AnAS'] = (list_ACU_status[3])
    dict_acustatus['AnES'] = (list_ACU_status[4])
    acus = ''
    if list_ACU_status[5] == 'W':
        acus = '待机'
    if list_ACU_status[5] == 'P':
        acus = '程引'
    if list_ACU_status[5] == 'S':
        acus = '搜索'
    if list_ACU_status[5] == 'M':
        acus = '手动'
    if list_ACU_status[5] == 'A':
        acus = '自跟'
    # str_acustatus += acus
    # ACU状态，包含告警
    dict_acustatus['AnS'] = acus

    # 轴状态
    xzstus = ''
    yzstus = ''
    SyW = []
    if (int(list_ACU_status[8]) & 1) == 1:
        xzstus = '  西限位'
        SyW.append('西限位')
    if (int(list_ACU_status[8]) & 2) == 2:
        xzstus = '  东限位'
        SyW.append('东限位')
    if (int(list_ACU_status[8]) & 4) == 4:
        xzstus = '  X轴伺服使能'
    if (int(list_ACU_status[8]) & 8) == 8:
        xzstus = '  X轴伺服告警'
        SyW.append('X轴伺服告警')
    if (int(list_ACU_status[9]) & 1) == 1:
        yzstus = '  南限位'
        SyW.append('南限位')
    if (int(list_ACU_status[9]) & 2) == 2:
        yzstus = '  北限位'
        SyW.append('北限位')
    if (int(list_ACU_status[9]) & 4) == 4:
        yzstus = '  Y轴伺服使能'
    if (int(list_ACU_status[9]) & 8) == 8:
        yzstus = '  Y轴伺服告警'
        SyW.append('Y轴伺服告警')
    if SyW:
        dict_alarm['ACU'] = SyW
    else:
        dict_alarm['ACU'] = []
    # 接收极化
    if 'X' in list_ACU_status[-3]:
        AnTA = str(round(int(list_ACU_status[6])/51, 2))+'V'
        dict_acustatus['AnTA'] = AnTA
        dict_acustatus['TCDP'] = list_ACU_status[11]
    if 'S' in list_ACU_status[-3]:
        AnTA = str(round(int(list_ACU_status[7])/51, 2))+'V'
        dict_acustatus['AnTA'] = AnTA
        dict_acustatus['TCDP'] = list_ACU_status[12]
    # str_acustatus += xzstus
    # str_acustatus += yzstus

    # print(dict_status)


def pack_bbe():
    sniff(iface='Intel(R) I350 Gigabit Network Connection',
          filter='udp', prn=pack_callback, count=0)


def get_bytes_time():
    dt_now = datetime.datetime.now()
    y = dt_now.year
    m = dt_now.month
    d = dt_now.day
    dt_start = datetime.datetime(y, m, d, 0, 0, 0)
    dt_delta = dt_now-dt_start
    integral_Seconds = dt_delta.seconds*10
    btime = integral_Seconds.to_bytes(
        length=4, byteorder='little', signed=False)
    stime = btime.hex()
    return btime


def produce_stop_bat(pid, tmpfile="stop_xxx.bat"):
    '''
    生成自动关闭文件
    :param pid : 自身的pid
    :param timefile : 文件名字符串
    '''
    # 待写入内容
    stop_cmd = 'taskkill /pid ' + str(pid) + ' /f'  # 关闭指定进程
    del_self_cmd = "del %0"  # 删除自身文件
    # 文件路径和名称
    tmp_all = "stop_" + tmpfile + ".bat"
    # 写入文件
    with open(file=tmp_all, mode="w") as f:
        f.write(stop_cmd + "\n" + del_self_cmd)


def pack_auto_recieve():
    '''
    抓取ACU、信道、解调器数据包
    '''
    sniff(iface='Intel(R) I350 Gigabit Network Connection',
          filter='ip src 172.30.61.26 or ip src 172.30.61.32 or ip src 172.30.61.21', prn=pack_callback, count=0,store=0)


def int_to_four_string(flength=20):
    return int.to_bytes(flength, length=4, byteorder='big', signed=True).hex()


def cut(obj, sec):
    return [obj[i:i + sec] for i in range(0, len(obj), sec)]


def bytes_to_float(b):
    f = struct.unpack("!f", b)[0]
    return f


def bytes_to_int(b):
    i = int.from_bytes(b, byteorder='big', signed=False)
    return i


def get_demode_status():
    '''
    通过发送TCP指令获取解调器状态
    '''
    host = '172.30.61.22'
    port = 3000
    addr = (host, port)
    buffsize = 1024
    frame_start = '499602d2'
    frame_length = int_to_four_string(20)
    frame_flowid = '00000000'
    frame_end = 'b669fd2e'
    # 帧模块ID
    frame_module_id = '00003010'
    list_module_id = ['00003010', '00003011',
                      '00003070', '00003071', '00003072', '00003073','00003001']
    global dict_alarm
    global dict_dmstatus

    while True:
        tcpsk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dict_dmstatus = {}
        try:
            tcpsk.connect(addr)

            for mid in list_module_id:
                cmd_checkstatus = frame_start + frame_length + frame_flowid + mid + frame_end
                # cmd_checkstatus = frame_start + frame_length + frame_flowid + frame_module_id + frame_end
                # print(cmd_checkstatus)
                cmdBytes = bytes.fromhex(cmd_checkstatus)
                tcpsk.send(cmdBytes)
                # 获取返回
                d = tcpsk.recv(buffsize)
                # 列表，各偏移量对应响应，此处会在tcp连接断开的时候报错，本程序未进行判断处理
                list_bytes_recieve = cut(d, 4)
                frame_resp_mid = list_bytes_recieve[3]

                # 解调消息块1
                if (frame_resp_mid == b'\x00\x00\x30\x10'):
                    dict_dmstatus['DT1L'] = ''
                    # Viterbi锁定
                    vtb = list_bytes_recieve[52]
                    if (vtb == 1 or vtb == 2 or vtb == 3):
                        dict_dmstatus['DT1L'] = 'B'
                    # 载波是否锁定,如果Viterbi锁定则不改变值
                    if dict_dmstatus['DT1L']:
                        pass
                    else:
                        if (bytes_to_int(list_bytes_recieve[46]) == 2):
                            dict_dmstatus['DT1L'] = 'C'
                        else:
                            dict_dmstatus['DT1L'] = 'U'
                    # Eb/N0
                    dict_dmstatus['DT1E'] = str(
                        round(bytes_to_float(list_bytes_recieve[47]), 2))
                    # 多普勒
                    dict_dmstatus['DT1D'] = str(
                        round(bytes_to_float(list_bytes_recieve[44])/1000, 2))
                # 解调消息块2
                if (frame_resp_mid == b'\x00\x00\x30\x11'):
                    dict_dmstatus['DT2L'] = ''
                    # Viterbi锁定
                    vtb = list_bytes_recieve[52]
                    if (vtb == 1 or vtb == 2 or vtb == 3):
                        dict_dmstatus['DT2L'] = 'B'
                    # 载波是否锁定,如果Viterbi锁定则不改变值
                    if dict_dmstatus['DT2L']:
                        pass
                    else:
                        if (bytes_to_int(list_bytes_recieve[46]) == 2):
                            dict_dmstatus['DT2L'] = 'C'
                        else:
                            dict_dmstatus['DT2L'] = 'U'
                    # Eb/N0
                    dict_dmstatus['DT2E'] = str(
                        round(bytes_to_float(list_bytes_recieve[47]), 2))
                    # 多普勒
                    dict_dmstatus['DT2D'] = str(
                        round(bytes_to_float(list_bytes_recieve[44])/1000, 2))
                # 数据处理消息块-通道1-I支路
                if (frame_resp_mid == b'\x00\x00\x30\x70'):
                    # 帧同步状态
                    ztb = bytes_to_int(list_bytes_recieve[52])
                    if ztb == 2:
                        dict_dmstatus['DT1IF'] = 'T'
                    else:
                        dict_dmstatus['DT1IF'] = 'F'
                # 数据处理消息块-通道1-Q支路
                if (frame_resp_mid == b'\x00\x00\x30\x71'):
                    # 帧同步状态
                    ztb = bytes_to_int(list_bytes_recieve[52])
                    if ztb == 2:
                        dict_dmstatus['DT1QF'] = 'T'
                    else:
                        dict_dmstatus['DT1QF'] = 'F'
                # 数据处理消息块-通道2-I支路
                if (frame_resp_mid == b'\x00\x00\x30\x72'):
                    # 帧同步状态
                    ztb = bytes_to_int(list_bytes_recieve[52])
                    if ztb == 2:
                        dict_dmstatus['DT2IF'] = 'T'
                    else:
                        dict_dmstatus['DT2IF'] = 'F'
                # 数据处理消息块-通道2-Q支路
                if (frame_resp_mid == b'\x00\x00\x30\x73'):
                    # 帧同步状态
                    ztb = bytes_to_int(list_bytes_recieve[52])
                    if ztb == 2:
                        dict_dmstatus['DT2QF'] = 'T'
                    else:
                        dict_dmstatus['DT2QF'] = 'F'
                # 全局消息快
                if (frame_resp_mid == b'\x00\x00\x30\x01'):
                    # 告警
                    dict_alarm['MOD'] = []
                    # 调制模块
                    tzmk = bytes_to_int(list_bytes_recieve[28])
                    if (tzmk & 1) == 0:
                        dict_alarm['MOD'].append('调制模块1未加载')                    
                    # 数据处理模块
                    sjclmk = bytes_to_int(list_bytes_recieve[29])
                    if (sjclmk & 1) == 0:
                        dict_alarm['MOD'].append('数据处理模块1未加载')
                    if (sjclmk & 2) == 0:
                        dict_alarm['MOD'].append('数据处理模块2未加载')
                    if (sjclmk & 4) == 0:
                        dict_alarm['MOD'].append('数据处理模块3未加载')
                    if (sjclmk & 8) == 0:
                        dict_alarm['MOD'].append('数据处理模块4未加载')
                    # 解调模块
                    jtmk = bytes_to_int(list_bytes_recieve[30])
                    if (jtmk & 1) == 0:
                        dict_alarm['MOD'].append('解调模块2未加载')
                    # 数据记录消息块
                    sjjlmk = bytes_to_int(list_bytes_recieve[31])
                    if (sjjlmk & 1) == 0:
                        dict_alarm['MOD'].append('数据记录模块1未加载')
                    if (sjjlmk & 2) == 0:
                        dict_alarm['MOD'].append('数据记录模块2未加载')
                    # 解调模块状态
                    jtmkzt = bytes_to_int(list_bytes_recieve[34])
                    if (jtmkzt & 1) == 1:
                        dict_alarm['MOD'].append('解调通道1无响应')
                    if (jtmkzt & 2) == 1:
                        dict_alarm['MOD'].append('解调通道2无响应')
                    # 警告
                    jg = bytes_to_int(list_bytes_recieve[40])
                    if (jg & 8) == 1:
                        dict_alarm['MOD'].append('解调硬件异常')
                    if (jg & 16) == 1:
                        dict_alarm['MOD'].append('调制硬件异常')
                    if (jg & 65536) == 1:
                        dict_alarm['MOD'].append('温度异常')
            tcpsk.close()
        except Exception as e:
            tcpsk.close()
            dict_dmstatus = {}
            dict_alarm['MOD'] = ['解调器未连接']
            print('Demod is not connected!')
            # print(repr(e))
            # print(traceback.print_exc())
            print(traceback.format_exc())
            time.sleep(5)
        time.sleep(1)


if __name__ == "__main__":
    # 进程号
    pid = os.getpid()
    # 本文件名（不含后缀.py）
    myfilename = os.path.split(__file__)[-1].split(".")[0]
    # 生成关闭进程的脚本文件
    produce_stop_bat(pid, myfilename)

    t_auto = threading.Thread(target=pack_auto_recieve)
    t_auto.start()

    t_tcp = threading.Thread(target=get_demode_status)
    t_tcp.start()

    # 发送状态数据
    sat = 'FFFFFFFF'
    byte_sat = bytes.fromhex(sat)
    byte_type = bytes.fromhex('C8112660')
    byte_device = bytes.fromhex('13000000')
    byte_res = bytes.fromhex('00000000')

    while True:
        byte_time = get_bytes_time()
        byte_head = byte_time+byte_sat+byte_type+byte_device+byte_res
        dict_status = {}
        
        # 处理告警信息
        dict_status['SyW'] = []
        for device in dict_alarm:
            if dict_alarm[device]:
                dict_status['SyW'] += dict_alarm[device]

        # 合并字典
        dict_status.update(dict_dmstatus)
        dict_status.update(dict_acustatus)
        dict_status.update(dict_xdstatus)
        dict_status.update(dict_dmstatus)
        
        # 构建状态字符串
        str_dict = '#'
        for key in dict_status:
            if (type(dict_status[key]) == list):
                if dict_status[key]:                    
                    str_list = ''
                    for k in dict_status[key]:
                        str_list = str_list + k + '@'
                    str_list = str_list[0:-1]
                    str_dict = str_dict + key + '@' + str_list + '#'
                else:
                    pass
            else:
                str_dict = str_dict + key + '@' + dict_status[key] + '#'
        str_status = str_dict[0:-1] + '$'
        # print(str_status)
        byte_status = bytes(str_status, encoding='utf-8')
        data_length = len(byte_status)
        byte_length = data_length.to_bytes(
            length=4, byteorder='little', signed=False)
        byte_frame_status = byte_head + byte_length + byte_status
        sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sk.sendto(byte_frame_status, ('172.17.3.25', 10001))
        sk.close()
        # print(byte_frame_status)
        # print(len(byte_frame_status))
        print(datetime.datetime.now())
        print(dict_status)


        time.sleep(1)
