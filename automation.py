#! /usr/bin/env python3

import os
from time import sleep
import datetime
from datetime import timedelta
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import RPi.GPIO as GPIO
from firebase import firebase
import csv
import Adafruit_DHT
import sys


'''Guarda les dades en un csv i penja per la web'''
def store_upload_data(Tm,Wm,Hm,Mm,date):
    with open('data_log.csv','a') as datalog:
        data_writer = csv.writer(datalog)
        data_writer.writerow([str(date),str(Wm),str(Mm),str(Tm),str(Hm)])
    datalog.close
    
    database = firebase.FirebaseApplication('https://pcare-c5ee1.firebaseio.com/',None)

    database.put('/Palau','Temperatura',Tm)
    database.put('/Palau','HumitatAire',Hm)
    database.put('/Palau','Humitat',round(Mm,1)) #round to 1 decimal for webpage)
    database.put('/Palau','Aigua',Wm)
    database.put('/Palau','CheckTime',date)

'''Manual. Mira si REGAR i REPARAR a la database té un 1 o un 0. Si té un 1 rega o para l'execució i canvia el número a 0 per indicar que ha regat'''
def click_regar_reparar():
    database = firebase.FirebaseApplication('https://pcare-c5ee1.firebaseio.com/',None)
    R = database.get('/Palau','Regar')
    RP = database.get('/Palau','Reparar')
    if R == 1:
        # energize relay to close valve circuit and let water flow
        GPIO.setup(17,GPIO.OUT)
        GPIO.output(17,GPIO.LOW)
        sleep(90)
        GPIO.output(17,GPIO.HIGH)
        R = 0
        database.put('/Palau','Regar',R)
    if RP == 1:
        RP = 0
        database.put('/Palau','Reparar',RP)
        GPIO.cleanup()
        sys.exit('Execution stopped for reparation')
        
    #next click check time (mínim ha de passar 1 hora per poder forçar el regat)
    check_clickregar = datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(hours=1)
    #print('Next regar check: ',check_clickregar)
    return check_clickregar


'''Mesura temperatura, humitats i nivell d'aigua i els retorna'''
def measure():
# WATER LEVEL
    #water_level = chan1.value
    #print('Water level: ',water_level)
    #if water_level < 100:
        #print('WATER LEVEL LOW!!!')
        
# MOISTURE

    #moisture_thresh = 0.53 #0.528 equival a 45000 (moist soil)
    moisture = round((chan0.value - 0)/(11500 - 0),2)
    '''
    if moisture < moisture_thresh:
        # energize relay to close valve circuit
        GPIO.setup(17,GPIO.OUT)
        GPIO.output(17,GPIO.LOW)
        sleep(90)
        GPIO.output(17,GPIO.HIGH)
        moistureAfter = round(1-(chan0.value - 32384)/(56256 - 32384),2)
    '''
# TEMPERATURE AND HUMIDITY
    humidity,temperature = Adafruit_DHT.read_retry(DHT_SENSOR,DHT_PIN)
    humidity = round(humidity,1)
    temperature= round(temperature,1)
    #print(moisture,temperature,humidity)
    return moisture,humidity,temperature

#Sistema autònom. Recull dades i rega si cal, penja i emmagatzema dades, calcula proper check time
def auto():
    
    mVal,hVal,tVal = measure()
    # save check time 
    check_time = datetime.datetime.now().replace(microsecond=0)
    #print('Check time: ',check_time)

    store_upload_data(tVal,7,hVal,mVal,check_time)
    
    # schedule next check time (si hi ha hagut algun error en la càrrega no es programa un temps de proper check, així no tornarà a activar-se auto)'
    check_next = check_time + datetime.timedelta(hours=6)
    #print('Next check time scheduled: ',check_next)

    return check_next


try:
    '''SETTING UP VALVE GPIO 17'''
    GPIO.setmode(GPIO.BCM)

    '''SETTING UP ADC FOR MOISTURE SENSOR '''
    # create SPI bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    # create cs (chip select)
    cs = digitalio.DigitalInOut(board.D22) # GPIO 22
    # create MCP object
    mcp = MCP.MCP3008(spi, cs)
    # create analog input channel on pin 0 of MCP (moisture sensor)
    chan0 = AnalogIn(mcp, MCP.P0)
    #chan1 = AnalogIn(mcp,MCP.P1)

    '''SETTING UP DHT22 GPIO 14'''
    DHT_SENSOR = Adafruit_DHT.DHT22
    DHT_PIN = 14

    # first check
    check_next = auto()
    check_clickregar = click_regar_reparar()
    while True:
        # next check when scheduled time arrives
        if datetime.datetime.now().replace(microsecond=0) == check_next:
            check_next = auto()
        if datetime.datetime.now().replace(microsecond=0) == check_clickregar:
            check_clickregar = click_regar_reparar()
                

except Exception as ex:
    GPIO.cleanup()
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    sys.stdout.write(message) #avisa al terminal
    # avisa de l'error a la base de dades
    database = firebase.FirebaseApplication('https://pcare-c5ee1.firebaseio.com/',None)
    database.put('/Palau','SystemError',1)
    database.put('/Palau','ErrorMessage',message)

#except KeyboardInterrupt:
    #GPIO.cleanup()
    #print('Run cancelled')
