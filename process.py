from parameter import *

from main import queue1, queue2, lock1, lock2
from model import Net, device

import torch


def process():
    model = Net(PCAP_SIZE, NFFT, OUTPUT_SIZE).to(device)
    model.load_state_dict(torch.load(MODEL_PATH))
    while True:
        if not queue1.empty():
            with lock1:
                data = queue1.get()
            data = data.to(device)
            result = model(data)
            if DEBUG:
                print(result)
            with lock2:
                queue2.put(result)