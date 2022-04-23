import RPi.GPIO as GPIO
from time import sleep

gas_value=0
metal_value1=0

GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN)
GPIO.setup(18,GPIO.IN)


def gasleak():
    gas_value=0
    if(GPIO.input(18)):
        gas_value=GPIO.input(18)
        ##print("alive")
            
    else:
        gas_value=GPIO.input(18)
        ##print(value)
        ##print("leakage detected...!")
    return gas_value

def metaldetect():
    metal_value = 0
    if(GPIO.input(23)):
        metal_value=GPIO.input(23)
            
    else:
        metal_value=GPIO.input(23)
        ##print(value1)
        ##print("alive")
        
    return metal_value
#gasleak()
##metaldetect()            

        