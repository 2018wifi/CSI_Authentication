import threading
import queue


queue1 = queue.Queue()
queue2 = queue.Queue()


lock1 = threading.Lock()
lock2 = threading.Lock()


if __name__ == '__main__':
    from get_data import get_data
    from process import process
    from plot import plot

    t1 = threading.Thread(target=get_data)
    #t1.start()
    t2 = threading.Thread(target=process)
    t2.start()
    t3 = threading.Thread(target=plot)
    t3.start()