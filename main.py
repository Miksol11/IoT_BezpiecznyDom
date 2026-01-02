import standby

states = {
    "standby": standby.standbyMode
}

def main():
    state = "standby"
    while True:
        state = states[state]()

if __name__ == "__main__":
    main()