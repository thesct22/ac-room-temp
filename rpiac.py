# RPi
import time
import paho.mqtt.client as mqtt
import sys
import csv

global ab
def on_connect(client, userdata, flags, rc):
    if rc==0:
       print("Connected with result code " + str(rc))
       print("connected OK")
       client.subscribe("/esp8266/roomtemp")
    else:
        print("Bad connection Returned code=",rc)
# The callback for when a PUBLISH message is received from the server. 
def on_message(client, userdata, msg): 
    #print(msg.topic+" "+str( msg.payload)) 
   # Check if this is a message for the Pi LED. 
    if msg.topic == '/esp8266/roomtemp': 
       # Look at the message data and perform the appropriate action. 
        #print("temperature at 2 is: "+str(msg.payload))
        global ac
        ac=int(msg.payload)
        #print ac
# Create MQTT client and connect to localhost, i.e. the Raspberry Pi running 
# this script and the MQTT server. 
client = mqtt.Client() 
client.on_connect = on_connect 
client.on_message = on_message 

ac=0

# Connect to the MQTT server and process messages in a background thread. 
try:
    client.loop_start()
    print("Connecting to broker")
    client.connect('localhost', 1883, 60)     #connect to broker
    
    with open('datafinal.csv') as csvfile:
		valreader = csv.reader(csvfile, delimiter=',')
		for row in valreader:
			settime=int(row[0])
			setval=int(row[1])
			setvalto=int(row[2])
		print (settime)
		print (setval)
		print (setvalto)
    flag=True
    client.publish("/esp8266/acval", str(setval),qos=1, retain=False)
    while 1:
		global ac
		print (ac)
		if flag and ac==setval:
			time.sleep(settime)
			client.publish("/esp8266/acval", str(setvalto),qos=1, retain=False)
			flag=False
			print('sent')
		if not flag and ac>setvalto+1:
			flag=True
			client.publish("/esp8266/acval", str(setval),qos=1, retain=False)
			print('sent1')
		time.sleep(2)
    
    print("in Main Loop")
except KeyboardInterrupt:
    client.loop_stop()    #Stop loop 
    client.disconnect() # disconnect
