# from https://stackoverflow.com/questions/53249801/python-aws-iot-sdk-subscription

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import argparse
import json

import datetime

host = "am6287j7b6ceo-ats.iot.eu-west-2.amazonaws.com"
rootCAPath = "root-CA.crt"
certificatePath = "TestingPlatform.cert.pem"
privateKeyPath = "TestingPlatform.private.key"
port = 8883
clientId = "sdk-python"
topic = "forces_sensor"
message_to_print="hello world from Python!"

def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, port)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe("topic_1", 1, customCallback)

# Publish to the same topic in a loop forever
loopCount = 0
while True:
    time_now = str(datetime.datetime.now())

    message = {}
    message["cid"] = clientId
    message['message'] = message_to_print
    message['stamp'] = time_now + " " + str(loopCount)
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish(topic, messageJson, 1)
    loopCount += 1
    time.sleep(0.25)