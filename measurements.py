#!/usr/bin/env python3

from config import *
import board
import busio
import adafruit_bme280.advanced as adafruit_bme280
import time
import os

bme280 = None

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