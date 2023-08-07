import serial
from time import sleep
from ctypes import *
from datetime import datetime
import time
eventMessage = ""

class StimGenerator:

    def __init__(self):
        # Serial communication port number
        self.port = 'COM9'
        
        # Serial communication baudrate
        self.baudRate = 115200

        # For setting minimum and maximum stimulation frequency. These valus should be within 10 Hz to 100 Hz.
        self.minFreq = 10
        self.maxFreq = 100

        # For setting minimum and maxumum distance between a bucket and burried pipe. This valus should be positive.
        self.minDis = 10
        self.maxDis = 100

        self.delayFlag = 0
        self.timeStart = 0.0
        self.timeCurrent = 0.0
        self.delayDesired = 0.05

    def parameterSetting(self, minFrequency, maxFrequency,minDistance, maxDistance, limitValue):
        if limitValue == 1:
            self.minFreq = minFrequency
        elif limitValue == 0:
            self.minFreq = 0

        self.maxFreq = maxFrequency
        self.minDis = minDistance
        self.maxDis = maxDistance

        self.slopeA = (self.maxFreq-self.minFreq) / (self.minDis-self.maxDis)
        self.constantB = 0.5 * ((self.maxFreq+self.minFreq) - self.slopeA * (self.minDis+self.maxDis))

    def delayfunc(delayTime):
        start = time.time()
        while time.time()-start <= delayTime:
            continue

    def FreqGenerator(self, mode, dis):
        stimFreqVal = 0.0
        if mode == 10:
            if dis >= self.minDis and dis<=self.maxDis:
                stimFreqVal  = self.slopeA * dis + self.constantB
            elif dis > self.maxDis:
                stimFreqVal = 0.0
            elif dis < self.minDis:
                stimFreqVal = 0.0
        elif mode == 20:
            if dis > 100:
                stimFreqVal = 100
            elif dis < 0:
                stimFreqVal = 0
            else:
                stimFreqVal = dis

        print(stimFreqVal)
        return stimFreqVal

    def StimGenerate(self, comStatus, mode, sync, dis, tempInput):

        # Caution****------------------------------------------------------------------------------------- 
        # Please do not edit scripts below. If you revise any codes below, 
        # it would lead to electrical shock to subjects, and its your responsibility.
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
                serialComm = serial.Serial(self.port, self.baudRate)
                if serialComm:
                    print("Serial comm successfully open")
                    with open("StimLog.txt", "a") as f:
                        eventMessage = "Serial comm open mode successfully activated. \n"
                        output = str(now) + " -> " + eventMessage
                        f.write(output)
            except:
                print("Check your port. Default port is COM5.")
                with open("StimLog.txt", "a") as f:
                    eventMessage = "Serial comm open failed. \n"
                    output = str(now) + " -> " + eventMessage
                    f.write(output)
                return
            serialComm.timeout = timeOut
            self.delayfunc(0.05)
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
        
            freq = self.FreqGenerator(mode, dis)
            #print(freq)
            #freq = FreqGenerator(dis, libc, mode, sync)
            
        elif comStatus == 1:
            freq = str(0)
            serialComm.write(str(int(freq)).encode('utf-8'))
            ##sleep(0.05)
            self.delayfunc(0.05)
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
                if (type(dis) != float) or (type(self.minDis) != float) or (type(self.maxDis) != float) or (type(self.minFreq) != float) or (type(self.maxFreq) != float):
                    print("Please check data types of your inputs. serial Comm is closed.")
                    serialComm.close()
                    return
                if dis < 0 or self.minDis < 0 or self.maxDis <= 0 or self.minFreq < 0 or self.maxFreq <= 0 or self.minDis >= self.maxDis or self.minFreq >= self.maxFreq:
                    print("Please check one of the input values are below zero.Serial comm is closed.")
                    serialComm.close()
                    return
                #freq = FreqGenerator(dis, libc, mode, sync)
                freq = self.FreqGenerator(mode, dis)
                #print(freq)
                with open("StimLog.txt", "a") as f:
                    eventMessage = "Stimulation mode. "
                    output = str(now) + " -> " + eventMessage+"Freq: " + str(int(freq)) + "[Hz]" + "\n"
                    f.write(output)
                #print("test_freq: "+str(freq))
            elif mode == 20:
                freq = self.FreqGenerator(mode, dis)
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
        
                if (time.time()-timeStart) >= self.delayDesired:
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
            self.delayfunc(0.05)
            freq = str(0)
            serialComm.write(str(int(freq)).encode('utf-8'))
            self.delayfunc(0.05)
            ##sleep(1)
            serialComm.close()
            print("Serial comm successfully closed")
            with open("StimLog.txt", "a") as f:
                eventMessage = "Serial comm closing mode successfully activated. \n"
                output = str(now) + " -> " + eventMessage
                f.write(output)