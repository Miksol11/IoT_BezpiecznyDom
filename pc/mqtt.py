from paho.mqtt.client import Client
import db
import json

BROKER_HOST = "192.168.1.10"
BROKER_PORT = 1883

REQ_ADD_TOPIC = "cards/add"
RES_ADD_TOPIC = "cards/add/result"

REQ_DEL_TOPIC = "cards/del"
RES_DEL_TOPIC = "cards/del/result"

REQ_GET_TOPIC = "cards/get"
RES_GET_TOPIC = "cards/get/result"

REQ_ALL_TOPIC = "cards/all"
RES_ALL_TOPIC = "cards/all/result"

def onConnect(client, userdata, flags, rc):
    client.subscribe(REQ_ADD_TOPIC)
    client.subscribe(REQ_DEL_TOPIC)
    client.subscribe(REQ_GET_TOPIC)
    client.subscribe(REQ_ALL_TOPIC)
    print("Connected rc=", rc)

def onMessage(client, userdata, msg):
    print("Received " + msg.topic)
    if msg.topic == REQ_ADD_TOPIC:
        onAddCardMessage(client, userdata, msg)
    elif msg.topic == REQ_DEL_TOPIC:
        onDeleteCardMessage(client, userdata, msg)
    elif msg.topic == REQ_GET_TOPIC:
        onGetCardMessage(client, userdata, msg)
    elif msg.topic == REQ_ALL_TOPIC:
        onAllCardMessage(client, userdata, msg)
    else:
        return  

def onAddCardMessage(client, userdata, msg):
    card_id = msg.payload.decode("utf-8").strip()
    try:
        success = db.addCard(card_id)
    except Exception:
        success = False
    client.publish(RES_ADD_TOPIC, "true" if success else "false")
    print("Sending back", RES_ADD_TOPIC)

def onDeleteCardMessage(client, userdata, msg):
    card_id = msg.payload.decode("utf-8").strip()
    try:
        success = db.deleteCard(card_id)
    except Exception:
        success = False
    client.publish(RES_DEL_TOPIC, "true" if success else "false")
    print("Sending back", RES_DEL_TOPIC)

def onGetCardMessage(client, userdata, msg):
    card_id = msg.payload.decode("utf-8").strip()
    try:
        success = db.cardExists(card_id)
    except Exception:
        success = False
    client.publish(RES_GET_TOPIC, "true" if success else "false")
    print("Sending back", RES_GET_TOPIC)

def onAllCardMessage(client, userdata, msg):
    try:
        cards = db.listCards()
    except Exception:
        cards = []
    client.publish(RES_ALL_TOPIC, json.dumps(cards))
    print("Sending back", RES_ALL_TOPIC)

def main():
    db.ensureDatabaseExists()

    client = Client(client_id="pc")
    client.on_connect = onConnect
    client.on_message = onMessage

    client.connect(BROKER_HOST, BROKER_PORT, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()