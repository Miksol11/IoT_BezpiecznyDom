import display
import buttons
import time
import screens
try:
    import RPi.GPIO as GPIO
    from config import *
except ModuleNotFoundError:
    pass

PIN = "0000"
digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
entered_pin = ""
current_digit = '0'
next_state = None
needs_redraw = True

def loginMode():
    global entered_pin, current_digit, next_state, needs_redraw

    entered_pin = "000"
    current_digit = '0'
    next_state = None
    needs_redraw = True

    buttons.connectGreenButton(confirmDigit)
    buttons.connectRedButton(backspaceDigit)
    buttons.connectEncoderLeft(decraseDigit)
    buttons.connectEncoderRight(increaseDigit)
    
    while True:
        if next_state:
            return next_state
        if needs_redraw:
            image = screens.getPinScreen(current_digit, entered_pin)
            display.show(image)
            needs_redraw = False
        time.sleep(0.05)

def changeDigit(value):
    global current_digit, needs_redraw
    current_digit = digits[(digits.index(current_digit) + value) % len(digits)]
    needs_redraw = True

def increaseDigit():
    changeDigit(1)

def decraseDigit():
    changeDigit(-1)

def confirmDigit():
    global entered_pin, next_state, needs_redraw
    entered_pin += current_digit
    if len(entered_pin) == len(PIN):
        if entered_pin == PIN:
            next_state = "menu"
        else:
            next_state = "login"
    else:
        needs_redraw = True

def backspaceDigit():
    global entered_pin, needs_redraw
    if len(entered_pin) > 0:
        entered_pin = entered_pin[:-1]
        needs_redraw = True

if __name__ == "__main__":
    result = loginMode()
    if result == "menu":
        print("Poprawny PIN")
    else:
        print("Niepoprawny PIN")