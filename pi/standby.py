import time
import display
import buttons
import screens
import rfid_module
import mqtt
HARDWARE_AVAILABLE = False
try:
    import RPi.GPIO as GPIO
    from config import *
    HARDWARE_AVAILABLE = True
except ModuleNotFoundError:
    pass

next_state = None
TIMEOUT = 10  # sekund

def standbyMode():
    global next_state

    buttons.connectGreenButton(wakeUp)
    buttons.connectRedButton(wakeUp)
    buttons.connectEncoderLeft(wakeUp)
    buttons.connectEncoderRight(wakeUp)

    next_state = None

    enter_time = time.time()
    logoScreen()
    while True:
        result = rfid_module.check_card(False)
        if result:
            is_card_good = mqtt.card_exists(str(result))
            effects(is_card_good)
        if enter_time >= 0 and time.time() - enter_time >= TIMEOUT:
            blackScreen()
            
            enter_time = -1
        if next_state:
            return next_state
        sendData()
        time.sleep(0.05)


def effects(success):
    global pixels
    if not HARDWARE_AVAILABLE:
        print("efekty świelne i dzwiękowe (to ważne)")
        return

    if success:
        pixels.fill((0, 0, 255))
        pixels.show()
        GPIO.output(buzzerPin, 0)
        time.sleep(1)
    else:
        pixels.fill((255, 0, 0))
        pixels.show()
        GPIO.output(buzzerPin, 0)
        time.sleep(0.1)
        GPIO.output(buzzerPin, 1)
        time.sleep(0.2)
        GPIO.output(buzzerPin, 0)
        time.sleep(0.1)
        GPIO.output(buzzerPin, 1)
        time.sleep(0.2)
        GPIO.output(buzzerPin, 0)
        time.sleep(0.1)

    GPIO.output(buzzerPin, 1)
    pixels.fill((0, 0, 0))
    pixels.show()

def standbyConfirmMode():
    global next_state

    buttons.connectGreenButton(goStandby)
    buttons.connectRedButton(goMenu)
    buttons.connectEncoderLeft(lambda: None)
    buttons.connectEncoderRight(lambda: None)

    next_state = None

    image = screens.getStandbyScreen(True)
    display.show(image)

    while True:
        if next_state:
            return next_state
        time.sleep(0.05)

def goStandby():
    global next_state
    next_state = "standby"

def goMenu():
    global next_state
    next_state = "menu"

def wakeUp():
    global next_state
    next_state = "login"

def logoScreen():
    logo = screens.getLogoScreen()
    display.show(logo)

def blackScreen():
    black_image = screens.getBlackScreen()
    display.show(black_image)

def sendData():
    # temperature = measurements.getTemperature()
    # pressure = measurements.getPressure()
    # humidity = measurements.getHumidity()
    # altitude = measurements.getAltitude()
    # print(temperature, pressure, humidity, altitude)
    pass

if __name__ == "__main__":
    standbyMode()