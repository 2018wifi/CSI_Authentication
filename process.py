from parameter import *

from main import queue1, queue2, lock1, lock2
from model import Net, device
import numpy as np
import torch


def process():
    model = Net(PCAP_SIZE, NFFT, OUTPUT_SIZE).to(device)
    model.load_state_dict(torch.load(MODEL_PATH))
    print('模型加载成功', model)
    while True:
        if not queue1.empty():
            with lock1:
                data = queue1.get()
            data = torch.from_numpy(data.astype('float64'))
            data.device = device
            data = torch.reshape(data, (1, 1, PCAP_SIZE, NFFT))
            result = model(data)
            if DEBUG:
                print(result)
            with lock2:
                queue2.put(result)

if __name__ == '__main__':
    model = Net(PCAP_SIZE, NFFT, OUTPUT_SIZE).to(device)
    model.load_state_dict(torch.load(MODEL_PATH))
    print('模型加载成功', model)
    data = np.zeros((PCAP_SIZE, NFFT))
    data = torch.from_numpy(data)
    data = data.to(device).float()
    data = torch.reshape(data, (1, 1, PCAP_SIZE, NFFT))
    result = model(data)
    if DEBUG:
        print(result)
    with lock2:
        queue2.put(result)