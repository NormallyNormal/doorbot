import RPi.GPIO as GPIO
import time
import mpu6050
from flask import Flask
from threading import Thread
import asyncio
from websockets.sync.client import connect

mpu6050 = mpu6050.mpu6050(0x68)

opening = False

#This runs on the door clients
#Don't need to call anything here from the server

def open_routine():
    global opening
    if opening:
        return
    opening = True
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18,GPIO.OUT)
    servo = GPIO.PWM(18,50)
    servo.start(0)

    servo.ChangeDutyCycle(12.5)
    timeout = 30   # [seconds]
    timeout_start = time.time()
    while time.time() < timeout_start + timeout:
        test = mpu6050.get_gyro_data()['y']
        if abs(test) > 30:
            break
    servo.ChangeDutyCycle(2.5)
    time.sleep(2)
    servo.stop()
    GPIO.cleanup()
    opening = False
    return

async def websocket_connect():
    with connect("ws://10.137.3.146:8765") as websocket:
        websocket.send("room403 password123")
        print("Connected")
        while True:
            message = websocket.recv()
            Thread(target=open_routine).start()
            print(f"Received: {message}")

if __name__=='__main__':
    while True:
        try:
            asyncio.run(websocket_connect())
        except:
            print("Unable to connect... retry in 5 seconds")
            time.sleep(5)
        
