import dpkt
import time
import struct
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

BW = 20     # 带宽
NFFT = int(BW * 3.2)
t_c = 1     # 时间（选取前x秒）
rate = 50   # 发包速率，单位：包/秒

class Pcap:
    def __init__(self, rasp_num, point_num, file_name):
        self.rasp_num = rasp_num
        self.point_num = point_num
        self.pcap_name = file_name

    def __parse_udp(self, buffer):      # 解析udp包的二进制流
        nbyte = int(len(buffer))        # 字节数
        data = np.array(struct.unpack(nbyte * "B", buffer), dtype=np.uint8)
        return data

    def __read_header(self, data):  # 提取头信息
        header = {}

        header["magic_bytes"] = data[:4]
        header["source_mac"] = data[4:10]
        header["sequence_number"] = data[10:12]

        coreSpatialBytes = int.from_bytes(data[12:14], byteorder="little")
        header["core"] = [int(coreSpatialBytes & x != 0) for x in range(3)]
        header["spatial_stream"] = [int(coreSpatialBytes & x != 0) for x in range(3, 6)]

        header["channel_spec"] = data[14:16]
        header["chip"] = data[16:18]

        return header

    def __read_csi(self, data):     # 提取CSI信息，并转换成矩阵
        csi = np.zeros(NFFT, dtype=np.complex)
        sourceData = data[18:]
        sourceData.dtype = np.int16
        csi_data = sourceData.reshape(-1, 2).tolist()
        i = 0
        for x in csi_data:
            csi[i] = np.complex(x[0], x[1])
            i += 1
        return csi

    def parse(self):                                            # 提取CSI信息和时间戳信息，并转换成矩阵
        f = open("data_pcap/MAC1/pi" + str(self.rasp_num) + "/" + "T" + str(self.point_num) + "/" + self.pcap_name + ".pcap", 'rb')
        pcap = dpkt.pcap.Reader(f)

        csi_matrix_list = []
        ts_raw_list = []
        ts_list = []
        t_d = []
        no = 0

        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            transf_data = ip.data
            payload = transf_data.data      # 逐层解包

            if len(payload) != 274:         # 大小不对时舍弃这个包
                print('*')
                continue

            data = self.__parse_udp(payload)  # 处理数据
            csi = self.__read_csi(data)

            if no == 0:
                ts_s = ts

            tt = int(time.strftime("%S",time.localtime(ts - ts_s))) # 按秒统计，tt为当前秒数
            if tt < t_c:
                csi_matrix_list.append(csi)
                ts_list.append(ts - ts_s)
                ts_raw_list.append(tt)      # 用于检验原始数据使用，供以画图
                if no > 0:
                    t_d.append(-ts_list[no] + ts_list[no - 1])      #负差值，方便后面从大到小排序
            no = no + 1

        ts_lack = t_c * rate - len(ts_list)     # 与目标数量相差包数

        td_matrix = np.array(t_d)   # 每个包收到时间差值
        td_sort = td_matrix.argsort()   # 对td_matrix值从大到小排序得到的序号

        for i in range(ts_lack):
            shift = 0   # 位移数
            ma_i = [0 for j in range(NFFT)]

            for j in range(i):
                if td_sort[i] > td_sort[j]:     # 如果前面有插入新值，后面插入的值的位移量要增加
                    shift = shift + 1

            index = td_sort[i] + shift

            for j in range(NFFT):                       # 取索引位前后的中值作为插值
                ma_i[j] = (abs(csi_matrix_list[index][j]) + abs(csi_matrix_list[index + 1][j])) / 2
            csi_matrix_list.insert(index + 1, ma_i)

        self.csi_matrix = np.array(csi_matrix_list)
        self.ts_raw_matrix = np.array(ts_raw_list)
        f.close()

    def save(self):                                     # 写入npy文件
        path = "data_npy/data" + str(self.rasp_num) + "/" + "T" + str(self.point_num) + "/" + self.pcap_name + ".npy"
        with open(path, 'wb'):
            pass
        np.save(path, self.csi_matrix)

    def draw(self):                    # 绘制未插值的pcap数据包接收情况
        ts_matrix = self.ts_raw_matrix
        xnum = ts_matrix[len(ts_matrix) - 1]
        x = [i + 1 for i in range(xnum + 1)]    # 设置x轴数值
        data_count = []
        data = sorted(ts_matrix)

        for i in range(xnum + 1):
            # print(data.count(i))
            data_count.append(data.count(i))    # 计算每秒有多少个包

        plt.ylabel('number of packet')
        plt.xlabel('time')
        width = 0.6     # 柱形宽度
        x_major_locator = MultipleLocator(2)    # 刻度设置

        ax = plt.gca()
        ax.xaxis.set_major_locator(x_major_locator)
        bn = plt.bar(x, data_count, width)  # 初始状态柱状图
        plt.tick_params(axis='x', labelsize=5)
        # plt.xticks(rotation=-45)
        ax.set_title(self.pcap_name)

        for b in bn:        # 在柱形上显示对应数字
            ax.text(b.get_x() + b.get_width() / 2, b.get_height(),b.get_height(), fontsize=7,ha = 'center',va='bottom')
        plt.show()


if __name__ == '__main__':
    for i in range(1, 10):           # 点
        for j in range(1, 251):      # 包
            pcap_name = "T" + str(i) + "_" + str(j)
            print("Parsing ", pcap_name)
            pcap1 = Pcap(1, i, pcap_name)
            pcap2 = Pcap(2, i, pcap_name)
            pcap3 = Pcap(3, i, pcap_name)
            pcap1.parse()
            pcap2.parse()
            pcap3.parse()

            con_matrix = np.zeros((100, 64), dtype=np.complex)
            con_matrix[0:50] = pcap1.csi_matrix[0:50]
            con_matrix[50:100] = pcap2.csi_matrix[0:50]
            con_matrix[100:150] = pcap3.csi_matrix[0:50]
            with open("data/MAC1/State7/T" + str(i) + "/T" + str(i) + "_" + str(j) + ".npy",
                      'wb'):
                pass
            np.save("data/MAC1/State7/T" + str(i) + "/T" + str(i) + "_" + str(j) + ".npy", con_matrix)

            # pcap1.save()
            # pcap2.save()
            # pcap3.save()

