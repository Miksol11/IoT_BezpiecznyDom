import standby
import login
import menu
import time
import measurements
import cardManager

states = {
    "standby": standby.standbyMode,
    "login": login.loginMode,
    "menu": menu.menuMode,
    "standbyConfirm": standby.standbyConfirmMode,
    "karty": cardManager.menuMode
}

def main():
    measurements.start_background_loop()

    state = "standby"
    while True:
        try:
           state = states[state]()
        except Exception as e:
            print(f"Error in state {state}: {e}")
            time.sleep(1)


if __name__ == "__main__":
    main()