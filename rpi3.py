import numpy as np
import RPi.GPIO as GPIO
# import sys
import time
import zmq

def main():
    # a = np.zeros([8,3], dtype=np.int32)
    # pins = np.where(a==0, GPIO.LOW, GPIO.HIGH)
    context = zmq.Context()
    socket = context.socket(zmq.REQ)  # Client
    socket.connect('tcp://zw1:26231')
    while True:
        pins = np.random.choice((GPIO.LOW, GPIO.HIGH), [8,3])
        print(pins)
        bmsg = pins.tostring()
        socket.send(bmsg)
        antwort = socket.recv()
        print(antwort)
        time.sleep(10)

if __name__ == "__main__":
    main()

