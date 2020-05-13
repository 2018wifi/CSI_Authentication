import time
import copy
import struct
import socket
import threading
import numpy as np
from parameter import *

from main import queue1 as queue
from main import lock1 as lock

lock1 = threading.Lock()
reset = False                                            # 三个接收CSI包的线程是否从头开始写入缓冲区
matrix = np.zeros((PCAP_SIZE, NFFT), dtype=np.complex)   # 缓冲区
tlist = np.zeros((PCAP_SIZE), dtype=np.long)             # 和缓冲区中每一行对应的时间戳表，精度是毫秒级


def get_data():
    receiver_A = threading.Thread(target=receive_data, args=(0,))
    receiver_A.start()
    receiver_B = threading.Thread(target=receive_data, args=(1,))
    receiver_B.start()
    receiver_C = threading.Thread(target=receive_data, args=(2,))
    receiver_C.start()
    receiver_C = threading.Thread(target=receive_data, args=(2,))
    receiver_C.start()

    preprocesser = threading.Thread(target=preprocess_data)
    preprocesser.start()

'''接收CSI包'''

def receive_data(num):          # 参数为对接的树莓派编号
    wriPos = 50 * num           # 缓冲区指针（指向下一个要写入CSI的位置）

    if num == 0:
        port = PORT1
    elif num == 1:
        port = PORT2
    elif num == 2:
        port = PORT3
    
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(("", port))
    tcp_socket.listen(128)

    print("waiting...")

    client_socket, _ = tcp_socket.accept()

    print("connected successfully in port: ", port)

    while True:
        buffer = client_socket.recv(65535)
        data = parse(buffer)
        vector = read_csi(data)

        with lock1:
            if reset:                       # 检查是否重置
                wriPos = 50 * num
                reset = False

            if wriPos < 50 * (num + 1):     # 写入缓冲区（溢出的包丢弃）
                matrix[wriPos] = vector
                tlist[wriPos] = int(round(time.time() * 1000))      # 记录时间戳
                print(num, "\twrite a line in buffer")
    # tcp_socket.close()

'''预处理数据'''

def preprocess_data():
    global reset
    global matrix
    global tlist
    ls = int(time.time())       # 上一秒
    ns = int(time.time())       # 当前秒
    while True:
        if ns != ls:            # 跨越到新的一秒时
            print("new second: ", ns)
            ls = ns
            with lock1:
                pmatrix = copy.deepcopy(matrix)
                ptlist = copy.deepcopy(tlist)
                reset = True
                matrix = np.zeros((PCAP_SIZE, NFFT), dtype=np.complex)
                tlist = np.zeros((PCAP_SIZE), dtype=np.long)
                print("Copied the matrix and tlist")
            pmatrix = np.abs(pmatrix)               # 将复数矩阵求模运算
            fill_blanks(pmatrix, ptlist)            # 插值
            print("fill the blank")
            for i in range(pmatrix.shape[0]):       # 幅值置零，归一化
                for j in [0, 29, 30, 31, 32, 33, 34, 35]:
                    pmatrix[i][j] = 0     
                csi_max = pmatrix[i].max()
                for k in range(pmatrix.shape[1]):
                    pmatrix[i][k] = pmatrix[i][k] / csi_max
            print("set 0 to some column and normalization")
            print("result:\n", pmatrix)
            with lock:
                queue.put(pmatrix)          # 将处理好的数据插入队列中
                print("put the data to queue")
        ls = int(time.time())
        ns = int(time.time())


'''处理CSI的工具函数'''

def parse(buffer):      # 解析二进制流
    nbyte = int(len(buffer))        # 字节数
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

def read_csi(data):     # 提取CSI信息，并转换成矩阵
    csi = np.zeros(NFFT, dtype=np.complex)
    sourceData = data[18:]
    sourceData.dtype = np.int16
    csi_data = sourceData.reshape(-1, 2).tolist()

    i = 0
    for x in csi_data:
        csi[i] = np.complex(x[0], x[1])
        i += 1

    return csi

'''插值算法'''

def fill_blanks(pmatrix, ptlist):
    blank_count = [-1, -1, -1] 
    for i in range(50):
        if ptlist[i] == 0 and blank_count[0] == -1:
            blank_count[0] = 50 - i
        if ptlist[i + 50] == 0 and blank_count[1] == -1:
            blank_count[1] = 100 - i
        if ptlist[i + 100] == 0 and blank_count[2] == -1:
            blank_count[2] = 150 - i    
    if blank_count[0] == -1:
        blank_count[0] = 0
    if blank_count[1] == -1:
        blank_count[1] = 0
    if blank_count[2] == -1:
        blank_count[2] = 0

    
def fill(blank_count, pmatrix, ptlist):
    max_interval = [0, 0, 0]
    max_interval_index = [-1, -1, -1]
    for i in range(1, 50):
        if blank_count[0] != 0:
            if ptlist[i] != 0:
                interval = ptlist[i] - ptlist[i - 1]
                if interval >= max_interval[0]:
                    max_interval[0] = interval
                    max_interval_index[0] = i
        if blank_count[1] != 0:
            if ptlist[i + 50] != 0:
                interval = ptlist[i + 50] - ptlist[i + 50 - 1]
                if interval >= max_interval[1]:
                    max_interval[1] = interval
                    max_interval_index[1] = i + 50
        if blank_count[2] != 0:
            if ptlist[i + 100] != 0:
                interval = ptlist[i + 100] - ptlist[i + 100 - 1]
                if interval >= max_interval[2]:
                    max_interval[2] = interval
                    max_interval_index[2] = i + 100

    if max_interval_index[0] != -1:
        i = 49
        while i !=max_interval_index[0]:
            pmatrix[i] = pmatrix[i - 1]
        pmatrix[i] = (pmatrix[i - 1] + pmatrix[i + 1])/2
        blank_count[0] -= blank_count[0]
    if max_interval_index[1] != -1:
        i = 99
        while i !=max_interval_index[1]:
            pmatrix[i] = pmatrix[i - 1]
        pmatrix[i] = (pmatrix[i - 1] + pmatrix[i + 1])/2
        blank_count[1] -= blank_count[1]
    if max_interval_index[2] != -1:
        i = 149
        while i !=max_interval_index[0]:
            pmatrix[i] = pmatrix[i - 1]
        pmatrix[i] = (pmatrix[i - 1] + pmatrix[i + 1])/2
        blank_count[2] -= blank_count[2]
