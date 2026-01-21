#!/usr/bin/env python3

from config import *
import board
import busio
import adafruit_bme280.advanced as adafruit_bme280
import time
import os
import threading
import json
# dodane importy dla MQTT
try:
    import paho.mqtt.client as mqtt
except ModuleNotFoundError:
    mqtt = None

bme280 = None
_mqtt_client = None
_mqtt_lock = threading.Lock()
_last_send_time = 0.0

def setup():
    global bme280
    i2c = busio.I2C(board.SCL, board.SDA)
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)

    bme280.sea_level_pressure = 1015.5
    bme280.standby_period = adafruit_bme280.STANDBY_TC_500
    bme280.iir_filter = adafruit_bme280.IIR_FILTER_X16
    bme280.overscan_pressure = adafruit_bme280.OVERSCAN_X16
    bme280.overscan_humidity = adafruit_bme280.OVERSCAN_X1
    bme280.overscan_temperature = adafruit_bme280.OVERSCAN_X2

def ensureBME():
    global bme280
    if bme280 is None:
        setup()

def getTemperature():
    ensureBME()
    return bme280.temperature

def getPressure():
    ensureBME()
    return bme280.pressure

def getHumidity():
    ensureBME()
    return bme280.humidity

def getAltitude():
    ensureBME()
    return bme280.altitude

# helper: init mqtt client lazily (domyślny broker 10.108.33.106)
def _ensure_mqtt():
    global _mqtt_client
    if mqtt is None:
        raise RuntimeError("Brak biblioteki paho-mqtt. Zainstaluj: sudo pip3 install paho-mqtt")

    if _mqtt_client is not None:
        return _mqtt_client

    broker = globals().get('MQTT_BROKER', '10.108.33.106')
    port = globals().get('MQTT_PORT', 1883)
    user = globals().get('MQTT_USER', "mati")
    password = globals().get('MQTT_PASSWORD', "siems")
    client_id = globals().get('MQTT_CLIENT_ID', 'bme280-client')

    client = mqtt.Client(client_id=client_id)
    if user is not None and password is not None:
        client.username_pw_set(user, password)

    try:
        client.connect(broker, port, keepalive=60)
        client.loop_start()
    except Exception as e:
        raise RuntimeError(f"Nie można połączyć z brokerem MQTT {broker}:{port}: {e}")

    _mqtt_client = client
    return _mqtt_client
# ...existing code...

def sendMeasurements():
    global _last_send_time

    now = time.time()
    with _mqtt_lock:
        if (now - _last_send_time) < 1.0:
            return False  # zbyt często, pominięte
        _last_send_time = now

    ensureBME()
    try:
        temperature = getTemperature()
        pressure = getPressure()
        humidity = getHumidity()
        altitude = getAltitude()
    except Exception as e:
        with _mqtt_lock:
            _last_send_time = 0.0
        raise

    payload = {
        "temperature": float(round(temperature, 2)),
        "pressure": float(round(pressure, 2)),
        "humidity": float(round(humidity, 2)),
        "altitude": float(round(altitude, 2)),
        "ts": int(time.time())
    }

    topic = globals().get('MQTT_TOPIC', 'sensors/bme280')

    try:
        client = _ensure_mqtt()
        client.publish(topic, json.dumps(payload), qos=1)
        return True
    except Exception:
        with _mqtt_lock:
            _last_send_time = 0.0
        raise