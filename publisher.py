
'''
SUBMISSION INFO

STUDENT             |   NUMBER
---------------------------------
Michael Casey       |   C23343691
Killian O Connell   |   C23412864
Eoin Kenny          |   C23350933
'''

# Imports
from network import WLAN
import time, socket
from machine import Pin, PWM, ADC, Timer
import cryptolib
from time import sleep
import json
import umqtt.robust as umqtt

# WiFi details
ssid = 'Michael-hotspot'
password = '36042067'

# MQTT details
HOSTNAME = '10.215.254.246'  # Raspberry Pi 5 IP address
PORT = 25000
TOPIC = 'temp/pico'

# Connect to WiFi
wifi = WLAN(WLAN.IF_STA)
wifi.active(True)

ssid = 'Michael-hotspot'
password = '36042067'

# Connecting to a network
wifi.connect(ssid, password)

time.sleep(5)

if wifi.status() != 3:
    print('Wifi couldnt connect')
else:
    print('Connected to WiFi')
    print('Pico IP:', wifi.ifconfig()[0])

# Temperature sensor setup
temp_sensor = ADC(4)

# Read temperature
def read_temp():
    value = temp_sensor.read_u16()
    voltage = value * (3.3 / 65535)
    temperature = 27 - (voltage - 0.706) / 0.001721
    return round(temperature, 2)


# MQTT client setup
mqtt = umqtt.MQTTClient(
    client_id=b'publish',
    server=HOSTNAME.encode(),
    port=PORT,
    keepalive=7000
)

# Connect to MQTT broker
print("Connecting to MQTT broker...")
mqtt.connect()
print("Connected to MQTT broker")


# Continuously read and publish temperature
while True:
    temperature = read_temp()
    print("Temperature:", temperature, "C")
    mqtt.publish(TOPIC, str(temperature).encode())
    print("Temperature published to:", TOPIC)
    time.sleep(2)
