import sys
import Adafruit_DHT
import mysql.connector
from gpiozero import LED
from time import sleep
import boto3
import botocore
import datetime as datetime
import paho.mqtt.client as mqtt
from decimal import *

pin = 4
ledalert = LED(18)


try:
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('iotdata')
    deviceid = 'deviceid_HC'
    print("Successfully connected to database")
    #maybe mqtt here idk
    #have the on message turn the light on or off
    #get mqtt messages from web interface
    ledalert.on()
    print("Successfully connected to broker")
    update = True
    while update:
        try:
            humidity, temperature = Adafruit_DHT.read_retry(11, pin)    #read tmp and humidity and store into variables
            print('Temp: {:.1f} C'.format(temperature)) #print temp
            print('Humidity: {:.1f}'.format(humidity))  #print humidity
            datetimeid = datetime.datetime.now()
            response = table.put_item(
                Item={
                    'deviceid': deviceid,
                    'datetimeid': str(datetimeid),
                    'temperature': Decimal(temperature),
                    'humidity': Decimal(humidity)
                }
            )
            print('Stored data into dynamodb')
            sleep(5)
        except KeyboardInterrupt:
            update = False
        except:
            print("Error while inserting data...")
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
except:
    print(sys.exc_info()[0])
    print(sys.exc_info()[1])