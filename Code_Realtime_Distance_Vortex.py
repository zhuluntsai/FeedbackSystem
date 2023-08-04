import Vortex
import math
 
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

def pre_step(extension):
    
    if(extension.inputs.DistanceL.value < 0.3):
        val = extension.inputs.DistanceL.value
        print(val)
    

        