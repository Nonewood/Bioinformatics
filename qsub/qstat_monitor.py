# 根据 qsub 的 jobID 进行定时的获取内存的监控，待完善
#! /usr/bin/python3
import sys,os
from datetime import datetime
import time
jobID = sys.argv[1]
time_sleep = int(sys.argv[2])
def timer(n):
    while True:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        vf = os.popen('qstat -j ' + jobID + '| grep usage').readline().strip('\n')
        if vf:
            print(vf)
        else:
            exit()
        time.sleep(n)
timer(time_sleep)
