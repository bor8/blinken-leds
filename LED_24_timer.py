import RPi.GPIO as GPIO
import time

def main():
    pins = list(range(1, 25))
    GPIO.setmode(GPIO.BCM)
    for k in pins:
        GPIO.setup(k, GPIO.OUT)
    zeit = int(time.time_ns() / (10 ** 9))  # in Sekunden
    try:
        while True:
            zeit_vorher = zeit
            zeit = int(time.time_ns() / (10 ** 9))  # in Sekunden
            if zeit_vorher != zeit:
                # Alle "gleichzeitig":
                for k in pins:
                    GPIO.output(k, GPIO.HIGH)
                time.sleep(0.1)
                for k in pins:
                    GPIO.output(k, GPIO.LOW)
    except KeyboardInterrupt:
        GPIO.cleanup()

main()
