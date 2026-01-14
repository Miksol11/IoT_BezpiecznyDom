import os
import sys
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)
    import lib.oled.SSD1331 as SSD1331
    display_available = True
except ModuleNotFoundError:
    display_available = False
    

SCREEN_RESOLUTION = (96, 64)
_disp = None

def getDisp():
    global _disp
    if _disp is None:
        os.system('sudo systemctl stop ip-oled.service')
        _disp = SSD1331.SSD1331()
        _disp.Init()
        _disp.clear()
    return _disp
    
def show(image):
    if image.size != SCREEN_RESOLUTION:
        image = image.resize(SCREEN_RESOLUTION)
    if display_available:
        disp = getDisp()
        disp.ShowImage(image, 0, 0) #żeby pokazać IRL na ekraniku
    else:
        image.show() #żeby pokazać na komputerze podczas testów

def test():
    from PIL import Image
    getDisp()
    image = Image.new("RGB", SCREEN_RESOLUTION, "red")
    show(image)

if __name__ == "__main__":
    test()