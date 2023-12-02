import time
import RPi.GPIO as GPIO
from ADCDevice import *

# Adding a soil moisture sensor and a relay to the board
# closing the relay upon the moisture sensor falling dry
# might control a pump in a later setup

adc = ADCDevice()

relay_pin = 16 # GPIO23

percentage_cutoff = 75 # if percentage falls under zhis value the relais is closed

def setup():
    global adc
    if adc.detectI2C(0x4b):
        adc = ADS7830()
        print("ADC found")
    else:
        print("ADC not found")
        exit(-1)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(relay_pin, GPIO.OUT, initial = GPIO.LOW)
    print ('using pin %d to control the relay' %relay_pin)

def loop():
    while True:
        value = adc.analogRead(1)
        voltage = value / 255 * 3.3
        percentage = value / 2.55
        print ('ADC value: %s, Voltage: %.2f, Percentage: %s' %(
            f"{value:>3}", 
            voltage, 
            f"{round(percentage):>3}"
        ))
        time.sleep(0.2)
        if percentage_cutoff < percentage:
            GPIO.output(relay_pin, GPIO.HIGH)
        else:
            GPIO.output(relay_pin, GPIO.LOW)

def destroy():
    adc.close()
    GPIO.cleanup()
    print("\nProgram terminated regularly")
    print("Have a nice day\n")

if __name__ == '__main__':
    print ("Starting")
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        destroy()
