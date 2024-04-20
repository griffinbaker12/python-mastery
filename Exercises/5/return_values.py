import threading
import time
from concurrent.futures import Future


def parse_line(line):
    res = line.split("=")
    if len(res) > 1:
        return tuple(res)
    return None


def worker(x, y):
    print("about to work")
    print("no, really...")
    time.sleep(20)
    print("Done")
    return x + y


def do_work(x, y, fut):
    fut.set_result(worker(x, y))


fut = Future()
t = threading.Thread(target=do_work, args=(2, 3, fut))
t.start()

print("can do other work here on the main thread")
x = 2 + 2
x += 3

res = fut.result()
print(res)

print("yo")
