# alarmsystem.py
#Alarmsystem mittles IMU des M5stick
#Gruppe 22



# serverAddress, below is the pi's host name. But, since the Mosquitto broker and
# this program (which acts as the subscriber) are on the same Raspberry Pi
# it is recommended to simply use "localhost" as the server name.

serverAddress = "localhost"
username      = "user01"            #usernames and passwords are stored in the passwd file of mosquitto
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

buzzer   =  4       #GPIO 4 for buzzer
buttonS1 = 23       #GPIO 23 for button S1
buttonS2 = 24       #GPIO 24 for button S2



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


    if message == "alarmActivate":  #If message is "alarmActivate" the alarm gets activated
        alarmActive = True
        print("--- Alarm armed !!! ---")
    elif message == "alarmDeactivate":  #If message is "alarmActivate" the alarm gets deactivated
        alarmActive = False
        print("--- Alarm disarmed !!! ---")

        
    elif message == "alarmTripped":     
        if alarmActive == True:                 #Check if alarm is activated, before it goes on
            alarmReset = False                  #Set alarm to non-resetted
            print("--- Alarm tripped !!! ---")
            buzzeralarm()                       #call function Buzzeralarm

            
    #If any message was sent in "m5connected" the message is shown in the terminal. 
    #It shows which m5stick was connected. Example "m5stick Kitchen was connected"
    elif topic == 'm5connected':  
        print(message, "was connected")




def buzzeralarm():

    while alarmReset == False:         #Buzzer makes noise until S2 was pressed
        #Turn buzzer on for 1 second
        GPIO.output(buzzer,GPIO.HIGH)
        time.sleep(1)
        
        #Turn buzzer off for a half second
        GPIO.output(buzzer,GPIO.LOW)   
        time.sleep(0.5)
        


#------------------------Functions Buttons---------------------

def buttonS1_pressed(channel):   #Button S1 is able to activate and deactivate the alarm
    global alarmActive

    #Activate alarm via button
    if alarmActive == False:    
        print("Button S1 was pushed, alarm armed!")
        mqttClient.publish("alarmactivation", "alarmActivate")  #Publish message to tell all clients alarm is active
        alarmActive = True   #Covering the case message was not send, alarm will still be abled in the script
    #Deactivate alarm via button
    elif alarmActive == True:
        print("Button S1 was pushed, alarm disarmed!")
        mqttClient.publish("alarmactivation", "alarmDeactivate") #Publish message to tell all clients alarm is inactive
        alarmActive = False  #Covering the case message was not send, alarm will still be disabled in the script
        



def buttonS2_pressed(channel):   #Button S2 is able to reset the alarm after it was tipped
    global alarmReset

    if alarmReset == False:
        alarmReset = True       #Reset the tripped alarm
        print("Button S2 was pushed, alarm was resettet!")
        


##############################################################################



GPIO.add_event_detect(buttonS1,GPIO.RISING,callback=buttonS1_pressed)   #check if S1 was pressed
GPIO.add_event_detect(buttonS2,GPIO.RISING,callback=buttonS2_pressed)   #check if S2 was pressed

# Set up calling functions to mqttClient
mqttClient.on_connect = connectionStatus
mqttClient.on_message = messageDecoder

# Connect to the MQTT server & loop forever.
# CTRL-C will stop the program from running.
print("server address is:", serverAddress)
mqttClient.username_pw_set(username, password)
mqttClient.connect(serverAddress)
mqttClient.loop_forever()
