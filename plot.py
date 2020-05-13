from main import queue2 as queue
from main import lock2 as lock
from parameter import *
import turtle
import numpy as np
def goto(turtle, i, color_list):
    path = np.linspace(list(turtle.pos()), PST[i], 51)
    for c, p in zip(color_list, path):
        turtle.color(c)
        turtle.goto(p)

def plot():
    # color_list = []
    # for r in range(255, -1, -5):
    #     color_list.append((r, 255, 0))
    # turtle.colormode(255)
    # turtle.setworldcoordinates(0, 0, 10, 10)
    # # turtle.speed(1)
    # turtle.shape('triangle')
    # turtle.pensize(10)
    # # turtle.penup()
    # while True:
    #     goto(turtle, 0, color_list)
    #     turtle.dot(20, "blue")
    #     goto(turtle, 1, color_list)
    #     turtle.dot(20, "red")
    #     goto(turtle, 2, color_list)
    #     turtle.dot(20, "purple")
    # # 计算任意两点间的斜率
    # k12 = (PST[1][1] - PST[2][1])/(PST[1][0] - PST[2][0])
    # k13 = (PST[1][1] - PST[3][1]) / (PST[1][0] - PST[3][0])
    # k23 = (PST[2][1] - PST[3][1]) / (PST[2][0] - PST[3][0])
    # # 计算对应的纵截距
    # b12 = PST[1][1] - k12*PST[1][0]
    # b13 = PST[1][1] - k13*PST[1][0]
    # b23 = PST[2][1] - k23*PST[2][0]
    while True:
        if not queue.empty():
            with lock:
                data = queue.get()
                print(data)
# plot()
