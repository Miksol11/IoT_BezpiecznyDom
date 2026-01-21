import standby
import login
import menu
import time

states = {
    "standby": standby.standbyMode,
    "login": login.loginMode,
    "menu": menu.menuMode,
    "standbyConfirm": standby.standbyConfirmMode
}

def main():
    state = "standby"
    while True:
        state = states[state]()
        time.sleep(0.05)

if __name__ == "__main__":
    main()