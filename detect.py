from parameter import *

from model import Net, device
import numpy as np
import torch
import time


def detect(matrix):
    target_mac = TARGET_MAC.replace(':', '')
    model_path = "./Train/models/" + target_mac
    if RASP_STATE1 and RASP_STATE2 and RASP_STATE3:
        model_path += "7"
    elif (not RASP_STATE1) and RASP_STATE2 and RASP_STATE3:
        model_path += "3"
    elif RASP_STATE1 and (not RASP_STATE2) and RASP_STATE3:
        model_path += "5"
    elif RASP_STATE1 and RASP_STATE2 and (not RASP_STATE3):
        model_path += "6"
    elif (not RASP_STATE1) and (not RASP_STATE2) and RASP_STATE3:
        model_path += "1"
    elif (not RASP_STATE1) and RASP_STATE2 and (not RASP_STATE3):
        model_path += "2"
    elif RASP_STATE1 and (not RASP_STATE2) and (not RASP_STATE3):
        model_path += "4"
    else:
        print("ERROR: 所有树莓派均故障，无法识别")
        return
    model_path += ".pkl"

    model = Net(FP_SIZE, NFFT, OUTPUT_SIZE).to(device)
    model.load_state_dict(torch.load(model_path))
    # print('模型加载成功', model)


    data = matrix.to(device).float()
    data = torch.reshape(data, (1, 1, FP_SIZE, NFFT))
    time_beg = int(round(time.time() * 1000000))
    result = model(data)
    time_end = int(round(time.time() * 1000000))
    print(list(result[0]))
    return result.argmax(), get_prob(result), time_end - time_beg         # 最可能的点，各点的结果方差，检测时间

def get_prob(result):
    exps = np.exp(result[0] - np.max(result[0]))
    return exps / np.sum(exps)