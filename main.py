import standby
import login
import menu
import time
import measurements

states = {
    "standby": standby.standbyMode,
    "login": login.loginMode,
    "menu": menu.menuMode,
    "standbyConfirm": standby.standbyConfirmMode
}

def main():
    state = "standby"
    while True:
        # state = states[state]()
        # time.sleep(0.05)
        measurements.sendMeasurements()
        time.sleep(2)
        print("wysłano pomiary")

if __name__ == "__main__":
    main()