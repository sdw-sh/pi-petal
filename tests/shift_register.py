#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
# Defines the data bit that is transmitted preferentially in the shiftOut function.
LSBFIRST = 1
MSBFIRST = 2
# define the pins for 74HC595
dataPin   = 11      # DS Pin of 74HC595(Pin14)
latchPin  = 13      # ST_CP Pin of 74HC595(Pin12)
clockPin = 15       # CH_CP Pin of 74HC595(Pin11)

def setup():
    GPIO.setmode(GPIO.BOARD)    # use PHYSICAL GPIO Numbering
    GPIO.setup(dataPin, GPIO.OUT) # set pin to OUTPUT mode
    GPIO.setup(latchPin, GPIO.OUT)
    GPIO.setup(clockPin, GPIO.OUT)
    
# shiftOut function, use bit serial transmission. 
def shiftOut(dPin,cPin,order,val):
    for i in range(0,8):
        GPIO.output(cPin,GPIO.LOW);
        if(order == LSBFIRST):
            GPIO.output(dPin,(0x01&(val>>i)==0x01) and GPIO.HIGH or GPIO.LOW)
        elif(order == MSBFIRST):
            GPIO.output(dPin,(0x80&(val<<i)==0x80) and GPIO.HIGH or GPIO.LOW)
        GPIO.output(cPin,GPIO.HIGH);

def set_led():
    _led_state = 0b11111111
    led_state = 0b10000000
    
    for i in range(8):
        GPIO.output(latchPin,GPIO.LOW)
        GPIO.output(clockPin,GPIO.LOW)
        bit = (led_state >> i) & 1
        print('---')
        print(i)
        print(bit) 
        GPIO.output(dataPin, bit)
        GPIO.output(clockPin,GPIO.HIGH)
        GPIO.output(latchPin,GPIO.HIGH)
        time.sleep(0.33)
        # Use bitwise AND with 1 to extract the rightmost bit
    
    time.sleep(1000)

        

def loop():
    while True:
        x=0x01
        for i in range(0,8):
            GPIO.output(latchPin,GPIO.LOW)  # Output low level to latchPin
            shiftOut(dataPin,clockPin,LSBFIRST,x) # Send serial data to 74HC595
            GPIO.output(latchPin,GPIO.HIGH) # Output high level to latchPin, and 74HC595 will update the data to the parallel output port.
            x<<=1 # make the variable move one bit to left once, then the bright LED move one step to the left once.
            time.sleep(0.1)
        x=0x80
        for i in range(0,8):
            GPIO.output(latchPin,GPIO.LOW)
            shiftOut(dataPin,clockPin,LSBFIRST,x)
            GPIO.output(latchPin,GPIO.HIGH)
            x>>=1
            time.sleep(0.1)

def destroy(controller):   
    controller.switch_off(0, 1, 2, 3, 4, 5, 6, 7)
    GPIO.cleanup()
    print()
    print('Program terminated regularly')
    print('Did it work as expected?')
    print()

class ShiftRegisterController:
    def __init__(self):
        self.state = 0x00000000
        self._update_register()
        print(self.state)

    def switch_on(self, *args: int):
        for position in args:
            if self._check_position(int(position)):
                self.state = self.state | (1 << int(position))
        print(bin(self.state))
        self._update_register()

    def switch_off(self, *args: int):
        for position in args:
            if self._check_position(int(position)):
                self.state = self.state & ~(1 << int(position))
        print(bin(self.state))
        self._update_register()


    def _check_position (self, position: int):
        if position > 7 or position < 0:
            print(f"WARNING: trying to switch position `{position}` in ShiftRegisterController, this position is invalid.")
            return False
        else:
            return True
        
    def _update_register(self):
        GPIO.output(clockPin,GPIO.LOW)
        for i in range(8):
            bit = (self.state >> i) & 1
            print('---')
            print(i)
            print(bit) 
            GPIO.output(dataPin, bit)
            GPIO.output(clockPin,GPIO.HIGH)
            GPIO.output(clockPin,GPIO.LOW)
        GPIO.output(latchPin,GPIO.HIGH)
        GPIO.output(latchPin,GPIO.LOW)

if __name__ == '__main__': # Program entrance
    print ('Program is starting...' )
    setup() 
    controller = ShiftRegisterController()
    time.sleep(0.5)
    # try:
    #     delay = 0.1
    #     while True:
    #         for i in range(8):
    #             controller.switch_on(i)
    #             time.sleep(delay)
    #         for i in range(8):
    #             controller.switch_off(i)
    #             time.sleep(delay)
    #         for i in range(8):
    #             controller.switch_on(7-i)
    #             time.sleep(delay)
    #         for i in range(8):
    #             controller.switch_off(7-i)
    #             time.sleep(delay)
    #     # loop()
    # #    set_led()
    # except KeyboardInterrupt:  # Press ctrl-c to end the program.
    #     destroy()
    controller.switch_on(0)
    time.sleep(0.5)
    # controller.switch_on(1)
    # time.sleep(0.5)
    # controller.switch_on(7, 6, 7, 9, 2)
    # time.sleep(0.5)
    # controller.switch_off(3, 1, 7, 9, 2)
    # time.sleep(0.5)
    # controller.switch_on(9)
    time.sleep(0.5)
    controller.switch_on(7)
    time.sleep(0.5)

    destroy(controller)



