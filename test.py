from PIL import Image, ImageDraw, ImageFont
import display
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_FILE = os.path.join(SCRIPT_DIR, 'sources', 'Font.ttf')

#Ekrany z trybu logowania
def test():
    image = Image.new("RGB", display.SCREEN_RESOLUTION, "WHITE")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_FILE, 12)
    big_font = ImageFont.truetype(FONT_FILE, 20)
    draw.rectangle((0, 0, 96, 15), fill="BLACK")
    draw.text((5, 0), "Wprowadź PIN:", font=font, fill="WHITE")
    draw.text((26, 10), "- - - -", font=big_font, fill="BLACK")
    draw.text((24, 32), "< 3 >", font=big_font, fill="BLACK")
    display.show(image)

def test2():
    image = Image.new("RGB", display.SCREEN_RESOLUTION, "WHITE")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_FILE, 12)
    second_font = ImageFont.truetype(FONT_FILE, 10)
    draw.text((0, 0), "Wprowadzono", font=font, fill="BLACK")
    draw.text((0, 15), "niepoprawny", font=font, fill="BLACK")
    draw.text((0, 30), "PIN", font=font, fill="BLACK")
    draw.text((0, 50), "Pozostałe próby: 2", font=second_font, fill="BLACK")
    display.show(image)

def test3():
    image = Image.new("RGB", display.SCREEN_RESOLUTION, "WHITE")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_FILE, 12)
    draw.rectangle((0, 0, 96, 15), fill="BLACK")
    draw.text((5, 0), "Tryb czuwania:", font=font, fill="WHITE")
    draw.rectangle((30, 30, 66, 45), outline="BLACK")
    draw.text((31, 29), "Wyjdź", font=font, fill="BLACK")
    display.show(image)



#Ekrany z trybu z kartami

# Menu główne kart: Karty / Usuń / Dodaj
def test_cards_menu():
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
    display.show(image)

# Menu główne kart z zaznaczonym "Usuń"
def test_cards_menu_remove_selected():
    image = Image.new("RGB", display.SCREEN_RESOLUTION, "WHITE")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_FILE, 12)
    draw.rectangle((0, 0, 96, 15), fill="BLACK")
    draw.text((25, 0), "Karty", font=font, fill="WHITE")
    draw.rectangle((20, 22, 76, 37), fill="BLACK")
    draw.text((35, 23), "Usuń", font=font, fill="WHITE")
    draw.rectangle((20, 42, 76, 57), outline="BLACK")
    draw.text((32, 43), "Dodaj", font=font, fill="BLACK")
    display.show(image)

# Menu główne kart z zaznaczonym "Dodaj"
def test_cards_menu_add_selected():
    image = Image.new("RGB", display.SCREEN_RESOLUTION, "WHITE")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_FILE, 12)
    draw.rectangle((0, 0, 96, 15), fill="BLACK")
    draw.text((25, 0), "Karty", font=font, fill="WHITE")
    draw.rectangle((20, 22, 76, 37), outline="BLACK")
    draw.text((35, 23), "Usuń", font=font, fill="BLACK")
    draw.rectangle((20, 42, 76, 57), fill="BLACK")
    draw.text((32, 43), "Dodaj", font=font, fill="WHITE")
    display.show(image)

# Lista kart do usuwania
def test_remove_card_list():
    image = Image.new("RGB", display.SCREEN_RESOLUTION, "WHITE")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_FILE, 12)
    small_font = ImageFont.truetype(FONT_FILE, 10)
    draw.rectangle((0, 0, 96, 15), fill="BLACK")
    draw.text((10, 0), "Usuń kartę:", font=font, fill="WHITE")
    # Lista przykładowych kart
    draw.rectangle((5, 18, 91, 30), fill="BLACK")
    draw.text((8, 18), "> Karta 1", font=small_font, fill="WHITE")
    draw.text((8, 32), "  Karta 2", font=small_font, fill="BLACK")
    draw.text((8, 44), "  Karta 3", font=small_font, fill="BLACK")
    display.show(image)

# Lista kart do dodawania (przyłóż kartę)
def test_add_card_waiting():
    image = Image.new("RGB", display.SCREEN_RESOLUTION, "WHITE")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_FILE, 12)
    small_font = ImageFont.truetype(FONT_FILE, 10)
    draw.rectangle((0, 0, 96, 15), fill="BLACK")
    draw.text((5, 0), "Dodaj kartę:", font=font, fill="WHITE")
    draw.text((10, 25), "Przyłóż kartę", font=font, fill="BLACK")
    draw.text((15, 42), "do czytnika", font=font, fill="BLACK")
    display.show(image)

# Karta dodana pomyślnie
def test_card_added_success():
    image = Image.new("RGB", display.SCREEN_RESOLUTION, "WHITE")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_FILE, 12)
    small_font = ImageFont.truetype(FONT_FILE, 10)
    draw.rectangle((0, 0, 96, 15), fill="BLACK")
    draw.text((5, 0), "Dodaj kartę:", font=font, fill="WHITE")
    draw.text((5, 22), "Karta", font=small_font, fill="BLACK")
    draw.text((5, 35), "dodana", font=small_font, fill="BLACK")
    draw.text((5, 48), "pomyślnie!", font=small_font, fill="BLACK")
    display.show(image)

# Karta usunięta pomyślnie
def test_card_removed_success():
    image = Image.new("RGB", display.SCREEN_RESOLUTION, "WHITE")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_FILE, 12)
    small_font = ImageFont.truetype(FONT_FILE, 10)
    draw.rectangle((0, 0, 96, 15), fill="BLACK")
    draw.text((5, 0), "Usuń kartę:", font=font, fill="WHITE")
    draw.text((5, 22), "Karta", font=small_font, fill="BLACK")
    draw.text((5, 35), "usunięta", font=small_font, fill="BLACK")
    draw.text((5, 48), "pomyślnie!", font=small_font, fill="BLACK")
    display.show(image)

# Karta już istnieje (błąd)
def test_card_already_exists():
    image = Image.new("RGB", display.SCREEN_RESOLUTION, "WHITE")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_FILE, 12)
    small_font = ImageFont.truetype(FONT_FILE, 10)
    draw.rectangle((0, 0, 96, 15), fill="BLACK")
    draw.text((5, 0), "Błąd!", font=font, fill="WHITE")
    draw.text((5, 22), "Karta została", font=small_font, fill="BLACK")
    draw.text((5, 35), "już wcześniej", font=small_font, fill="BLACK")
    draw.text((5, 48), "dodana.", font=small_font, fill="BLACK")
    display.show(image)

# Potwierdzenie usunięcia karty
def test_confirm_remove_card():
    image = Image.new("RGB", display.SCREEN_RESOLUTION, "WHITE")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_FILE, 12)
    small_font = ImageFont.truetype(FONT_FILE, 10)
    draw.rectangle((0, 0, 96, 15), fill="BLACK")
    draw.text((15, 0), "Potwierdź:", font=font, fill="WHITE")
    draw.text((5, 18), "Usunąć kartę?", font=small_font, fill="BLACK")
    draw.rectangle((5, 35, 45, 50), fill="BLACK")
    draw.text((15, 36), "Tak", font=font, fill="WHITE")
    draw.rectangle((50, 35, 90, 50), outline="BLACK")
    draw.text((60, 36), "Nie", font=font, fill="BLACK")
    display.show(image)

# Brak kart do usunięcia
def test_no_cards():
    image = Image.new("RGB", display.SCREEN_RESOLUTION, "WHITE")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_FILE, 12)
    small_font = ImageFont.truetype(FONT_FILE, 10)
    draw.rectangle((0, 0, 96, 15), fill="BLACK")
    draw.text((10, 0), "Usuń kartę:", font=font, fill="WHITE")
    draw.text((15, 28), "Brak kart", font=font, fill="BLACK")
    display.show(image)

if __name__ == "__main__":
    # Ekrany logowania:
    #test()      # PIN input
     test2()     # Niepoprawny PIN
    # Ekran czuwania:
    # test3()     # Tryb czuwania
    
    # Ekrany kart:
    # test_cards_menu()                # Menu: Karty
    # test_cards_menu_remove_selected() # Menu z zaznaczonym Usuń
    # test_cards_menu_add_selected()   # Menu z zaznaczonym Dodaj
    # test_remove_card_list()          # Lista kart do usunięcia
    # test_add_card_waiting()          # Czekanie na przyłożenie karty
    # test_card_added_success()        # Karta dodana
    # test_card_removed_success()      # Karta usunięta
    # test_card_already_exists()       # Karta już istnieje
    # test_confirm_remove_card()       # Potwierdzenie usunięcia
    # test_no_cards()                  # Brak kart