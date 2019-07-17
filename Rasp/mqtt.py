import paho.mqtt.client as mqtt
import time
import re
import log
from store_Sensor_Data_to_DB import sensor_Data_Handler

MQTT_SERVER = "localhost"
MQTT_PATH = "Temp"
 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if (rc == 0):
        log.Action("Connected to broker successfully")
    else:
        log.Action("Problems to connect with broker")    
    
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print ("MQTT Data Received...")
    #print ("MQTT Topic: " + msg.topic)  
    #print ("Data: " + msg.payload)
    sensor_Data_Handler(msg.topic, msg.payload)
    
    #print(msg.topic+" "+str(msg.payload.decode("utf-8","ignore")))
    #log.Action(msg.topic + " " + str(msg.payload.decode("utf-8","ignore")))
    # more callbacks, etc
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("pia","pia") 
client.connect(MQTT_SERVER, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

client.loop_start()
    
#def sub(Topic, Payload, ClientId):
    

#def sub(Topic, Payload):
 #   print(str(Topic)+ " " +re.findall("\d+\.\d+", str(Payload)))
    

while True:
    #client.publish("Temp Rx","1")
    time.sleep(10)
    #client.publish("Temp Rx","0")

    