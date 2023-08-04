from test_only_distance import pre_step
inputValue = 0
while True:
    inputCharacter = input("Input: ")
    if inputCharacter == "e":
        break
    elif inputCharacter == "a":
        inputValue+=0.05
        print("InputValue: ", inputValue)
    elif inputCharacter == "d":
        inputValue-=0.05
        print("InputValue: ",inputValue)
    pre_step(inputValue)