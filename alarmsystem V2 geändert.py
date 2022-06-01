# alarmsystem.py
# Written by Luca Schulte, Hochschule Emden-Leer.

# You can control this subscriber program with an app named
# MQTT Dashboard, which you can download for free from the Google Play Store at:
# https://apps.apple.com/us/app/mil-mascaras/id1550345112?platform=iphone
#
# serverAddress, below is your pi's host name. But, since our Mosquitto broker and
# this program (which acts as the subscriber) are on the same Raspberry Pi
# we can simply use "localhost" as the server name.

serverAddress = "localhost"
username      = "user01"
password      = "MXv65bWrGGH4BKY2"


###############################################################################

import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO



clientName = "alarmActor"

mqttClient = mqtt.Client(clientName)
# Flag to indicate subscribe confirmation hasn't been printed yet.
didPrintSubscribeMessage = False

#---------------------------Variablen
alarmActive = True
alarmReset  = True

#---------------------------GPIO-Pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

buzzer   =  4       #GPIO 4 für Buzzer belegt
buttonS1 = 23       #GPIO 23 für Taster S1 belegt
buttonS2 = 24       #GPIO 24 für Taster S2 belegt




GPIO.setup(buttonS1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(buttonS2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(buzzer,GPIO.OUT)




####################----------Funktionen----------###########################



def connectionStatus(client, userdata, flags, rc):
    global didPrintSubscribeMessage
    if not didPrintSubscribeMessage:
        didPrintSubscribeMessage = True
        print("subscribing")
        mqttClient.subscribe("alarmactivation")
        mqttClient.subscribe("alarmistripped")
        mqttClient.subscribe("m5connected")
        print("subscribed")


    if alarmActive == True:
        mqttClient.publish("alarmactivation", "alarmActivate")
    else:
        mqttClient.publish("alarmactivation", "alarmDeactivate")




def messageDecoder(client, userdata, msg):
    message = msg.payload.decode(encoding='UTF-8')
    topic   = msg.topic
    global alarmActive
    global alarmReset


    if message == "alarmActivate":
        alarmActive = True
        print("--- Alarm armed !!! ---")
    elif message == "alarmDeactivate":
        alarmActive = False
        print("--- Alarm disarmed !!! ---")

    elif message == "alarmTripped":
        if alarmActive == True:
            alarmReset = False
            print("--- Alarm tripped !!! ---")
            buzzeralarm()

    elif topic == 'm5connected':
        print(message)




def buzzeralarm():

    while alarmReset == False:
        GPIO.output(buzzer,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(buzzer,GPIO.LOW)
        time.sleep(0.5)
        #GPIO.cleanup()


#------------------------Funktionen der Kurzhubtaster---------------------

def buttonS1_pressed(channel):   #Funktion Taster S1
    global alarmActive

    if alarmActive == False:    #Alarm per Button aktivieren
        print("Button S1 was pushed, alarm armed!")
        mqttClient.publish("alarmactivation", "alarmActivate")
        alarmActive = True
    elif alarmActive == True:
        print("Button S1 was pushed, alarm disarmed!")
        mqttClient.publish("alarmactivation", "alarmDeactivate")
        alarmActive = False
        #GPIO.cleanup()



def buttonS2_pressed(channel):   #Funktion Taster S2
    global alarmReset

    if alarmReset == False:
        alarmReset = True       #Ausgelösten Alarm resetten
        print("Button S2 was pushed, alarm was resettet!")
        #GPIO.cleanup()


##############################################################################



GPIO.add_event_detect(buttonS1,GPIO.RISING,callback=buttonS1_pressed)
GPIO.add_event_detect(buttonS2,GPIO.RISING,callback=buttonS2_pressed)

# Calling Functions für MQTT client einrichten
mqttClient.on_connect = connectionStatus
mqttClient.on_message = messageDecoder

# Mit MQTT Server verbinden und unendliche Schleife starten
# Mit Strg.+C wird das Programm beendet
print("server address is:", serverAddress)
mqttClient.username_pw_set(username, password)
mqttClient.connect(serverAddress)
mqttClient.loop_forever()
