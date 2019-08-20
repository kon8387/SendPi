from flask import Flask, render_template, jsonify, request, Response

import sys

import json
import numpy
import datetime
import decimal
import boto3
import botocore
from boto3.dynamodb.conditions import Key, Attr

from decimal import Decimal
import json
import datetime
import numpy

import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer

gevent.monkey.patch_all()

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
	
host = "xxxx.iot.us-east-1.amazonaws.com"
rootCAPath = "rootca.pem"
certificatePath = "certificate.pem.crt"
privateKeyPath = "private.pem.key"
access_key = "xxxx"
secret_access_key = "yyyy"
session_token = "zzzz"


my_rpi = AWSIoTMQTTClient("basicPubSub")
my_rpi.configureEndpoint(host, 8883)
my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
my_rpi.configureMQTTOperationTimeout(5)  # 5 sec
my_rpi.connect()

def mqtt_pub(msg):
    my_rpi.publish("sensor/light", str(msg), 1)

def ledOn():
    #mqtt send msg
    mqtt_pub('on')
    return "LED is turned on"

def ledOff():
    #mqtt send msg
    mqtt_pub('off')
    return "LED is turned off"

class GenericEncoder(json.JSONEncoder):
    def default(self, obj):  
        if isinstance(obj, numpy.generic):
            return numpy.asscalar(obj)
        elif isinstance(obj, Decimal):
            return str(obj) 
        elif isinstance(obj, datetime.datetime):  
            return obj.strftime('%Y-%m-%d %H:%M:%S') 
        elif isinstance(obj, Decimal):
            return float(obj)
        else:  
            return json.JSONEncoder.default(self, obj) 

def data_to_json(data):
    json_data = json.dumps(data,cls=GenericEncoder)
    return json_data


app = Flask(__name__)

@app.route("/api/getdata/<deviceid>", methods=['POST', 'GET'])
def apidata_getdata(deviceid):
    if request.method == 'POST':
        try:
            dynamodb = boto3.resource('dynamodb', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key, aws_session_token=session_token, region_name='us-east-1')
            table = dynamodb.Table('iotdata')
            response = table.query(
                KeyConditionExpression = Key('deviceid').eq(deviceid)
            )
            items_reversed = response['Items'][::-1]
            items = items_reversed[:10]
            data = {'chart_data': data_to_json(items[::-1]), 'title': "IOT Data"}
            return jsonify(data)
        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])

@app.route("/writeLED/<status>")
def writePin(status):

   if status == 'On':
     response = ledOn()
   else:
     response = ledOff()

   return response


@app.route("/")
def mainpage():
    return render_template('index.html')


if __name__ == '__main__':
    try:
        http_server = WSGIServer(('0.0.0.0', 80), app)
        app.debug = True
        http_server.serve_forever()
    except:
        print("Exception")
