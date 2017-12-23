import random
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14,GPIO.OUT)
#GPIO.setup(18,GPIO.OUT)
try:
    while True:
        #print("LED on")
        GPIO.output(14,GPIO.HIGH)
        #GPIO.output(18,GPIO.HIGH)
        time.sleep(random.random()*0.4)
        #print("LED off")
        GPIO.output(14,GPIO.LOW)
        #GPIO.output(18,GPIO.LOW)
        time.sleep(random.random()*0.4)
except KeyboardInterrupt:
    GPIO.cleanup()
