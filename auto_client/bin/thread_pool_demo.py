from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
import time

def task(arg1,arg2):
    print(arg1,arg2)
    time.sleep(1)

# pool = ProcessPoolExecutor(10)
pool = ThreadPoolExecutor(10)

for i in range(100):
    pool.submit(task,i,i)