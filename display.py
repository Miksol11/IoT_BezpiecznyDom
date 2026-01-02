import os
try:
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