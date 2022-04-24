import gas_leakage as ga
import RPi.GPIO as GPIO
from time import sleep
import os
import threading
import requests
import urllib
import urllib.request     
import RPi.GPIO as GPIO
import dht11
import time
import socket
import datetime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def readSensor():
    global temperature
    global humidity
    global gas
    global metal

    temperature =0
    humidity=0
    gas=0
    metal =0
    
    
# read data using Pin GPIO21 
    instance = dht11.DHT11(pin=4)
    while True:
        result = instance.read()
        if result.is_valid():
            temperature=result.temperature
            humidity=result.humidity
        if(temperature and humidity):
            break
            ## print("Temp: %d C" % result.temperature +' '+"Humid: %d %%" % result.humidity)
            ## time.sleep(1)
    
    ##print(f'Temperature: {temperature} degrees')
    gas=ga.gasleak()
    ##print(gas)
    metal=ga.metaldetect()
    ##print(metal)
    

def get_ip_address():
    ip_address = '';
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

def sendDataToServer():
    global temperature
    global humidity
    global gas
    global metal
    threading.Timer(600,sendDataToServer).start()
    print("\nSensing...")
    readSensor()
    temperature = round(temperature,1)
    humidity=round(humidity,1)
    gas=round(gas,1)
    metal=round(metal,1)
    ##print(temperature)
    print(f"Temperature: {temperature}\N{DEGREE SIGN} Celcius")
    print(f"Humidity: {humidity}%")
    ##print(f"gas: {gas}")
    is_metal_detected = bool(metal)
    is_gas_detected = bool(gas)
    if gas:
        print("gas detected!!!")
    else:
        print("No gas detected.")
        
    if metal == 1:
        print("metal detected!!!")
    else:
        print("No metal detected on the surface.")
    
    temp= "%.1f" %temperature
    hum ="%.1f" %humidity
    gas = "%.1f" %gas
    metal="%.1f" %metal
    print(temp,hum,gas,metal)
    
    urllib.request.urlopen("https://iotcloud22.in/Army/post_value.php?value1="+temp+"&value2="+hum+"&value3="+gas+"&value4="+metal).read()
    ip_address = get_ip_address()
    PORT = 5000
    url = f"http://{ip_address}:{PORT}/add_sensor_data"
    data = {
        'temperature': temp,
        'humidity': hum,
        'is_metal_detected': is_metal_detected,
        'is_gas_detected': is_gas_detected,
    }
    try:
        requests.post(url, data=data)
        print("sensor data successfully sent to the server.")
    except Exception:
        return "Cannot send data to the serve. Server is not listening."

while True:
    sendDataToServer()
