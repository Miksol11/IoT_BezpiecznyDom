from paho.mqtt.client import Client
import time
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


def _call(req_topic, res_topic, payload, timeout_s):
    response = {"value": None}

    def on_connect(client, userdata, flags, rc):
        client.subscribe(res_topic, qos=1)

    def on_message(client, userdata, msg):
        response["value"] = msg.payload.decode("utf-8")
        client.disconnect()

    client = Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_HOST, BROKER_PORT, 60)
    client.loop_start()

    time.sleep(0.05)
    client.publish(req_topic, payload, qos=1)

    deadline = time.time() + timeout_s
    while time.time() < deadline and response["value"] is None:
        time.sleep(0.01)

    client.loop_stop()
    client.disconnect()

    return response["value"]


def add_card(card_id):
    res = _call(REQ_ADD_TOPIC, RES_ADD_TOPIC, (card_id or "").strip())
    return res == "true"


def delete_card(card_id):
    res = _call(REQ_DEL_TOPIC, RES_DEL_TOPIC, (card_id or "").strip())
    return res == "true"


def card_exists(card_id):
    res = _call(REQ_GET_TOPIC, RES_GET_TOPIC, (card_id or "").strip())
    return res == "true"


def list_cards():
    res = _call(REQ_ALL_TOPIC, RES_ALL_TOPIC, "")
    if not res:
        return []
    return json.loads(res)
