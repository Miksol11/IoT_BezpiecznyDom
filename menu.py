import buttons
import display
import time
from PIL import Image, ImageDraw, ImageFont
try:
    import RPi.GPIO as GPIO
    from config import *
except ModuleNotFoundError:
    pass

class Page:
    def __init__(self, name, image):
        self.name = name
        self.image = image

next_state = None
pages = [
    Page("pogoda", Image.new("RGB", display.SCREEN_RESOLUTION, "red")),
    Page("karty", Image.new("RGB", display.SCREEN_RESOLUTION, "green")),
    Page("standby", Image.new("RGB", display.SCREEN_RESOLUTION, "blue"))
]
current_page = 0

def menuMode():
    buttons.connectGreenButton(selectPage)
    buttons.connectRedButton(lambda: None)
    buttons.connectEncoderLeft(previousPage)
    buttons.connectEncoderRight(nextPage)
    
    while True:
        if next_state:
            return next_state
        time.sleep(0.1)

def changePage(value):
    global current_page
    current_page += value
    current_page %= len(pages)
    display.show(pages[current_page].image)

def nextPage():
    changePage(1)
    
def previousPage():
    changePage(-1)

def selectPage():
    global next_state
    next_state = pages[current_page].name

if __name__ == "__main__":
    menuMode()