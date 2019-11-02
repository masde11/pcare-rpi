#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 10:58:19 2019

@author: arnau
"""

import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import busio
import digitalio
import board
from time import sleep

'''SETTING UP ADC FOR MOISTURE SENSOR '''
# create SPI bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
# create cs (chip select)
cs = digitalio.DigitalInOut(board.D22) # GPIO 22
# create MCP object
mcp = MCP.MCP3008(spi, cs)
# create analog input channel on pin 0 of MCP (moisture sensor)
chan0 = AnalogIn(mcp, MCP.P0)
    
while True:
    print('Value: ',chan0.value)
    moisture = round((chan0.value - 0)/(11500 - 0),2) #valor-min/max-min
    print('Normalised: ',moisture)
    sleep(5)
    
