from main import queue2 as queue
from main import lock2 as lock


def plot():
    while True:
        if not queue.empty():
            with lock:
                data = queue.get()
                print(data)
