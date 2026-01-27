import buttons
import display
import screens
import time
try:
    import RPi.GPIO as GPIO
    from config import *
except ModuleNotFoundError:
    pass

class Page:
    def __init__(self, name, image):
        self.name = name
        self.image = image

pages = [
    Page("pogoda", screens.getWeatherScreen),
    Page("karty", lambda: screens.getCardsMenuScreen(2)),
    Page("standbyConfirm", lambda: screens.getStandbyScreen(False))
]
current_page_index = 0
next_state = None
needs_redraw = True

def menuMode():
    global current_page_index, needs_redraw, next_state

    current_page_index = 0
    next_state = None
    needs_redraw = True
    
    buttons.connectGreenButton(selectPage)
    buttons.connectRedButton(lambda: None)
    buttons.connectEncoderLeft(previousPage)
    buttons.connectEncoderRight(nextPage)
    
    while True:
        if next_state:
            return next_state
        if needs_redraw:
            image = pages[current_page_index].image()
            display.show(image)
            needs_redraw = False
        time.sleep(0.05)

def changePage(value):
    global current_page_index, needs_redraw
    
    new_index = (current_page_index + value) % len(pages)
    
    if new_index != current_page_index:
        current_page_index = new_index
        needs_redraw = True

def nextPage():
    changePage(1)
    
def previousPage():
    changePage(-1)

def selectPage():
    global next_state
    if pages[current_page_index].name != "pogoda":
        next_state = pages[current_page_index].name

if __name__ == "__main__":
    result = menuMode()
    print(f"Twój następny widok: {result}")