import display
import buttons
import time
try:
    import RPi.GPIO as GPIO
    from config import *
except ModuleNotFoundError:
    pass

def cardsMode():
    buttons.connectGreenButton()
    buttons.connectRedButton()
    buttons.connectEncoderLeft()
    buttons.connectEncoderRight()
  
    