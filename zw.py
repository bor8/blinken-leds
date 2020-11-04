import numpy as np
import queue
import RPi.GPIO as GPIO
import socket
# import sys
import threading
import time
import zmq

fpsk_min = 1.0 / 500.0
q_target = 100
q = queue.Queue()
tqw_alive = True

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
    tqw = threading.Thread(target=q_worker)
    tqw.start()
    try:
        while True:
            ts, bmsg = q.get()
            pins = np.frombuffer(bmsg, dtype=np.int32)
            pins = pins.reshape(8,3)
            # print(pins)
            pins = pins.T.flat
            # time.sleep(1.0/30.0 - (time.time() % (1./30.)))
            highs = np.where(pins == GPIO.HIGH)[0]
            lows = np.where(pins == -1)[0]
            highs += 1
            lows += 1
            np.random.shuffle(highs)
            np.random.shuffle(lows)
            highs = highs.tolist()
            lows = lows.tolist()
            while True:
                if time.time() > ts:
                    # print(ts)
                    break
                time.sleep(fpsk_min)
            # print(highs)
            # print(lows)
            GPIO.output(highs, GPIO.HIGH)
            GPIO.output(lows, GPIO.LOW)
    finally:
        tqw_alive = False
        GPIO.cleanup()

def q_worker():
    context = zmq.Context()
    socket = context.socket(zmq.REP)  # Server
    ip = get_ip()
    print(ip)
    # Funzt nur mit LAN-IP oder Stern:
    socket.bind('tcp://{}:26231'.format(ip))
    while tqw_alive == True:
        while q.qsize() < q_target:
            via_rpi3 = socket.recv_pyobj()
            socket.send_pyobj(int(q.qsize()))
            if via_rpi3 == 'Weiter!':
                break
            ts, bmsg = via_rpi3
            q.put((ts, bmsg))
        time.sleep(fpsk_min * 3.0)

if __name__ == "__main__":
    main()
