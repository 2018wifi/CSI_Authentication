from main import queue2 as queue
from main import lock2 as lock
from parameter import *
import turtle
import numpy as np
def goto(turtle, i, color_list):
    path = np.linspace(list(turtle.pos()), POS[i], 15)
    print(POS)
    for c, p in zip(color_list, path):
        turtle.color(c)
        turtle.goto(p)

def plot():
    # while True:
        # goto(turtle, 0, color_list)
        # turtle.dot(20, "blue")
        # goto(turtle, 1, color_list)
        # turtle.dot(20, "red")
        # goto(turtle, 2, color_list)
        # turtle.dot(20, "purple")
    # # 计算任意两点间的斜率
    # k12 = (POS[1][1] - POS[2][1])/(POS[1][0] - POS[2][0])
    # k13 = (POS[1][1] - POS[3][1]) / (POS[1][0] - POS[3][0])
    # k23 = (POS[2][1] - POS[3][1]) / (POS[2][0] - POS[3][0])
    # # 计算对应的纵截距
    # b12 = POS[1][1] - k12*POS[1][0]
    # b13 = POS[1][1] - k13*POS[1][0]
    # b23 = POS[2][1] - k23*POS[2][0]
    while True:
        if not queue.empty():
            with lock:
                data = queue.get()
                print(data)
