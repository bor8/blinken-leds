import numpy as np
import RPi.GPIO as GPIO
# import sys
import time
import zmq

def main():
    # a = np.zeros([8,3], dtype=np.int32)
    # pins = np.where(a==0, GPIO.LOW, GPIO.HIGH)
    pins = np.random.choice((GPIO.LOW, GPIO.HIGH), [8,18])
    print(pins)
    context = zmq.Context()
    socket1 = context.socket(zmq.REQ)  # Client
    socket2 = context.socket(zmq.REQ)  # Client
    socket1.connect('tcp://zw1:26231')
    socket2.connect('tcp://zw2:26231')
    while True:
        pins = np.roll(pins, 1, axis=0)
        pins1 = pins[:, 0:3]
        pins2 = pins[:, 3:6]
        bmsg1 = pins1.tostring()
        bmsg2 = pins2.tostring()
        socket1.send(bmsg1)
        socket2.send(bmsg2)
        antwort1 = socket1.recv()
        #print(antwort1)
        antwort2 = socket2.recv()
        #print(antwort2)
        time.sleep(1.0/10.0)

if __name__ == "__main__":
    main()

