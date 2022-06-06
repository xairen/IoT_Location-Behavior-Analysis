#AWS IoT Project Python code
#Author : Abhinav Srinivasan

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import serial
import argparse
import json
import uuid
import socket
import time
from geopy.geocoders import Nominatim
from pprint import pprint

app = Nominatim(user_agent="tutorial")

s = socket.socket()
print ("Socket successfully created")

port = 9090
# @brief: Send a read/write command to the Arduino
# @par ser: The serial port instance
# @par command: The name of the read/write command
# @ret None
def send_command(ser, command):
	ser.write(command.encode())
	
s.bind(('', port))
print ("socket binded to %s" %(port))
	
	
def read_uart(ser):	
	value = ser.readline().decode('utf-8')	# Read and print the received serial transmission
	print(value)
	return value
	
def check_ack(ser, ack_string):	
	while(1):
		recd_ack = ser.readline().decode('utf-8')	# Read and print the received serial transmission
		print(recd_ack)
		
		if (recd_ack == ack_string + "\r\n"):	# Check if the recieved message is an acknowledgement message
			print(recd_ack+" received")
			break


def serial_port():
	ser = serial.Serial(
	    port='/dev/ttyS1',\
	    baudrate=9600,\
	    parity=serial.PARITY_NONE,\
	    stopbits=serial.STOPBITS_ONE,\
	    bytesize=serial.EIGHTBITS,\
	    timeout=None)
	print("Connected to: " + ser.portstr)
	return ser
	
def get_location_by_address(address):
    time.sleep(1)
    try:
        return app.geocode(address).raw
    except:
        return get_location_by_address(address)
        
def get_address_by_location(latitude, longitude, language="en"):
    # build coordinates string to pass to reverse() function
    coordinates = f"{latitude}, {longitude}"
    # sleep for a second to respect Usage Policy
    time.sleep(1)
    try:
        return app.reverse(coordinates, language=language).raw
    except:
        return get_address_by_location(latitude, longitude)
        
        
# Configuration details and certificate paths
clientId = "Omega2"
endpoint = "agg31r4m0arla-ats.iot.us-east-1.amazonaws.com" #AmazonAWS
rootCAFilePath = "Amazon-CA.pem" #.pem file 
privateKeyFilePath = "a1b7b422f4-private.pem.key" #.pem.key file
certFilePath = "a1b7b422f4-certificate.pem.crt" #pem.crt file

print("Connecting to: " + endpoint + " ClientID: " + clientId)
# For certificate based connection
# myMQTTClient = AWSIoTMQTTClient("myClientID")
myMQTTClient = AWSIoTMQTTClient(clientId)
# For Websocket connection
# myMQTTClient = AWSIoTMQTTClient("myClientID", useWebsocket=True)

print("Connected!")
print("Subscribing to topic: Omega_AAB0/+/details")
print("Subscribed with QoS: 1")
# Configurations: - 
# For TLS mutual authentication
# myMQTTClient.configureEndpoint("YOUR.ENDPOINT", 8883)
myMQTTClient.configureEndpoint(endpoint, 8883)
# For Websocket
# myMQTTClient.configureEndpoint("YOUR.ENDPOINT", 443)
# For TLS mutual authentication with TLS ALPN extension
# myMQTTClient.configureEndpoint("YOUR.ENDPOINT", 443)

# myMQTTClient.configureCredentials("YOUR/ROOT/CA/PATH", "PRIVATE/KEY/PATH", "CERTIFICATE/PATH")
myMQTTClient.configureCredentials(rootCAFilePath, privateKeyFilePath, certFilePath)
# For Websocket, we only need to configure the root CA
# myMQTTClient.configureCredentials("YOUR/ROOT/CA/PATH")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

QoS = 1

# payload = "myPayload"
# payload = json.dumps(payload)
def customCallback(client, userdata, message):
	print(str(message.topic) + ": " + str(message.payload))

def customOnMessage(client, userdata, message):
	if (message.topic) == "Omega_AAB0/device/details":
		print(str(message.topic) + ": " + str(message.payload))
		print("Recieved device configuration:" + str(message.payload))
	
connect_ACK = myMQTTClient.connect()
topic = "Omega_AAB0/device/details"
myMQTTClient.subscribe(topic, 1, customOnMessage)

address = input("Enter address here :") #change address over here ex: Rochester, Brooks Ave, New York
#address = "Rochester, Monroe, New York"
#address = "Rochester, Brooks Ave, New York"
#address = "Rochester, Henrietta, New York"
location = get_location_by_address(address)
latitude = location["lat"]
longitude = location["lon"]
# Configure the Serial port of the Omega board
ser = serial_port()
num = 1
t1 = int(time.strftime("%S"))
while True:
	print("Reading rotary sensor(Mobile)")
	send_command(ser, "ANGLE_CHECK")
	angle = int(read_uart(ser))
	print("Angle: " + str(angle))
	if angle > 89 and angle < 100:
		send_command(ser, "ANGLE_90")
		check_ack(ser, "ANGLE_90")
		print(f"{latitude}, {longitude}")
		
		# Store lattitude and longitude; return Location 
			# if(latitude == "43.157285" and longitude == "-77.615214"):
			# 	print("You are in RIT University")
			# 	payload = '{"Location":"RIT"}'

			# elif(latitude == "43.11590925" and longitude == "-77.63463580644128"):
			# 	print("You are at rustic village")
			# 	payload = '{"Location":"Rustic"}'
	
			# elif(latitude == "43.12807995" and longitude == "-77.65757590000001"):
			# 	print("You are at the airport")
			# 	payload = '{"Location":"ROCAirport"}'
			
	elif angle == 0:
		send_command(ser, "ANGLE_180")
		check_ack(ser, "ANGLE_180")
		print("\nThe device is either on charge or not in use")
		payload = '{"Device" : "Charging"}'

	else:
		send_command(ser, "ANGLE_T")
		check_ack(ser, "ANGLE_T")
		print("\nThe device is being used\n")
		time.sleep(2)
		num += 1
		t2 = int(time.strftime("%S"))
		print(str(t2-t1) + "Seconds the device has been used")
		payload = '{"Device" : "In Use"}'


	myMQTTClient.publish(topic,payload, 1)
	
	num += 1
	if (num == 2):
		time.sleep(1)
		break

	

myMQTTClient.unsubscribe(topic)
myMQTTClient.disconnect()
	
	
#define your coordinates if you want to hard code it
#latitude = 43.080123
#longitude = -77.669178
# get the address info
#address = get_address_by_location(latitude, longitude)
# print all returned data
#pprint(address)
