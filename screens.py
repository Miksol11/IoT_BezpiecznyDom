import display
import os
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_FILE = os.path.join(SCRIPT_DIR, 'sources', 'Font.ttf')
LOGO_FILE = os.path.join(SCRIPT_DIR, 'images', 'logo.png')

def getBlackScreen():
    return Image.new("RGB", display.SCREEN_RESOLUTION, "black")

def getLogoScreen():
    return Image.open(LOGO_FILE).convert("RGB")

def getPinScreen(current_digit, current_pass):
    password = len(current_pass) * "* "
    password += (4 - len(current_pass)) * "- "
    password = password.rstrip()

    image = Image.new("RGB", display.SCREEN_RESOLUTION, "WHITE")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_FILE, 12)
    big_font = ImageFont.truetype(FONT_FILE, 20)
    draw.rectangle((0, 0, 96, 15), fill="BLACK")
    draw.text((5, 0), "Wprowadź PIN:", font=font, fill="WHITE")
    draw.text((26, 10), password, font=big_font, fill="BLACK")
    draw.text((24, 32), f"< {current_digit} >", font=big_font, fill="BLACK")

    return image

def getWeatherScreen():
    return getPinScreen('P', "")

def getCardScreen():
    image = Image.new("RGB", display.SCREEN_RESOLUTION, "WHITE")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_FILE, 12)
    big_font = ImageFont.truetype(FONT_FILE, 14)
    draw.rectangle((0, 0, 96, 15), fill="BLACK")
    draw.text((25, 0), "Karty", font=font, fill="WHITE")
    draw.rectangle((20, 22, 76, 37), outline="BLACK")
    draw.text((35, 23), "Usuń", font=font, fill="BLACK")
    draw.rectangle((20, 42, 76, 57), outline="BLACK")
    draw.text((32, 43), "Dodaj", font=font, fill="BLACK")
    return image

def getStandbyScreen(is_confirmation):
    if is_confirmation:
        first_color = "BLACK"
        second_color = "WHITE"
    else:
        first_color = "WHITE"
        second_color = "BLACK"

    image = Image.new("RGB", display.SCREEN_RESOLUTION, "WHITE")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_FILE, 12)
    draw.rectangle((0, 0, 96, 15), fill=second_color)
    draw.text((5, 0), "Tryb czuwania:", font=font, fill=first_color)
    if is_confirmation:
        draw.rectangle((30, 30, 66, 45), fill="BLACK")
    else:
        draw.rectangle((30, 30, 66, 45), outline="BLACK")
    
    draw.text((31, 29), "Wyjdź", font=font, fill=second_color)
    return image

if __name__ == "__main__":
    print("siems")