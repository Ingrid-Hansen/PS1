import RPi.GPIO as GPIO
import time
import thingspeak 
from datetime import date

#Function to pause program for litterbox cleaning
def cleaning():
    if GPIO.input(pause_button)==1:
        print("Cleaning Litterbox")
        time.sleep(300)
        print("Cleaning Complete")



#Setup and variables
GPIO.setmode(GPIO.BCM)
Pir_Pin= 24
GPIO.setup(Pir_Pin, GPIO.IN)
channel_id = 1709723
write_key = "Z6NEWQH4B03MZPXE"
read_key = "LARFASQS65HGBRIP"
channel = thingspeak.Channel(id=channel_id,api_key=write_key)

pause_button = 23

GPIO.setup(pause_button,GPIO.IN)


#Main
try:
    time.sleep(15)
    print("Program Started")
    while True:
        cleaning()
        systemtime= time.localtime()
        time_string=time.strftime("%H:%M:%S",systemtime)
        today = date.today()
        current_date = today.strftime("%d/%m/%Y")
        if GPIO.input(Pir_Pin)==1:
            with open('/home/pi/litterboxlog.txt','a') as log:
                print("Litterbox In Use")
                channel.update({1:1, 2:1})
                data = current_date + '\t' + time_string + '\n'
                log.write(data)
                time.sleep(600) 
                print("Litterbox Free")        
finally:
    GPIO.cleanup()
