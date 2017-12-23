import argparse
import random
import RPi.GPIO as GPIO
import time


def main(warten):
    pins = list(range(1, 9)) + list(range(9, 17))[::-1] + list(range(17,25))
    
    GPIO.setmode(GPIO.BCM)
    # GPIO.setwarnings(False)
    for k in pins:
        # print(str(k))
        GPIO.setup(k, GPIO.OUT)
    try:
        while True:
            time.sleep(warten)
            GPIO.output(random.randint(1,24), GPIO.HIGH)
            time.sleep(warten)
            GPIO.output(random.randint(1,24), GPIO.LOW)
    except KeyboardInterrupt:
        GPIO.cleanup()

parser = argparse.ArgumentParser()
parser.add_argument('warten', type=float, help='lol')
args = parser.parse_args()
main(args.warten)
