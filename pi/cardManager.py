
import time
import buttons
import display
import screens
import rfid_module

try:
    import RPi.GPIO as GPIO
    from pi.config import *
except ModuleNotFoundError:
    pass

STATE_MENU = "MENU"
STATE_ADD_WAIT = "ADD_WAIT"
STATE_REMOVE_LIST = "REMOVE_LIST"
STATE_REMOVE_LIST_WAIT = "REMOVE_LIST_WAIT"
STATE_CONFIRM = "CONFIRM"
STATE_RESULT = "RESULT"

current_state = STATE_MENU
should_exit = False
menu_selected_option = 1
cards_list = []           
list_selected_index = 0   
list_scroll_offset = 0    
card_to_remove = None
result_message = {}       
result_timestamp = 0

needs_redraw = True


mockCards = ["111111", "222222", "123456", "987654"]

def mockAddCard(uid):
    print(f"[BACKEND] Dodawanie karty {uid}...")
    time.sleep(0.5) 
    if str(uid) in mockCards:
        return False
    mockCards.append(str(uid))
    return True

def mockGetCards():
    print(f"[BACKEND] Pobieranie listy kart...")
    time.sleep(0.5)
    return mockCards

def mockDeleteCard(uid):
    print(f"[BACKEND] Usuwanie karty {uid}...")
    time.sleep(0.5)
    if str(uid) in mockCards:
        mockCards.remove(str(uid))
    return True

# --- Logika Sterowania ---

def menuMode():
    global current_state, should_exit, needs_redraw
    global menu_selected_option, list_selected_index, list_scroll_offset, card_to_remove, result_message
    
    current_state = STATE_MENU
    should_exit = False
    needs_redraw = True
    menu_selected_option = 1 
    
    rfid_module.init()
    setupButtonsForState(STATE_MENU)

    while not should_exit:
        handleStateLogic()
        if needs_redraw:
            drawScreen()
            needs_redraw = False
        time.sleep(0.05)
    
    return "menu"

def setupButtonsForState(state):
    if state == STATE_MENU:
        buttons.connectGreenButton(actionMenuConfirm)
        buttons.connectRedButton(actionExit)
        buttons.connectEncoderLeft(lambda: actionMenuChange(-1))
        buttons.connectEncoderRight(lambda: actionMenuChange(1))
        
    elif state == STATE_ADD_WAIT:
        buttons.connectGreenButton(lambda: None)
        buttons.connectRedButton(actionBackToMenu)
        buttons.connectEncoderLeft(lambda: None)
        buttons.connectEncoderRight(lambda: None)
        
    elif state == STATE_REMOVE_LIST:
        buttons.connectGreenButton(actionListSelect)
        buttons.connectRedButton(actionBackToMenu)
        buttons.connectEncoderLeft(lambda: actionListScroll(-1))
        buttons.connectEncoderRight(lambda: actionListScroll(1))
        
    elif state == STATE_CONFIRM:
        buttons.connectGreenButton(actionConfirmDelete)
        buttons.connectRedButton(actionBackToList)
        buttons.connectEncoderLeft(lambda: None)
        buttons.connectEncoderRight(lambda: None)
        
    elif state == STATE_RESULT:
        buttons.connectGreenButton(actionBackToMenu)
        buttons.connectRedButton(actionBackToMenu)
        buttons.connectEncoderLeft(actionBackToMenu)
        buttons.connectEncoderRight(actionBackToMenu)


def handleStateLogic():
    global current_state, needs_redraw
    
    if current_state == STATE_ADD_WAIT:
        uid = rfid_module.check_card()
        if uid:
            success = mockAddCard(uid)
            if success:
                 showResult("Dodaj kartę:", "Karta", str(uid), "dodana!")
            else:
                 showResult("Błąd!", "Karta została", "już wcześniej", "dodana.")
            
    elif current_state == STATE_REMOVE_LIST_WAIT:
        global cards_list, list_selected_index, list_scroll_offset
        cards = mockGetCards()
        cards_list = cards

        list_selected_index = 0
        list_scroll_offset = 0
        current_state = STATE_REMOVE_LIST
        setupButtonsForState(STATE_REMOVE_LIST)
        needs_redraw = True
        
    elif current_state == STATE_RESULT:
        global result_timestamp
        if time.time() - result_timestamp > 3.0:
            actionBackToMenu()

def drawScreen():
    if current_state == STATE_MENU:
        img = screens.getCardsMenuScreen(menu_selected_option)
        display.show(img)
        
    elif current_state == STATE_ADD_WAIT:
        img = screens.getAddCardWaitingScreen()
        display.show(img)
        
    elif current_state == STATE_REMOVE_LIST_WAIT:
        img = screens.getStatusScreen("Pobieranie...", "Proszę czekać")
        display.show(img)
        
    elif current_state == STATE_REMOVE_LIST:
        img = screens.getRemoveCardListScreen(cards_list, list_selected_index, list_scroll_offset)
        display.show(img)
        
    elif current_state == STATE_CONFIRM:
        img = screens.getConfirmRemoveCardScreen(card_to_remove)
        display.show(img)
        
    elif current_state == STATE_RESULT:
        img = screens.getStatusScreen(
            result_message.get("title", ""),
            result_message.get("line1", ""),
            result_message.get("line2", ""),
            result_message.get("line3", "")
        )
        display.show(img)

# Akcje Przycisków

def actionExit():
    global should_exit
    should_exit = True

def actionBackToMenu():
    global current_state, needs_redraw
    current_state = STATE_MENU
    setupButtonsForState(STATE_MENU)
    needs_redraw = True

def actionBackToList():
    global current_state, needs_redraw
    current_state = STATE_REMOVE_LIST
    setupButtonsForState(STATE_REMOVE_LIST)
    needs_redraw = True

def actionMenuChange(delta):
    global menu_selected_option, needs_redraw
    prev = menu_selected_option
    menu_selected_option = (menu_selected_option + delta) % 2
    if prev != menu_selected_option:
        needs_redraw = True

def actionMenuConfirm():
    global current_state, needs_redraw
    if menu_selected_option == 1:
        current_state = STATE_ADD_WAIT
        setupButtonsForState(STATE_ADD_WAIT)
    else:
        current_state = STATE_REMOVE_LIST_WAIT
        
    needs_redraw = True

def actionListScroll(delta):
    global list_selected_index, list_scroll_offset, needs_redraw
    if not cards_list:
        return
        
    prev = list_selected_index
    new_index = list_selected_index + delta
    
    if 0 <= new_index < len(cards_list):
        list_selected_index = new_index
        
        if list_selected_index >= list_scroll_offset + 3:
            list_scroll_offset += 1
        elif list_selected_index < list_scroll_offset:
            list_scroll_offset -= 1
            
        needs_redraw = True

def actionListSelect():
    global current_state, needs_redraw, card_to_remove
    if not cards_list:
        return
    
    card_to_remove = cards_list[list_selected_index]
    current_state = STATE_CONFIRM
    setupButtonsForState(STATE_CONFIRM)
    needs_redraw = True

def actionConfirmDelete():
    global card_to_remove
    success = mockDeleteCard(card_to_remove)
    showResult("Usuń kartę:", "Karta", str(card_to_remove), "usunięta!" if success else "Błąd!")

def showResult(title, l1, l2, l3):
    global current_state, needs_redraw, result_message, result_timestamp
    result_message = {"title": title, "line1": l1, "line2": l2, "line3": l3}
    result_timestamp = time.time()
    current_state = STATE_RESULT
    setupButtonsForState(STATE_RESULT)
    needs_redraw = True

if __name__ == "__main__":
    print("Uruchamianie Card Manager (Standalone Test)...")
    menuMode()