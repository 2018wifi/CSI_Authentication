# coding=gbk
import threading
import queue


# queue1用于存储规格化后的CSI样本，queue2用于存储运算结果
queue1 = queue.Queue()
queue2 = queue.Queue()


# queue1和queue2的线程锁
lock1 = threading.Lock()
lock2 = threading.Lock()


if __name__ == '__main__':
    from get_data import get_data
    from process import process
    from plot import plot

    t1 = threading.Thread(target=get_data)
    t1.start()
    t2 = threading.Thread(target=process)
    t2.start()
    t3 = threading.Thread(target=plot)
    t3.start()