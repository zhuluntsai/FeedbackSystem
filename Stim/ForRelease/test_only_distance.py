import Vortex
import math
from ExcavatorStim import StimGenerator, parameterSetting
# mode = 10 (for API mode), mode = 20 (for frequency and amplitude adjustment mode)
mode = 10
serialConnectionTrigger = 0 # To control serial connection -> 0: Before connected, 1: After connected


minFreqinLink = 10.0 # For setting minimum stimulation , Unit: Hz, This valus should be over 10.0 Hz
maxFreqinLink = 100.0 # For setting maximum stimulation , Unit: Hz, This valus should be under 100 Hz.
minDisinLink = 0.0# For setting minimum distance between a bucket and burried pipe. This valus should be positive.
              # But, I recommend you not to change minDis. (10.0 <- optimal value)
maxDisinLink = 0.3 # For setting maximum distance between a bucket and burried pipe. This value should be positive.


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


parameterSetting(minFreqinLink, maxFreqinLink, minDisinLink, maxDisinLink)    
    
def pre_step(extension):
    # extension
    disval = extension.inputs.DistanceL.value 
    global serialConnectionTrigger
    if (disval <= maxDisinLink and disval>=minDisinLink and serialConnectionTrigger == 0):
        StimGenerator(0, mode, 1, float(maxDisinLink+1))
        #StimGenerator(0, mode, 1, float(disval))
        for _ in range(10):
            StimGenerator(1, mode, 2)
            print("Activated Standy")
        serialConnectionTrigger = 1
    elif (disval <= maxDisinLink and disval>=minDisinLink and serialConnectionTrigger == 1):
        StimGenerator(2, mode, 3, float(disval) )
        print("Activated", disval)
    elif ((disval > maxDisinLink or disval < minDisinLink) and serialConnectionTrigger == 1 ):
        StimGenerator(2, mode, 3, float(maxDisinLink+1))
        StimGenerator(3, mode, 4)
        for _ in range(10):
            print("Abort Standy")
        serialConnectionTrigger = 0    
