# 위에 꺼랑 맞추어야 함
# Before using this section, please resstart the current kernel.
# To use this function, please follow this steps.
# 1) First , initiate this mode by clicking "1) Mode."
# 2) Second, turn on or turn off stim by clicking "2) Stim On" or "3) Stim Off."
# 3) Third, turn off the mode by clicking "3) Mode Abort."
from ExcavatorStim import StimGenerator
from tkinter import *
minFreq = 10 # 절대로 지우지 말것
maxFreq = 100 # 절대로 지우지 말것
mode = 20
modeReadyStatus = False
modeAbortStatus = False

root=Tk()
root.wm_attributes("-topmost", 1) # 창 제일 위에 올라오게 하기
root.title("Stimulation amplitude / frequency adjustment")
root.geometry("600x600+0+0")#창 크기조절,좌표.
root.resizable(False, False)#창 크기변경 가능 불가능.
currStatus = Label(root, text = 'Current status: ', font = ("Timex new roman",20))
currStatus.place(x=0, y=320)
currStatusInfo = Label(root, text = '                        ', font = ("Timex new roman",20), relief = "solid", padx=5, pady=5, background="white")
currStatusInfo.place(x=200, y=320)
labelfreqS = Label(root, text = 'Current frequency [Hz]: ', font = ("Timex new roman",20))
labelfreqS.place(x=0, y=400)
freq  = minFreq  # 절대로 지우지 말것
labelfreq = Label(root, text =  str(freq), font = ("Timex new roman",20), relief = "solid", padx=5, pady=5, background="white")
labelfreq.place(x=330, y=400)

def AdjustmentModeReady():
    global modeReadyStatus
    global modeAbortStatus
    if modeReadyStatus == False:
        StimGenerator(0, mode, 1)
        modeReadyStatus = True
        modeAbortStatus = True
        currStatusInfo.config(text="Mode Ready")

def StimOn():
    if modeReadyStatus == True:
        StimGenerator(2, mode, 3, freq)
        print("stim Applied")
        currStatusInfo.config(text="Stim On")
    
def StimOff():
    if modeReadyStatus == True:
        StimGenerator(2, mode, 3, 0)
        print("Stim off")
        currStatusInfo.config(text="Stim Off")
    
def AdjustmentModeAbort():
    if modeAbortStatus == True:
        StimGenerator(3, mode, 4)
        modeReadyStatus = False
        currStatusInfo.config(text="Mode Abbort")
        root.destroy()

def Increase_functions():
    if modeReadyStatus == True:
        global freq
        freq += 5
        if freq > maxFreq:
            freq = maxFreq
        labelfreq.config(text=str(freq))
        StimOn()
        #print(buttonIncrease.text)
    
def Decrease_functions():
    if modeReadyStatus == True:
        global freq
        freq -= 5
        if freq < minFreq:
            freq = minFreq
        labelfreq.config(text=str(freq))
        StimOn()
        #print(buttonIncrease.text)
        
def emergency_Serial_close():
    if modeAbortStatus == True:
        StimGenerator(3, mode, 4)
        modeReadyStatus = False
        root.destroy()
        

buttonReady = Button(root, text = "1) Mode Ready", command=AdjustmentModeReady, height=3, width=84, activebackground = "red", overrelief="solid")     
buttonReady.place(x=0, y=10)

buttonReady = Button(root, text = "2) Stim On", command=StimOn, height=3, width=84, activebackground = "red", overrelief="solid")    
buttonReady.place(x=0, y=80)

buttonReady = Button(root, text = "2) Stim Off", command=StimOff, height=3, width=84, activebackground = "red",overrelief="solid")  
buttonReady.place(x=0, y=150)

buttonReady = Button(root, text = "3) Mode Abort", command=AdjustmentModeAbort, height=3, width=84, activebackground = "red",overrelief="solid")    
buttonReady.place(x=0, y=220)

buttonIncrease = Button(root, text = "+5 Hz", command=Increase_functions,height=2, width=15, activebackground = "red",overrelief="solid")   
buttonIncrease.place(x=0, y=450)

buttonDecrease = Button(root, text = "-5 Hz", command=Decrease_functions, height=2, width=15, activebackground = "red", overrelief="solid")
buttonDecrease.place(x=300, y=450)

buttonDecrease = Button(root, text = "Forcing serial Close", command=emergency_Serial_close, height=2, width=15, bg = "red", fg = "yellow", activebackground = "red",overrelief="solid")
buttonDecrease.place(x=460, y=550)

root.mainloop()
#print(freq)