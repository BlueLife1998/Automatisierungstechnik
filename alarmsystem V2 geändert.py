# alarmsystem.py


# serverAddress, below is the pi's host name. But, since the Mosquitto broker and
# this program (which acts as the subscriber) are on the same Raspberry Pi
# it is recommended to simply use "localhost" as the server name.

serverAddress = "localhost"
username      = "user01"
password      = "MXv65bWrGGH4BKY2"


###############################################################################

import time
import paho.mqtt.client as mqtt     #Lib of 
import RPi.GPIO as GPIO



clientName = "alarmActor"           #Client name can be changed here

mqttClient = mqtt.Client(clientName)
# Flag to indicate subscribe confirmation hasn't been printed yet.
didPrintSubscribeMessage = False



#---------------------------Variables
alarmActive = True      #Variable that states if alarm system is activ or inactive, preset alarm status active
alarmReset  = True      #Varible that states if alarm is resetted, after being tripped


#---------------------------GPIO-Pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)       #Broadcom numbers, don't change to BOARD

buzzer   =  4       #GPIO 4 for Buzzer
buttonS1 = 23       #GPIO 23 for Button S1
buttonS2 = 24       #GPIO 24 for Button S2



#Set the GPIO pins for the buttons as input, for the buzzer as output
GPIO.setup(buttonS1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(buttonS2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(buzzer,GPIO.OUT)




####################----------Functions-----------###########################



def connectionStatus(client, userdata, flags, rc):    #Subscribe to topics and give out that script is successfully subscriped
    global didPrintSubscribeMessage
    if not didPrintSubscribeMessage:
        didPrintSubscribeMessage = True
        print("subscribing")
        mqttClient.subscribe("alarmactivation")        #topic for messages to set the alarmsystem on or off
        mqttClient.subscribe("alarmistripped")         #topic to send message to trip the alarm
        mqttClient.subscribe("m5connected")            #topic in which M5 sticks message when they were connected
        print("subscribed")

    
    #Check the preset alarm status and message it to all clients
    if alarmActive == True:
        mqttClient.publish("alarmactivation", "alarmActivate")
    else:
        mqttClient.publish("alarmactivation", "alarmDeactivate")




def messageDecoder(client, userdata, msg):    
    message = msg.payload.decode(encoding='UTF-8')
    topic   = msg.topic     #get topic of the send message
    global alarmActive      #set alarmActive as global, so other functions can change and use it
    global alarmReset       #set alarmReset as global, so other functions can change and use it


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


#------------------------Functions Buttons---------------------

def buttonS1_pressed(channel):   #Function button S1
    global alarmActive

    #Activate alarm via button
    if alarmActive == False:    
        print("Button S1 was pushed, alarm armed!")
        mqttClient.publish("alarmactivation", "alarmActivate")  #Publish message to tell all clients alarm is active
        alarmActive = True   #Covering the case message was not send
    #Deactivate alarm via button
    elif alarmActive == True:
        print("Button S1 was pushed, alarm disarmed!")
        mqttClient.publish("alarmactivation", "alarmDeactivate") #Publish message to tell all clients alarm is inactive
        alarmActive = False  #Covering the case message was not send
        



def buttonS2_pressed(channel):   #Function button S2
    global alarmReset

    if alarmReset == False:
        alarmReset = True       #Reset the tripped alarm
        print("Button S2 was pushed, alarm was resettet!")
        


##############################################################################



GPIO.add_event_detect(buttonS1,GPIO.RISING,callback=buttonS1_pressed)
GPIO.add_event_detect(buttonS2,GPIO.RISING,callback=buttonS2_pressed)

# Set up calling functions to mqttClient
mqttClient.on_connect = connectionStatus
mqttClient.on_message = messageDecoder

# Connect to the MQTT server & loop forever.
# CTRL-C will stop the program from running.
print("server address is:", serverAddress)
mqttClient.username_pw_set(username, password)
mqttClient.connect(serverAddress)
mqttClient.loop_forever()
