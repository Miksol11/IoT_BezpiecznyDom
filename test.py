from PIL import Image, ImageDraw, ImageFont
import display

def test():
    image = Image.new("RGB", display.SCREEN_RESOLUTION, "WHITE")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('./sources/Font.ttf', 12)
    big_font = ImageFont.truetype('./sources/Font.ttf', 20)
    draw.rectangle((0, 0, 96, 15), fill="BLACK")
    draw.text((5, 0), "Wprowadź PIN:", font=font, fill="WHITE")
    draw.text((26, 10), "- - - -", font=big_font, fill="BLACK")
    draw.text((24, 32), "< 3 >", font=big_font, fill="BLACK")
    display.show(image)

def test2():
    image = Image.new("RGB", display.SCREEN_RESOLUTION, "WHITE")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('./sources/Font.ttf', 12)
    second_font = ImageFont.truetype('./sources/Font.ttf', 10)
    draw.text((0, 0), "Wprowadzono", font=font, fill="BLACK")
    draw.text((0, 15), "niepoprawny", font=font, fill="BLACK")
    draw.text((0, 30), "PIN", font=font, fill="BLACK")
    draw.text((0, 50), "Pozostałe próby: 2", font=second_font, fill="BLACK")
    display.show(image)

def test3():
    image = Image.new("RGB", display.SCREEN_RESOLUTION, "WHITE")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('./sources/Font.ttf', 12)
    draw.rectangle((0, 0, 96, 15), fill="BLACK")
    draw.text((5, 0), "Tryb czuwania:", font=font, fill="WHITE")
    draw.rectangle((30, 30, 66, 45), outline="BLACK")
    draw.text((31, 29), "Wyjdź", font=font, fill="BLACK")
    display.show(image)

if __name__ == "__main__":
    test()
    #test2()
    #test3()