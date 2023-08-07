# Date: 2022/10/28

# Modules and Parameters ------------------
# Do not edit this part.
import serial
#import ctypes
from time import sleep
from ctypes import *
from datetime import datetime
import time
eventMessage = ""
#------------------------------------------

# Parameters for operator---------------------------------------------------------------------------------------
port = '/dev/cu.usbmodem141301'# Serial communication port number
baudRate = 115200 # Serial communication baudrate
minFreq = 10.0 # For setting minimum stimulation , Unit: Hz, This valus should be over 10.0 Hz
maxFreq = 100.0 # For setting maximum stimulation , Unit: Hz, This valus should be under 100 Hz.
minDis = 10# For setting minimum distance between a bucket and burried pipe. This valus should be positive.
              # But, I recommend you not to change minDis. (10.0 <- optimal value)
maxDis = 100.0 # For setting maximum distance between a bucket and burried pipe. This value should be positive.
#-----------------------------------------------------------------------------------------------------------------

# Parameters for delay---------------------------------------------------------------------------------------
global delayFlag
delayFlag = 0

global timeStart
timeStart = 0.0

global timeCurrent
timeCurrent = 0.0

global delayDesired
delayDesired = 0.05
#-----------------------------------------------------------------------------------------------------------------

def parameterSetting(minFrequency, maxFrequency,minDistance, maxDistance, limitValue):
    global minFreq
    if limitValue==1:
        minFreq = minFrequency
    elif limitValue ==0:
        minFreq =0

    global maxFreq
    maxFreq = maxFrequency
    global minDis
    minDis = minDistance
    global maxDis
    maxDis = maxDistance
    
"""
def FreqGenerator(dis, libc, mode, sync):
    # To modulate the frequency of Estim by the distance information between an excavator's bucket and a buried pipe.
    # Data conversion for "C"--------------------------------------------------------------
    c_dis = c_float(dis)    
    c_minDis = c_float(minDis)
    c_maxDis = c_float(maxDis)
    c_minFreq = c_float(minFreq)
    c_maxFreq = c_float(maxFreq)
    #--------------------------------------------------------------------------------------
    _freqGenerator = libc.freqGenerator
    _freqGenerator.restype = c_float
    return _freqGenerator(c_dis, c_minDis, c_maxDis, c_minFreq, c_maxFreq, mode, sync)

"""
def delayfunc(delayTime):
    start = time.time()
    while ((time.time()-start)<=delayTime):
        continue

def FreqGenerator(mode, dis):
    stimFreqVal = 0.0
    if mode == 10:
        slopeA = (maxFreq-minFreq)/(minDis-maxDis)
        constantB = 0.5 * ((maxFreq+minFreq)-slopeA*(minDis+maxDis))
        if (dis>=minDis and dis<=maxDis):
            #stimFreqVal = slopeA*dis+constantB
            stimFreqVal  = slopeA*dis+constantB
        elif (dis>maxDis):
            stimFreqVal = 0.0
        elif (dis<minDis):
            stimFreqVal = 0.0
        
    elif mode == 20:
        if (dis>100):
            stimFreqVal = 100
        elif (dis <0):
            stimFreqVal = 0
        else:
            stimFreqVal = dis
    print(stimFreqVal)
    return int(stimFreqVal)   

def StimGenerator(comStatus, mode, sync, dis = minDis-1, tempInput = 0):
    #StimGenerator(comStatus, mode, sync, dis = minDis-1, tempInput = 0):
    global delayFlag
    global timeStart
    global timeCurrent
    global delayDesired
    #print("minFreq: ",type(minFreq))
    #print("maxFreq: ",type(maxFreq))
    #print("minDis: ", type(minDis))
    #print("maxDis: ", type(maxDis))
    #Caution****------------------------------------------------------------------------------------- 
    # Please do not edit scripts below. If you revise any codes below, 
    #it would lead to electrical shock to subjects, and its your responsibility.
    # -----------------------------------------------------------------------------------------------
    
    # Function Parameters ---------------------------------------------------------------------------------------------
    # comStatus -> 0: SerialCom open, 1: SerialCom ready, 2: SerialCom active, 3: SerialCom close
    # mode -> To switch between frequency-modulated electro-tactile feedback mode (mode = 10) 
    # and amplitude/frequency adjustmnet mode (mode = 20)
    # Sync -> time synchronization --> 0: SerialCom open, 1: SerialCom ready, 2: SerialCom active, 3: SerialCom close
    #------------------------------------------------------------------------------------------------------------------
    
    #Variables of Developer---------------------------------
    timeOut = 0 
    returnFreq = 0
    now = datetime.now() # Time Information
    #------------------------------------------------------
        
    if comStatus == 0:
        with open("StimLog.txt", "a") as f:
            output = "\n [Log: " + str(now) +"] \n"
            f.write(output)
        try:
            global serialComm
            serialComm = serial.Serial(port, baudRate)
            if serialComm:
                print("Serial comm successfully open")
                with open("StimLog.txt", "a") as f:
                    eventMessage = "Serial comm open mode successfully activated. \n"
                    output = str(now) + " -> " + eventMessage
                    f.write(output)
        except Exception as e:
            print(e)
            print("Check your port. Default port is COM5.")
            with open("StimLog.txt", "a") as f:
                eventMessage = "Serial comm open failed. \n"
                output = str(now) + " -> " + eventMessage
                f.write(output)
            return
        serialComm.timeout = timeOut
        delayfunc(0.05)
        ##sleep(0.5) # Wait for completing serial open
        try:
            #libc = ctypes.CDLL('./freqGenerator.dll') # It is to load DLL file. 
            with open("StimLog.txt", "a") as f:
                eventMessage = "Serial Comm open mode. Freq calculator successfully loaded. \n"
                output = str(now) + " -> " + eventMessage
                f.write(output)
        except:
            print("Your ""freqGenerator"" has problem. Please check it.")
            with open("StimLog.txt", "a") as f:
                eventMessage = "Serial Comm open mode. Freq calculator not successfully loaded. \n"
                output = str(now) + " -> " + eventMessage
                f.write(output)
            serialComm.close()
            return 
       
        freq = FreqGenerator(mode, dis)
        #print(freq)
        #freq = FreqGenerator(dis, libc, mode, sync)
        
    elif comStatus == 1:
        freq = str(0)
        serialComm.write(str(int(freq)).encode('utf-8'))
        ##sleep(0.05)
        delayfunc(0.05)
        with open("StimLog.txt", "a") as f:
            eventMessage = "Standby mode activated. "
            output = str(now) + " -> " + eventMessage + "Freq: " + freq + "[Hz]" + "\n"
            f.write(output)
        return
        
    elif comStatus == 2:
        try:
            #libc = ctypes.CDLL('./freqGenerator.dll') # It is to load DLL file. 
            with open("StimLog.txt", "a") as f:
                eventMessage = "Stimulation mode. Freq calculator successfully loaded. \n"
                output = str(now) + " -> " + eventMessage
                f.write(output)
        except:
            print("Your ""freqGenerator"" has problem. Please check it.")
            with open("StimLog.txt", "a") as f:
                eventMessage = "Stimulation mode. Freq calculator not successfully loaded. \n"
                output = str(now) + " -> " + eventMessage
                f.write(output)
            serialComm.close()
            return
        if mode == 10:
            if (type(dis) != float) or (type(minDis) != float) or (type(maxDis) != float) or (type(minFreq) != float) or (type(maxFreq) != float):
                print("Please check data types of your inputs. serial Comm is closed.")
                serialComm.close()
                return
            if dis<0 or minDis<0 or maxDis<=0 or minFreq<0 or maxFreq<=0 or minDis>=maxDis or minFreq>=maxFreq:
                print("Please check one of the input values are below zero.Serial comm is closed.")
                serialComm.close()
                return
            #freq = FreqGenerator(dis, libc, mode, sync)
            freq = FreqGenerator(mode, dis)
            #print(freq)
            with open("StimLog.txt", "a") as f:
                eventMessage = "Stimulation mode. "
                output = str(now) + " -> " + eventMessage+"Freq: " + str(int(freq)) + "[Hz]" + "\n"
                f.write(output)
            #print("test_freq: "+str(freq))
        elif mode == 20:
            freq = FreqGenerator(mode, dis)
            #print(freq)
            #freq = FreqGenerator(dis, libc, mode, sync)
            with open("StimLog.txt", "a") as f:
                eventMessage = "Stimulation mode. "
                output = str(now) + " -> " + eventMessage+"Freq: " + str(int(freq))+ "[Hz]"  + "\n"
                f.write(output)
        
        # For Arduino Serial comm------------------------------------------------------------------------
        if delayFlag == 0:
            timeStart = time.time()
            delayFlag = 1
        elif delayFlag == 1:
           if (time.time()-timeStart) >= delayDesired:
            serialComm.write(str(int(freq)).encode('utf-8'))
            delayFlag = 0
            """
            if (time.time()-timeStart) >= delayDesired:
                        if (tempInput == 0):
                            serialComm.write(str(int(freq)).encode('utf-8'))
                            delayFlag = 0
                        elif (tempInput == 100):
                            serialComm.write(str(0).encode('utf-8'))
                            delayFlag = 0
                    
            """

        #serialComm.write(str(int(freq)).encode('utf-8'))
        #delayfunc(0.05)
        
        
        ##sleep(0.05) #데이터 갔다가 오는데 시간이 걸리므로, 이것이 어찌보면 치명적인 역할을 할 수도 있음
        # 여기 sleep은 반드시 arduino의 Serial.setTimeout보다 커야 한다. 
        #------------------------------------------------------------------------------------------------
        
    elif comStatus == 3:
        ##sleep(0.5)
        delayfunc(0.05)
        freq = str(0)
        serialComm.write(str(int(freq)).encode('utf-8'))
        delayfunc(0.05)
        ##sleep(1)
        serialComm.close()
        print("Serial comm successfully closed")
        with open("StimLog.txt", "a") as f:
            eventMessage = "Serial comm closing mode successfully activated. \n"
            output = str(now) + " -> " + eventMessage
            f.write(output)