import argparse
import random
import RPi.GPIO as GPIO
import time

def main(k):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(k, GPIO.OUT)
    try:
        while True:
            GPIO.output(k, GPIO.HIGH)
            time.sleep(random.random()*0.4)
            GPIO.output(k, GPIO.LOW)
            time.sleep(random.random()*0.4)
    except KeyboardInterrupt:
        GPIO.cleanup()

parser = argparse.ArgumentParser()
parser.add_argument('k', type=int, help='GPIO number')
args = parser.parse_args()
main(args.k)
