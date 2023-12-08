#!/usr/bin/python
import RPi.GPIO as GPIO
import time

# Test for the AZ-Delivery soil moisture sensor
# using the digital out
# simply taken from the manual
# working as expected
# ao can be tested using freenove-kit/ADCLog.py

# GPIO SETUP
sensorpin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensorpin, GPIO.IN)


def checkmoinsture(sensorpin):
    if GPIO.input(sensorpin):
        print("no water detected")
    else:
        print("water detected")


# detect pin goes HIGH or LOW
GPIO.add_event_detect(sensorpin, GPIO.BOTH, bouncetime=300)

# Lunch callback
GPIO.add_event_callback(sensorpin, checkmoinsture)

# infinite loop
while True:
    time.sleep(1)
