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
    # 参数初始化
    color_list = []
    for r in range(255, -1, -5):
        color_list.append((r, 255, 0))
    turtle.colormode(255)
    turtle.setworldcoordinates(0, 0, LENGTH, WIDTH)
    turtle.shape('triangle')
    turtle.pensize(10)
    # 快速画出边界和网格
    turtle.hideturtle()
    turtle.speed(0)
    turtle.color('red')
    turtle.goto((0, WIDTH))
    turtle.goto((LENGTH, WIDTH))
    turtle.goto((LENGTH, 0))
    turtle.goto((0, 0))
    turtle.showturtle()
    turtle.color('grey')
    turtle.pensize(0.01)
    for i in range(1, LENGTH):
        turtle.penup()
        turtle.setposition(i, 0)
        turtle.pendown()
        turtle.goto(i, WIDTH)
    for i in range(1, WIDTH):
        turtle.penup()
        turtle.setposition(0, i)
        turtle.pendown()
        turtle.goto(LENGTH, i)
    turtle.penup()
    turtle.pensize(5)
    turtle.home()
    is_first = True
    last_pos = (0, 0)
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
                goto(turtle, data, color_list)
                last_pos = data
        else:
            goto(turtle, last_pos, color_list)
plot()
