from parameter import *
from detect import detect
import numpy as np
import torch


MIN_THR = 1e-10
MAX_THR = 0.9999
MAX_MIN_THR = 0.99999

'''合法检测'''

def legal_test():
    right_count = 0
    error_count = 0
    test_time = []          # us

    print("---合法集检测---")
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

            result, time_cost = detect(matrix)
            max_point = torch.argmax(result)
            min_point = torch.argmin(result)
            result_list = result.tolist()[0]
            # print("极差: {}\t 方差: {}\t".format(result.tolist()[0][max_point] - result.tolist()[0][min_point], torch.var(result)))

            if result_list[max_point] > MAX_THR or result_list[min_point] > MIN_THR or result_list[max_point] - result_list[min_point] > MAX_MIN_THR:
                right_count += 1
                # print("合法")
            else:
                error_count += 1
                # print("不合法")

            test_time.append(time_cost)

    print("---合法集检测结果---")
    print("合法集的准确率为: {}, 错误率为: {}".format(right_count / (right_count + error_count), error_count / (right_count + error_count)))
    print("平均检测时间: {0} ms".format(np.mean(test_time) / 1000))

'''不合法检测'''

def illegal_test():
    right_count = 0
    error_count = 0
    test_time = []

    print("---不合法集检测---")
    for i in range(1, 201):
        path = "./test/data/{0}.npy".format(i)
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

        result, time_cost = detect(matrix)
        max_point = torch.argmax(result)
        min_point = torch.argmin(result)
        result_list = result.tolist()[0]
        # print("极差: {}\t 方差: {}\t".format(result.tolist()[0][max_point] - result.tolist()[0][min_point], torch.var(result)))
        # print("最可能点:{0}, 最可能点概率: {1}\t最不可能点: {2}, 最不可能点概率: {3}".format(max_point, result.tolist()[0][max_point], min_point, result.tolist()[0][min_point]))

        if result_list[max_point] > MAX_THR or result_list[min_point] > MIN_THR or result_list[max_point] - result_list[min_point] > MAX_MIN_THR:
            right_count += 1
        # print("通过")
        # print("最可能点:{0}, 最可能点概率: {1}\t最不可能点: {2}, 最不可能点概率: {3}".format(max_point, result.tolist()[0][max_point], min_point, result.tolist()[0][min_point]))
        else:
            error_count += 1
            # print("不通过")

        test_time.append(time_cost)

    print("---不合法集检测结果---")
    print("不合法集的通过率为: {}, 不通过率为: {}".format(right_count / (right_count + error_count), error_count / (right_count + error_count)))
    print("平均检测时间: {0} ms".format(np.mean(test_time) / 1000))

legal_test()

illegal_test()