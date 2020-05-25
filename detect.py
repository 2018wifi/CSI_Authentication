from parameter import *

from model import Net, device
import numpy as np
import torch
import time


def detect(matrix):
    model_path = "./models/"
    model_size0 = FP_SIZE * (int(RASP_STATE1) + int(RASP_STATE2) + int(RASP_STATE3))    # 模型输入矩阵的长度，根据树莓派的状态而变化
    if RASP_STATE1 and RASP_STATE2 and RASP_STATE3:
        model_path += TARGET_MAC + "7"
    elif (not RASP_STATE1) and RASP_STATE2 and RASP_STATE3:
        model_path += TARGET_MAC + "3"
    elif RASP_STATE1 and (not RASP_STATE2) and RASP_STATE3:
        model_path += TARGET_MAC + "5"
    elif RASP_STATE1 and RASP_STATE2 and (not RASP_STATE3):
        model_path += TARGET_MAC + "6"
    elif (not RASP_STATE1) and (not RASP_STATE2) and RASP_STATE3:
        model_path += TARGET_MAC + "1"
    elif (not RASP_STATE1) and RASP_STATE2 and (not RASP_STATE3):
        model_path += TARGET_MAC + "2"
    elif RASP_STATE1 and (not RASP_STATE2) and (not RASP_STATE3):
        model_path += TARGET_MAC + "4"
    else:
        print("ERROR: 所有树莓派均故障，无法识别")
        return

    model = Net(model_size0, NFFT, OUTPUT_SIZE).to(device)
    model.load_state_dict(torch.load(model_path))
    print('模型加载成功', model)

    data = torch.from_numpy(np.abs(matrix))
    data = data.to(device).float()
    data = torch.reshape(data, (1, 1, model_size0, NFFT))
    time_beg = int(round(time.time() * 1000))
    result = model(data)
    time_end = int(round(time.time() * 1000))
    print("检测时间: ", time_end - time_beg)
    print("检测结果: ", result)

    return result


'''
将模型输出的结果转化为布尔变量
'''


def judge(raw_result):          # TODO
    pass