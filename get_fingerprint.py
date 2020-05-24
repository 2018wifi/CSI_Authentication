import time
import struct
import socket
import threading
import numpy as np
from parameter import *

matrix = np.zeros((FP_SIZE, NFFT), dtype=np.complex)    # 原始CSI矩阵
matrix_lock = threading.Lock()
finish_flag1 = False                                    # 接收完CSI的树莓派数量
finish_flag2 = False
finish_flag3 = False

send_flag = True                                        # UDP包发送控制标签


def get_fingerprint():
    global matrix
    global send_flag
    global FP_SIZE
    global RASP_STATE1
    global RASP_STATE2
    global RASP_STATE3

    matrix = np.zeros((FP_SIZE, NFFT), dtype=np.complex)
    '''请求树莓派发送CSI'''
    if RASP_STATE1:
        request_data(0)
    if RASP_STATE2:
        request_data(1)
    if RASP_STATE3:
        request_data(2)

    '''发送UDP包，强制目标设备发送稳定的CSI信息'''
    send_flag = True
    sender = threading.Thread(target=send_udp())
    sender.start()

    '''接收树莓派发送的CSI'''
    if RASP_STATE1:
        receiver_A = threading.Thread(target=receive_data, args=(0,))
        receiver_A.start()
    if RASP_STATE2:
        receiver_B = threading.Thread(target=receive_data, args=(1,))
        receiver_B.start()
    if RASP_STATE3:
        receiver_C = threading.Thread(target=receive_data, args=(2,))
        receiver_C.start()

    time_beg = int(round(time.time() * 1000))
    while (RASP_STATE1 and not finish_flag1) \
            or (RASP_STATE2 and not finish_flag2) \
            or (RASP_STATE3 and not finish_flag3):
        time_end = int(round(time.time() * 1000))
        if time_end - time_beg > TIMEOUT * 1000:                # 超时时，将超时的树莓派状态置为无效，同时将matrix缩小
            rasp_count_outdated = int(RASP_STATE1) + int(RASP_STATE2) + int(RASP_STATE3)
            if not finish_flag1:
                RASP_STATE1 = False
            if not finish_flag2:
                RASP_STATE2 = False
            if not finish_flag3:
                RASP_STATE3 = False
            rasp_count_new = int(RASP_STATE1) + int(RASP_STATE2) + int(RASP_STATE3)
            FP_SIZE = int((FP_SIZE / rasp_count_outdated) * rasp_count_new)   # 更新指纹大小
            new_matrix = np.zeros((FP_SIZE, NFFT), dtype=np.complex)
            bias = 0
            piece_count = FP_SIZE / rasp_count_new
            if RASP_STATE1:
                new_matrix[bias: bias + piece_count] = matrix[0: piece_count]
                bias += FP_SIZE / rasp_count_new
            if RASP_STATE2:
                new_matrix[bias: bias + piece_count] = matrix[piece_count: piece_count * 2]
                bias += FP_SIZE / rasp_count_new
            if RASP_STATE3:
                new_matrix[bias: bias + piece_count] = matrix[piece_count * 2: piece_count * 3]
            matrix = new_matrix
            break
        time.sleep(0.1)

    send_flag = False

    '''处理CSI成指纹'''
    preprocess_data()

    return matrix


'''
发送UDP给目标设备
'''


def send_udp():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    mes = ""  # 构造一定字节的内容
    for i in range(0, BYTE_NUM + 1):
        mes += str(i)

    ts = int(time.time() * 1000)
    interval = 1000 / float(RATE)

    print("UDP发送开始")
    while send_flag:
        if int(time.time() * 1000) < ts + interval:
            continue
        else:
            ts += interval

        udp_socket.sendto(mes.encode(), (TARGET_IP, NEW_DEVICE_PORT))
        # print("Have sent a packet to ", TARGET_IP, "\tts: ", int(time.time() * 1000))
    print("UDP发送结束")


'''
请求树莓派发送CSI
'''


def request_data(rasp_num):
    tcp_ip = None
    if rasp_num == 0:
        tcp_ip = RASP_IP1
    elif rasp_num == 1:
        tcp_ip = RASP_IP2
    elif rasp_num == 2:
        tcp_ip = RASP_IP3
    tcp_port = RASP_PORT
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((tcp_ip, tcp_port))

    mes = TARGET_MAC + " " + str(FP_SIZE / 3)         # 目标地址: 包数

    tcp_socket.send(mes.encode())
    reply = tcp_socket.recv(4096)
    tcp_socket.close()
    if reply != "OK":
        print("ERROR: 请求树莓派" + rasp_num + "发送CSI时返回错误!")
        return False
    else:
        return True


'''
接收CSI包
'''


def receive_data(rasp_num):  # 参数为树莓派编号
    global matrix
    global finish_count

    port = None
    if rasp_num == 0:
        port = SERVER_PORT1
    elif rasp_num == 1:
        port = SERVER_PORT2
    elif rasp_num == 2:
        port = SERVER_PORT3

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("", port))

    dst_count = FP_SIZE / 3  # 目标接收数量

    for i in range(dst_count):
        buffer = udp_socket.recv(1024)
        if len(buffer) != 274:  # 舍弃大小不正确的包
            continue
        data = parse(buffer)
        vector = read_csi(data)

        with matrix_lock:
            matrix[i + (dst_count * num)] = vector

    with matrix_lock:
        finish_count += 1


'''
预处理数据
'''


def preprocess_data():
    global matrix

    for i in range(matrix.shape[0]):
        for j in [0, 29, 30, 31, 32, 33, 34, 35]:  # 部分子载波幅值置零
            matrix[i][j] = 0
        csi_max = matrix[i].max()  # 归一化
        for k in range(matrix.shape[1]):
            matrix[i][k] = matrix[i][k] / csi_max

    return


'''
处理CSI的工具函数
'''


def parse(buffer):  # 解析二进制流
    nbyte = int(len(buffer))  # 字节数
    data = np.array(struct.unpack(nbyte * "B", buffer), dtype=np.uint8)

    return data


def read_header(data):  # 提取头信息
    header = {}

    header["magic_bytes"] = data[:4]
    header["source_mac"] = data[4:10]
    header["sequence_number"] = data[10:12]

    coreSpatialBytes = int.from_bytes(data[12:14], byteorder="little")
    header["core"] = [int(coreSpatialBytes & x != 0) for x in range(3)]
    header["spatial_stream"] = [int(coreSpatialBytes & x != 0) for x in range(3, 6)]

    header["channel_spec"] = data[14:16]
    header["chip"] = data[18:20]

    return header


def read_csi(data):  # 提取CSI信息，并转换成矩阵
    csi = np.zeros(NFFT, dtype=np.complex)
    sourceData = data[18:]
    sourceData.dtype = np.int16
    csi_data = sourceData.reshape(-1, 2).tolist()

    i = 0
    for x in csi_data:
        csi[i] = np.complex(x[0], x[1])
        i += 1

    return csi

# '''插值算法'''

# def fill_blanks(pmatrix, ptlist):
#     blank_count = [-1, -1, -1]
#     for i in range(50):
#         if ptlist[i] == 0 and blank_count[0] == -1:
#             blank_count[0] = 50 - i
#         if ptlist[i + 50] == 0 and blank_count[1] == -1:
#             blank_count[1] = 100 - (i + 50)
#         # if ptlist[i + 100] == 0 and blank_count[2] == -1:
#         #     blank_count[2] = 150 - (i + 100)
#     if blank_count[0] == -1:
#         blank_count[0] = 0
#     if blank_count[1] == -1:
#         blank_count[1] = 0
#     if blank_count[2] == -1:
#         blank_count[2] = 0
#     while(blank_count[0] != 0 or blank_count[1] != 0 or blank_count[2] != 0):
#         fill(blank_count, pmatrix, ptlist)


# def fill(blank_count, pmatrix, ptlist):
#     max_interval = [0, 0, 0]
#     max_interval_index = [-1, -1, -1]
#     for i in range(1, 50):
#         if blank_count[0] != 0:
#             if ptlist[i] != 0:
#                 interval = ptlist[i] - ptlist[i - 1]
#                 if interval >= max_interval[0]:
#                     max_interval[0] = interval
#                     max_interval_index[0] = i
#         if blank_count[1] != 0:
#             if ptlist[i + 50] != 0:
#                 interval = ptlist[i + 50] - ptlist[i + 50 - 1]
#                 if interval >= max_interval[1]:
#                     max_interval[1] = interval
#                     max_interval_index[1] = i + 50
#         if blank_count[2] != 0:
#             if ptlist[i + 100] != 0:
#                 interval = ptlist[i + 100] - ptlist[i + 100 - 1]
#                 if interval >= max_interval[2]:
#                     max_interval[2] = interval
#                     max_interval_index[2] = i + 100
#
#     if max_interval_index[0] != -1:
#         i = 49
#         while i != max_interval_index[0]:                       # 在max_interval_index处插入均值
#             pmatrix[i] = pmatrix[i - 1]
#             ptlist[i] = ptlist[i - 1]
#             i -= 1
#         pmatrix[i] = (pmatrix[i - 1] + pmatrix[i]) / 2
#         ptlist[i] = (ptlist[i - 1] + ptlist[i]) / 2
#         blank_count[0] -= 1
#     if max_interval_index[1] != -1:
#         i = 99
#         while i != max_interval_index[1]:  # 在max_interval_index处插入均值
#             pmatrix[i] = pmatrix[i - 1]
#             ptlist[i] = ptlist[i - 1]
#             i -= 1
#         pmatrix[i] = (pmatrix[i - 1] + pmatrix[i]) / 2
#         ptlist[i] = (ptlist[i - 1] + ptlist[i]) / 2
#         blank_count[1] -= 1
#     if max_interval_index[2] != -1:
#         np.insert(pmatrix, max_interval_index[2],
#                   (pmatrix[max_interval_index[2]] + pmatrix[max_interval_index[2] - 1]) / 2)
#         np.insert(ptlist, max_interval_index[2],
#                   (ptlist[max_interval_index[2]] + ptlist[max_interval_index[2] - 1]) / 2)
#         blank_count[2] -= 1
