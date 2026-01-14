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
current_page_index = 0
needs_redraw = True  # Flaga: czy trzeba odświeżyć ekran?

def menuMode():
    global current_page_index, needs_redraw
    
    # 1. Podpinamy przyciski - one tylko zmieniają zmienne!
    buttons.connectGreenButton(selectPage)
    buttons.connectRedButton(lambda: None)
    buttons.connectEncoderLeft(previousPage)
    buttons.connectEncoderRight(nextPage)
    
    # Wymuś pierwsze rysowanie
    needs_redraw = True
    
    while True:
        # 2. Jeśli wybrano opcję, wyjdź
        if next_state:
            return next_state
        
        # 3. Rysowanie odbywa się TYLKO w pętli głównej i TYLKO gdy coś się zmieniło
        if needs_redraw:
            # Rysujemy
            display.show(pages[current_page_index].image)
            # Resetujemy flagę - ekran jest aktualny
            needs_redraw = False
        
        # Krótki sleep, żeby nie zarzynać procesora, ale na tyle krótki, by reagować szybko
        time.sleep(0.05)

def changePage(value):
    global current_page_index, needs_redraw
    
    # Oblicz nową stronę
    new_index = (current_page_index + value) % len(pages)
    
    # Jeśli faktycznie zmieniła się strona (zabezpieczenie)
    if new_index != current_page_index:
        current_page_index = new_index
        needs_redraw = True # Zgłoś pętli głównej, że trzeba przerysować

def nextPage():
    changePage(1)
    
def previousPage():
    changePage(-1)

def selectPage():
    global next_state
    next_state = pages[current_page_index].name

if __name__ == "__main__":
    menuMode()