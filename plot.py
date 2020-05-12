from main import queue2 as queue
from main import lock2 as lock
from parameter import *
import matplotlib.pyplot as plt
def linear(k, b, x):
    return k*x + b

def plot():
    # 计算任意两点间的斜率
    k12 = (PST[1][1] - PST[2][1])/(PST[1][0] - PST[2][0])
    k13 = (PST[1][1] - PST[3][1]) / (PST[1][0] - PST[3][0])
    k23 = (PST[2][1] - PST[3][1]) / (PST[2][0] - PST[3][0])
    # 计算对应的纵截距
    b12 = PST[1][1] - k12*PST[1][0]
    b13 = PST[1][1] - k13*PST[1][0]
    b23 = PST[2][1] - k23*PST[2][0]
    # while True:
    #     if not queue.empty():
    #         with lock:
    #             data = queue.get()
    #             print(data)

