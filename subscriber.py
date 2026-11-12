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
from machine import Pin, PWM
import time
import umqtt.robust as umqtt

# WiFi details
ssid = 'Michael-hotspot'
password = '36042067'

# MQTT details
HOSTNAME = '10.215.254.246'  # Raspberry Pi 5 IP
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

# Temperature threshold
TEMP_THRESHOLD = 25

# LED setup
led = Pin(15, Pin.OUT)
led_pwm = PWM(led)
led_pwm.freq(5000)

# Turn LED off initially
led_pwm.duty_u16(0)


# Function to handle received MQTT messages
def on_message(topic, message):

    print("Message received on:", topic)

    try:
        temperature = float(message.decode())

        print("Temperature received:", temperature, "C")

        if temperature >= TEMP_THRESHOLD:

            led_pwm.duty_u16(65535)
            print("Temperature >= 25 C - LED ON")

        else:

            led_pwm.duty_u16(0)
            print("Temperature < 25 C - LED OFF")

    except ValueError:
        print("Invalid temperature received:", message)


# MQTT client setup
mqtt = umqtt.MQTTClient(
    client_id=b'pico2-subscriber',
    server=HOSTNAME.encode(),
    port=PORT,
    keepalive=60
)

# Set callback function
mqtt.set_callback(on_message)

# Connect to MQTT broker
print("Connecting to MQTT broker...")
mqtt.connect()

print("Connected to MQTT broker")

# Subscribe to temperature topic
mqtt.subscribe(TOPIC)

print("Subscribed to:", TOPIC)
print("Waiting for temperature readings...")


# Continuously listen for MQTT messages
while True:

    try:
        mqtt.check_msg()
        time.sleep(0.1)

    except OSError as e:
        print("MQTT connection error:", e)
        print("Attempting to reconnect...")

        time.sleep(2)
        mqtt.reconnect()
        mqtt.subscribe(TOPIC)