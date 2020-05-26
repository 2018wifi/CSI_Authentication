from get_fingerprint import get_fingerprint
from parameter import *
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
from detect import detect
import numpy as np
import torch

right_count = 0
error_count = 0
test_time = []              # us
for t in range(1, 9):
    for i in range(201, 251):
        path = "./local/T{0}/T{0}_{1}.npy".format(t, i)
        path = 'Train/data/MAC1/State7/T' + str(t) + '/T' + str(t) + '_1.npy'
        matrix = np.load(path)

        '''预处理'''
        for k in range(NPY_SIZE):
            matrix[k] = abs(matrix[k])
        matrix = torch.from_numpy(matrix.astype('float64'))[0:NPY_SIZE]
        for k in [0, 29, 30, 31, 32, 33, 34, 35]:  # 幅值指令
            matrix[:, k] = 0
        for k in range(matrix.shape[0]):  # 归一化
            CSI_max = matrix[k].max()
            for p in range(matrix.shape[1]):
                matrix[k][p] = matrix[k][p] / CSI_max

        point, variance, time_cost = detect(matrix)
        print("T{0}_{1}检测结果: 最大可能地点: {2}\t方差: {3}\t花费时间: {4} us".format(t, i, point, round(variance, 3), time_cost))
        test_time.append(time_cost)
        if point == t - 1:
            right_count += 1
        else:
            error_count += 1

print("---检测结果---")
print("准确率: {0}%".format(round(right_count / (right_count + error_count) * 100, 2)))
print("错误率: {0}%".format(round(error_count / (right_count + error_count) * 100, 2)))
print("平均检测时间: {0} ms".format(np.mean(test_time) / 1000))