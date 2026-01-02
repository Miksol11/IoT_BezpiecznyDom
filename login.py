import display
import buttons
import time
try:
    import RPi.GPIO as GPIO
    from config import *
except ModuleNotFoundError:
    pass

PIN = "1234"
digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
entered_pin = ""
current_digit = '0'

def loginMode():
    last_time = 0
    buttons.connectGreenButton(confirmDigit)
    buttons.connectRedButton(backspaceDigit)
    buttons.connectEncoderLeft(decraseDigit)
    buttons.connectEncoderRight(increaseDigit)

    
    while True:
        time.sleep(1)
        print("Current digit: ", current_digit)
        pass

def changeDigit(value):
    global current_digit
    current_digit = digits[(digits.index(current_digit) + value) % len(digits)]

def increaseDigit():
    changeDigit(1)

def decraseDigit():
    changeDigit(-1)

def confirmDigit():
    global entered_pin
    entered_pin += current_digit
    print(entered_pin)
    if len(entered_pin) == len(PIN):
        if entered_pin == PIN:
            print("Wprowadzono cały PIN - dobry")
            entered_pin = ""
        else:
            print("Wprowadzono cały PIN - zły")
            entered_pin = ""

def backspaceDigit():
    global entered_pin
    if len(entered_pin) > 0:
        entered_pin = entered_pin[:-1]
    print(entered_pin)

if __name__ == "__main__":
    loginMode()