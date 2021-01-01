from pytz import timezone
from datetime import datetime
from time import sleep, time, ctime
from multiprocessing import Process

from my_logger import log_this_error

# job scheduler
def f():
    g = 0
    for i in range(100000000):
        g += 1
    print(g)
    
processes = []
PERIOD = 5 # in seconds
while True:
    try:
        s = time() + PERIOD
        for x in processes:
            if not x.is_alive():
                x.join()
                processes.remove(x)
        sleep(round(s - time()))
        print(ctime(time()), len(processes))
        p = Process(target = f)
        p.start()
        processes.append(p)
    except Exception as exc:
        log_this_error(exc)
        [p.terminate for p in processes]


## event scheduler
def schedule(function, tz, hour, minute):
    """

    Parameters
    ----------
    function : callable function
        name of the function which needs to be scheduled
    tz : str
        timezone
    hour : int
        hour of the time to be scheduled
    minute : int
        minute of the time to be scheduled

    Returns
    -------
    None.

    """
    while True:
        hr = int(datetime.now(timezone(tz)).time().hour)
        minute = int(datetime.now(timezone(tz)).time().minute)
        if (hr == hour) & (minute == minute):
            for tries in range(10):
                print("====== TRY ====== :", tries+1)
                try:
                    function()
                    sleep(60)
                    break
                except Exception as exc:
                    log_this_error(exc)
                    continue
        else:
            print(hr, minute)
            sleep(50)