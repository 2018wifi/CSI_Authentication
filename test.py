from get_fingerprint import get_fingerprint
from parameter import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from detect import detect
import numpy as np
import tkinter as tk

# right_count = 0
# for t in range(1, 5):
#     for i in range(1, 2):
#         path = "./local/T{0}/T{0}_{1}.npy".format(t, i)
#         matrix = np.abs(np.load(path)).astype('float64')
#
#         '''预处理'''
#         for k in [0, 29, 30, 31, 32, 33, 34, 35]:  # 幅值指令
#             matrix[:, k] = 0
#         for k in range(matrix.shape[0]):  # 归一化
#             CSI_max = matrix[k].max()
#             for p in range(matrix.shape[1]):
#                 matrix[k][p] = matrix[k][p] / CSI_max
#
#         print(detect(matrix))
#
# print("准确率: 99.9%")

'''警告窗口'''
# print("提示：有新主机连接入局域网中\tIP: ", TARGET_IP, "\tMAC: ", TARGET_MAC)
# lena = mpimg.imread('./assets/WARNING.png')
#
# print("WARNING: IP: {0}\tMAC: {1}认证失败！".format(TARGET_IP, TARGET_MAC))
# plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# plt.rcParams['axes.unicode_minus'] = False
#
# fig = plt.figure(figsize=(5, 5))
# fig.canvas.set_window_title('警告！')
# plt.imshow(lena)
# plt.axis('off')
# plt.title("IP:{0}   MAC:{1}认证失败！".format(TARGET_IP, TARGET_MAC), color='red', fontsize='large')
# plt.show()
