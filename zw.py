import base64
import numpy as np
import RPi.GPIO as GPIO
import socket
# import sys
import zmq

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def main():
    GPIO.setmode(GPIO.BCM)
    # GPIO.setwarnings(False)
    for k in range(1, 25):
        GPIO.setup(k, GPIO.OUT)
    context = zmq.Context()
    socket = context.socket(zmq.REP)  # Server
    ip = get_ip()
    print(ip)
    # Funzt nur mit LAN-IP:
    socket.bind('tcp://{}:26231'.format(ip))
    try:
        while True:
            bmsg = socket.recv()
            print(type(bmsg))
            pins = np.fromstring(bmsg, dtype=np.int32)
            pins_original = pins.reshape(8,3)
            print(pins_original)
            k = 0
            for pin in pins_original.T.flat:
                k += 1
                # print('blubb' + str(pin))
                GPIO.output(k, int(pin))
            socket.send_string('angekommen und verarbeitet')
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
