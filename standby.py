import time
import display
import buttons
import menu
from PIL import Image, ImageDraw, ImageFont
import os
try:
    import RPi.GPIO as GPIO
    from config import *
except ModuleNotFoundError:
    pass

next_state = None
TIMEOUT = 10  # sekund

def standbyMode():
    buttons.connectGreenButton(wakeUp)
    buttons.connectRedButton(wakeUp)
    buttons.connectEncoderLeft(wakeUp)
    buttons.connectEncoderRight(wakeUp)

    enter_time = time.time()
    logoScreen()
    while True:
        if enter_time >= 0 and time.time() - enter_time >= TIMEOUT:
            blackScreen()
            enter_time = -1
        if next_state:
            return next_state

def wakeUp():
    global next_state
    next_state = "menu"

def logoScreen():
    logo = Image.open(os.path.join("./images/logo.png")).convert("RGB")
    display.show(logo)

def blackScreen():
    black_image = Image.new("RGB", display.SCREEN_RESOLUTION, "black")
    display.show(black_image)

if __name__ == "__main__":
    standbyMode()