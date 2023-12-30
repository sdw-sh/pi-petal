import RPi.GPIO as GPIO


def initialize_board():
    GPIO.setmode(GPIO.BOARD)
