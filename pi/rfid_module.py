import time
import datetime

HARDWARE_AVAILABLE = False
try:
    import RPi.GPIO as GPIO
    from config import *
    from mfrc522 import MFRC522
    import board
    import neopixel
    HARDWARE_AVAILABLE = True
except (ImportError, NotImplementedError, ModuleNotFoundError):
    print("Ostrzeżenie: Brak bibliotek sprzętowych (RPi.GPIO, mfrc522, neopixel). Uruchamiam w trybie symulacji.")
    HARDWARE_AVAILABLE = False
    buzzerPin = 23
    
    class MFRC522:
        pass

KEYBOARD_AVAILABLE = False
try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    pass

reader = None
pixels = None
card_present = False
stable_reads = 0
already_initialized = False

def init():
    global reader, pixels, HARDWARE_AVAILABLE, already_initialized
    
    if already_initialized or not HARDWARE_AVAILABLE:
        return

    try:
        reader = MFRC522()
        
        pixels = neopixel.NeoPixel(board.D18, 8, brightness=1.0/32, auto_write=False)
        pixels.fill((0, 0, 0))
        pixels.show()
        
    except Exception as e:
        print(f"Błąd inicjalizacji sprzętu RFID/LED: {e}")
        HARDWARE_AVAILABLE = False

    already_initialized = True

def effects(state, success=True):
    global pixels
    if not HARDWARE_AVAILABLE:
        return

    gpio_state = 0 if state else 1
    GPIO.output(buzzerPin, gpio_state)

    if state:
        if success:
            pixels.fill((0, 0, 255))
        else:
            pixels.fill((255, 0, 0))
        pixels.show()
    else:
        pixels.fill((0, 0, 0))
        pixels.show()

def uid_to_int(uid):
    num = 0
    for i in range(len(uid)):
        num += uid[i] << (i * 8)
    return num


def check_card():
    global reader, card_present, stable_reads
    
    if not HARDWARE_AVAILABLE:
        if KEYBOARD_AVAILABLE:
            simulated_uid = None
            if keyboard.is_pressed('1'):
                simulated_uid = 111111
            elif keyboard.is_pressed('2'):
                simulated_uid = 222222
            elif keyboard.is_pressed('3'):
                simulated_uid = 333333

            if simulated_uid:
                stable_reads = 0
                if not card_present:
                    print(f"SYMULACJA: Wykryto kartę UID: {simulated_uid}")
                    effects(True)
                    time.sleep(0.2)
                    effects(False)
                    card_present = True
                    return simulated_uid
            else:
                stable_reads += 1
                if stable_reads >= 5:
                    card_present = False
        return None

    if reader is None:
        return None

    (status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)

    if status == reader.MI_OK:
        (status, uid) = reader.MFRC522_Anticoll()
        if status == reader.MI_OK:
            stable_reads = 0
            uid_num = uid_to_int(uid)
            
            if not card_present:
                print("UID: ", uid_num, " Time: ", datetime.datetime.now().strftime("%H:%M:%S"))
                
                effects(True)
                time.sleep(0.2)
                effects(False)
                
                card_present = True
                return uid_num
            
            return None 

    else:
        stable_reads += 1
        if stable_reads >= 5:
            card_present = False
            
    return None

def main():
    init()
    try:
        print("Czekam na karty...")
        while True:
            uid = check_card()
            if uid:
                print(f"--> Odczytano w pętli głównej: {uid}")
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        if HARDWARE_AVAILABLE:
            GPIO.cleanup()

if __name__ == "__main__":
    main()
