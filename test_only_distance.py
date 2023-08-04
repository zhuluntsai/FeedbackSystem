# !pip install pyserial
# !pip install serial

import Vortex
import time
from datetime import datetime
# import serial
# import pyserial
# import ctypes
from ExcavatorStim import StimGenerator, parameterSetting
# mode = 10 (for API mode), mode = 20 (for frequency and amplitude adjustment mode)
mode = 10
serialConnectionTrigger = 0 # To control serial connection -> 0: Before connected, 1: After connected
pastTime = 0.0 # For time gap
currentTime = 0.0

minFreqinLink = 10.0 # For setting minimum stimulation , Unit: Hz, This valus should be over 10.0 Hz
maxFreqinLink = 75.0 # For setting maximum stimulation , Unit: Hz, This valus should be under 100 Hz.
minDisinLink = 0.0# For setting minimum distance between a bucket and burried pipe. This valus should be positive.
              # But, I recommend you not to change minDis. (10.0 <- optimal value)
maxDisinLink = 0.22 # For setting maximum distance between a bucket and burried pipe. This value should be positive.
#minDisinLink = (minDisinLink/0.1)*10
#maxDisinLink = (maxDisinLink/0.1)*10

# 생성 주기가 60Hz인 데이터를 저장하는 변수
disval = 0


def delayfunc(delayTime):
    start = time.time()
    while ((time.time()-start)<=delayTime):
        continue

def on_simulation_start(extension):
    # Turn on the engine by default
    # extension.outputs.engine.value = True
    # # Set the throttle to 1.0 at the start, 1 represents the pedal pressed all the way in, we want to go as fast as possible
    # extension.outputs.throttle.value = 1.0
    # # Switch to first gear right at the start
    # extension.outputs.gear.value = 1
    # if(abs(extension.inputs.Distance.value)) == 1:
    #     print("nice")

    print("Initialized")
if (disval<=0.3):
    parameterSetting(minFreqinLink, maxFreqinLink, minDisinLink, maxDisinLink, 1) 
else:
    parameterSetting(minFreqinLink, maxFreqinLink, minDisinLink, maxDisinLink, 0) 


# def pre_step(extension):

    # # 현재 시간 밀리초 값을 가져오기
    # millis = int(round(time.time() * 1000))
    # # 다음 데이터를 수집할 시간 계산
    # next_time = (millis // 100 + 1) * 100
    # time.sleep((next_time - millis) / 1000.0)

    # # 10Hz마다 데이터 수집
    # if next_time % 1000 == 0:
    #     disval = extension.inputs.DistanceL.value 
    #     print(disval)

    ## extension
    ##disval = extension.inputs.DistanceL.value 
    ##print(disval)


# 데이터를 카운트하는 변수
data_count = 0

def pre_step(extension):
    global disval, data_count
    # extension
    if disval is None or data_count == 6:
        # 새로운 데이터 생성
        disvalL = extension.inputs.DistanceL.value
        disvalR = extension.inputs.DistanceR.value
        disval = min(disvalL, disvalR)
        # 데이터 카운트 초기화
        data_count = 1
    else:
        # 이전 데이터를 사용
        data_count += 1
    #print(disval)
    
    global serialConnectionTrigger
    global pastTime
    if abs(disval)<=0.3 and serialConnectionTrigger == 0: # Connect serial connection when dis>10m
        StimGenerator(0, mode, 1, float(maxDisinLink+1))
        for _ in range(5):
            StimGenerator(1, mode, 2)
            #print("Activated Standy")
        serialConnectionTrigger = 1
        #print("TestA")
    elif abs(disval) <= maxDisinLink and abs(disval)>=minDisinLink and serialConnectionTrigger == 1:  
        StimGenerator(2, mode, 3, float(disval)) 

    elif abs(disval) > maxDisinLink and abs(disval)<=10 and serialConnectionTrigger == 1:  
        StimGenerator(2, mode, 3, float(1)) 

         
    elif abs(disval) > 10 and serialConnectionTrigger == 1: # disconnect serial connection when dis>10m
        StimGenerator(2, mode, 3, float(maxDisinLink+1))
        StimGenerator(3, mode, 4)
        for _ in range(10):
            print("Abort Standy")
        serialConnectionTrigger = 3
    
"""
    global serialConnectionTrigger
    if (disval <= maxDisinLink and disval>=minDisinLink and serialConnectionTrigger == 0):
                StimGenerator(0, mode, 1, float(maxDisinLink+1))
                #StimGenerator(0, mode, 1, float(disval))
                for _ in range(10):
                    StimGenerator(1, mode, 2)
                    #print("Activated Standy")
                serialConnectionTrigger = 1
    elif (disval <= maxDisinLink and disval>=minDisinLink and serialConnectionTrigger == 1):
                StimGenerator(2, mode, 3, float(disval) )
                #print("Activated", disval)
    elif ((disval > maxDisinLink or disval < minDisinLink) and serialConnectionTrigger == 1 ):
                StimGenerator(2, mode, 3, float(maxDisinLink+1))
                StimGenerator(3, mode, 4)
                for _ in range(10):
                    print("Abort Standy")
                serialConnectionTrigger = 0
"""    
