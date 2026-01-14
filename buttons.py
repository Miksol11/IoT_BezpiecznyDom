try:
    import RPi.GPIO as GPIO
    from config import *
    buttons_available = True
except ModuleNotFoundError:
    buttons_available = False
    buttonRed = 5
    buttonGreen = 6
    encoderLeft = 17
    encoderRight = 27
    try:
        import keyboard
    except ModuleNotFoundError:
        keyboard = None

BUTTON_DEBOUNCE_TIME = 200
ENCODER_DEBOUNCE_TIME = 50

connection_dict = {buttonRed: None, buttonGreen: None, encoderLeft: None, encoderRight: None}
button_key_dict = {buttonRed: 'r', buttonGreen: 'g', encoderLeft: "left", encoderRight: "right"}

def connectButton(button, event, encoder=False):
    if buttons_available:
        if connection_dict[button] is not None:
            GPIO.remove_event_detect(button)
        if encoder:
            GPIO.add_event_detect(button, GPIO.FALLING, callback=lambda e: encoderCallback(button, event), bouncetime=ENCODER_DEBOUNCE_TIME)
        else:
            def callback_handler(channel):
                if GPIO.input(channel) == 0:
                    event()
            
            GPIO.add_event_detect(button, GPIO.FALLING, callback=callback_handler, bouncetime=BUTTON_DEBOUNCE_TIME)
                
        connection_dict[button] = True
    else:
        if connection_dict[button] is not None:
            keyboard.unhook_key(button_key_dict[button])
        keyboard.on_press_key(button_key_dict[button], lambda e: event())
        connection_dict[button] = True

def connectRedButton(event):
    connectButton(buttonRed, event)
        
def connectGreenButton(event):
    connectButton(buttonGreen, event)
        
def connectEncoderLeft(event):
    connectButton(encoderLeft, event, True)

def connectEncoderRight(event):
    connectButton(encoderRight, event, True)

def encoderCallback(channel, event):
    if channel == encoderLeft:
        if GPIO.input(encoderRight) == 1:
            event()
    else:
        if GPIO.input(encoderLeft) == 1:
            event()

def test():
    import time

    connectRedButton(lambda: print("Red button pressed"))
    connectGreenButton(lambda: print("Green button pressed"))
    connectEncoderLeft(lambda: print("Encoder turned left"))
    connectEncoderRight(lambda: print("Encoder turned right"))
    
    while True:
        time.sleep(1)
        pass

if __name__ == "__main__":
    test()