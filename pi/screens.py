import display
import os
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_FILE = os.path.join(SCRIPT_DIR, 'sources', 'Font.ttf')
LOGO_FILE = os.path.join(SCRIPT_DIR, 'images', 'logo.png')
ICONS_DIR = os.path.join(SCRIPT_DIR, 'icons')

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


#Ekrany Managera Kart

def getCardsMenuScreen(selected_option):
    image = Image.new("RGB", display.SCREEN_RESOLUTION, "WHITE")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_FILE, 12)

    draw.rectangle((0, 0, 96, 15), fill="BLACK")
    draw.text((25, 0), "Karty", font=font, fill="WHITE")

    if selected_option == 0:
        draw.rectangle((20, 22, 76, 37), fill="BLACK")
        draw.text((35, 23), "Usuń", font=font, fill="WHITE")
    else:
        draw.rectangle((20, 22, 76, 37), outline="BLACK")
        draw.text((35, 23), "Usuń", font=font, fill="BLACK")

    if selected_option == 1:
        draw.rectangle((20, 42, 76, 57), fill="BLACK")
        draw.text((32, 43), "Dodaj", font=font, fill="WHITE")
    else:
        draw.rectangle((20, 42, 76, 57), outline="BLACK")
        draw.text((32, 43), "Dodaj", font=font, fill="BLACK")
    
    return image

def getRemoveCardListScreen(card_list, selected_index, scroll_offset):
    image = Image.new("RGB", display.SCREEN_RESOLUTION, "WHITE")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_FILE, 12)
    small_font = ImageFont.truetype(FONT_FILE, 10)
    draw.rectangle((0, 0, 96, 15), fill="BLACK")
    draw.text((10, 0), "Usuń kartę:", font=font, fill="WHITE")

    if not card_list:
        draw.text((15, 28), "Brak kart", font=font, fill="BLACK")
        return image

    MAX_VISIBLE_ITEMS = 3
    ITEM_HEIGHT = 14
    START_Y = 18

    for i in range(MAX_VISIBLE_ITEMS):
        list_index = scroll_offset + i
        if list_index < len(card_list):
            item_y = START_Y + (i * ITEM_HEIGHT)
            card_uid = str(card_list[list_index])
            
            if list_index == selected_index:
                draw.rectangle((5, item_y, 91, item_y + 12), fill="BLACK")
                draw.text((8, item_y), f"> {card_uid}", font=small_font, fill="WHITE")
            else:
                draw.text((8, item_y), f"  {card_uid}", font=small_font, fill="BLACK")
    
    return image

def getAddCardWaitingScreen():
    image = Image.new("RGB", display.SCREEN_RESOLUTION, "WHITE")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_FILE, 12)
    
    draw.rectangle((0, 0, 96, 15), fill="BLACK")
    draw.text((5, 0), "Dodaj kartę:", font=font, fill="WHITE")
    draw.text((10, 25), "Przyłóż kartę", font=font, fill="BLACK")
    draw.text((15, 42), "do czytnika", font=font, fill="BLACK")
    return image

def getConfirmRemoveCardScreen(card_uid):
    image = Image.new("RGB", display.SCREEN_RESOLUTION, "WHITE")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_FILE, 12)
    small_font = ImageFont.truetype(FONT_FILE, 10)
    
    draw.rectangle((0, 0, 96, 15), fill="BLACK")
    draw.text((15, 0), "Potwierdź:", font=font, fill="WHITE")
    draw.text((5, 18), "Usunąć kartę?", font=small_font, fill="BLACK")
    draw.text((5, 28), str(card_uid), font=small_font, fill="BLACK")
    
    draw.text((20, 45), "TAK", font=small_font, fill="GREEN")
    draw.text((60, 45), "NIE", font=small_font, fill="RED")
    
    return image

def getStatusScreen(title, line1, line2="", line3=""):
    image = Image.new("RGB", display.SCREEN_RESOLUTION, "WHITE")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_FILE, 12)
    small_font = ImageFont.truetype(FONT_FILE, 10)
    
    draw.rectangle((0, 0, 96, 15), fill="BLACK")
    draw.text((5, 0), title, font=font, fill="WHITE")
    
    draw.text((5, 22), line1, font=small_font, fill="BLACK")
    draw.text((5, 35), line2, font=small_font, fill="BLACK")
    draw.text((5, 48), line3, font=small_font, fill="BLACK")
    
    return image

def getWeatherScreen(measurements):
    image = Image.new("RGB", display.SCREEN_RESOLUTION, "White")
    if measurements is not None:
        measurements.popitem()
        print(measurements)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(FONT_FILE, 14)
        height = 0
        for key in measurements:
            icon = Image.open(f'{ICONS_DIR}/{key}.png')
            image.paste(icon, (0, height), icon)
            draw.text((18, height), f"{measurements[key]}", font=font, fill="BLACK")
            height+=16

    return image

def testCardsScreens():
    import time
    print("Testowanie widoków...")
    
    print("1. Menu: Usuń")
    display.show(getCardsMenuScreen(0))
    time.sleep(1)
    
    print("2. Menu: Dodaj")
    display.show(getCardsMenuScreen(1))
    time.sleep(1)
    
    print("3. Dodawanie: Przyłóż kartę")
    display.show(getAddCardWaitingScreen())
    time.sleep(1)
    
    print("4. Status: Sukces")
    display.show(getStatusScreen("Dodaj kartę:", "Karta", "dodana", "pomyślnie!"))
    time.sleep(1)
    
    cards = ["111111", "222222", "333333", "444444", "555555"]
    print("5. Lista kart (index 1)")
    display.show(getRemoveCardListScreen(cards, 1, 0))
    time.sleep(1)
    
    print("6. Lista kart (index 4, scroll 3)")
    display.show(getRemoveCardListScreen(cards, 4, 3))
    time.sleep(1)
    
    print("7. Potwierdzenie")
    display.show(getConfirmRemoveCardScreen("333333"))
    time.sleep(1)

    print("Test zakończony.")

if __name__ == "__main__":
    testCardsScreens()