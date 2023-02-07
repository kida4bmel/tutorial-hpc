import multiprocessing as mp
from time import time, sleep
import humanize
import psutil
import os
import sys
import GPUtil as GPU
import numpy as np


print("Terminal input is:", sys.argv)

def avail_hardware():
    process = psutil.Process(os.getpid())
    GPUs = GPU.getGPUs() #get informations abou GPUs  
    print(f"Number of CPU cores: {len(psutil.cpu_percent(interval=1, percpu=True))}\n\
            Avail Ram:{humanize.naturalsize( psutil.virtual_memory().available)}", flush=True)
    if GPUs:
        print("GPUs:", GPUs)


def printm(event):
    process = psutil.Process(os.getpid())
    GPUs = GPU.getGPUs() #get informations abou GPUs  
    
    while True:
        print("Gen RAM Free: " + humanize.naturalsize( psutil.virtual_memory().available ), " | Proc size: " + humanize.naturalsize( process.memory_info().rss), flush=True)
        print("CPU usage per core: ", sorted(psutil.cpu_percent(interval=1, percpu=True),reverse= True), flush=True)
        if GPUs:
            print("GPU RAM Free: {0:.0f}MB | Used: {1:.0f}MB | Util {2:3.0f}% | Total {3:.0f}MB".format(GPUs[0].memoryFree, GPUs[0].memoryUsed, GPUs[0].memoryUtil*100, GPUs[0].memoryTotal), flush=True)
        sleep(5)

        if event.is_set():
            break


# a usless function to at least do something
def Eigendecomposition(N, size):
    
    np.random.seed(0)

    for _ in range(N):
        t = time()
        A = np.random.random((size, size))
        np.linalg.eig(A)
        delta = time() - t
        print("Eigendecomposition of a %dx%d matrix in %0.2f s." % (size , size , delta / N), flush=True)

    


if __name__ == "__main__":
    avail_hardware()

    mp.set_start_method('spawn')
    event = mp.Event()
    p1 = mp.Process(target = Eigendecomposition,args=(5, 2048))
    p2 = mp.Process(target =  printm, args=(event,))
    p1.start()
    p2.start()
    p1.join()
    event.set() #kills printm process
    p2.join()
    print("Finished")

