import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ledStatus = False

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button1 to GPIO23
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button2 to GPIO22

GPIO.setup(25, GPIO.OUT)  #LED1 to GPIO24
GPIO.setup(9, GPIO.OUT)  #LED2 to GPIO24

GPIO.output(25, True)
GPIO.output(9, True)

try:
    while True:
         button_state1 = GPIO.input(23)
         button_state2 = GPIO.input(22)
         if button_state1 == False:
             GPIO.output(9, False) #off female
             GPIO.output(25, True)
             print('Male selected')
             time.sleep(0.2)
         elif button_state2 == False: #off male
             GPIO.output(25, False)
             GPIO.output(9, True)
             print('Female selected')
             time.sleep(0.2)
             
except:
    GPIO.cleanup()
