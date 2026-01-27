#!/usr/bin/env python3


try:
    from config import *
    import board
    import busio
    import adafruit_bme280.advanced as adafruit_bme280
    HARDWARE_AVAILABLE = True
except (ImportError, ModuleNotFoundError, NotImplementedError):
    HARDWARE_AVAILABLE = False
    # Fallback mocks if needed
    board = None
    busio = None
    adafruit_bme280 = None

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
    if not HARDWARE_AVAILABLE:
        return

    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)

        bme280.sea_level_pressure = 1015.5
        bme280.standby_period = adafruit_bme280.STANDBY_TC_500
        bme280.iir_filter = adafruit_bme280.IIR_FILTER_X16
        bme280.overscan_pressure = adafruit_bme280.OVERSCAN_X16
        bme280.overscan_humidity = adafruit_bme280.OVERSCAN_X1
        bme280.overscan_temperature = adafruit_bme280.OVERSCAN_X2
    except Exception as e:
        print(f"Błąd inicjalizacji BME280: {e}")


def ensureBME():
    global bme280
    if bme280 is None:
        setup()

def getTemperature():
    if not HARDWARE_AVAILABLE:
        import random
        return 20.0 + random.uniform(-2, 2)
    ensureBME()
    return bme280.temperature

def getPressure():
    if not HARDWARE_AVAILABLE:
        import random
        return 1013.25 + random.uniform(-10, 10)
    ensureBME()
    return bme280.pressure

def getHumidity():
    if not HARDWARE_AVAILABLE:
        import random
        return 50.0 + random.uniform(-5, 5)
    ensureBME()
    return bme280.humidity

def getAltitude():
    if not HARDWARE_AVAILABLE:
        return 100.0
    ensureBME()
    return bme280.altitude

# helper: init mqtt client lazily (domyślny broker 10.108.33.106)
def _ensure_mqtt():
    global _mqtt_client
    if mqtt is None:
        # Jeśli nie ma biblioteki paho-mqtt, zwracamy None (tryb mock bez MQTT)
        return None

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
        print(f"Błąd połączenia MQTT (tryb offline?): {e}")
        return None

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

    if HARDWARE_AVAILABLE:
        ensureBME()
        if bme280 is None:
            return False

    try:
        temperature = getTemperature()
        pressure = getPressure()
        humidity = getHumidity()
        altitude = getAltitude()
    except Exception as e:
        with _mqtt_lock:
            _last_send_time = 0.0
        print(f"Błąd odczytu sensorów: {e}")
        return False

    payload = {
        "temperature": float(round(temperature, 2)),
        "pressure": float(round(pressure, 2)),
        "humidity": float(round(humidity, 2)),
        "altitude": float(round(altitude, 2)),
        "ts": int(time.time())
    }

    if not HARDWARE_AVAILABLE:
        print(f"[MOCK] Pomiary: {payload}")

    topic = globals().get('MQTT_TOPIC', 'sensors/bme280')

    try:
        client = _ensure_mqtt()
        if client:
            client.publish(topic, json.dumps(payload), qos=1)
            return True
        else:
            return True
    except Exception:
        with _mqtt_lock:
            _last_send_time = 0.0
        return False


# Logika wątku w tle

_background_thread = None
_stop_background = threading.Event()

def _background_loop():
    while not _stop_background.is_set():
        try:
            sendMeasurements()
        except Exception as e:
            print(f"Błąd w wątku pomiarowym: {e}")
        
        time.sleep(1)

def start_background_loop():
    global _background_thread
    if _background_thread is None or not _background_thread.is_alive():
        _stop_background.clear()
        _background_thread = threading.Thread(target=_background_loop, daemon=True)
        _background_thread.start()
        print("Uruchomiono wątek pomiarów w tle.")

def stop_background_loop():
    _stop_background.set()
    global _background_thread
    if _background_thread:
        _background_thread.join(timeout=2.0)
        _background_thread = None
        print("Zatrzymano wątek pomiarów.")