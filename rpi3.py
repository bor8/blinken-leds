import numpy as np
import queue
import RPi.GPIO as GPIO
# import sys
import time
import zmq

def main():
    init_warten = 1.0
    fps = 4.0
    fpsk_min = 1.0 / 500.0
    q_target = 10

    fpsk = 1.0 / fps
    q = queue.Queue()
    # a = np.zeros([8,3], dtype=np.int32)
    # pins = np.where(a==0, GPIO.LOW, GPIO.HIGH)
    pins = np.random.choice((GPIO.LOW, GPIO.HIGH), [8,18])
    print(pins)
    context = zmq.Context()
    socket1 = context.socket(zmq.REQ)  # Client
    socket2 = context.socket(zmq.REQ)  # Client
    socket1.connect('tcp://zw1:26231')
    socket2.connect('tcp://zw2:26231')
    video_start_zeit = time.time() + init_warten
    abspiel_soll_zeit_max = video_start_zeit
    qsize1 = 0
    while True:
        while q.qsize() < q_target:
            if abspiel_soll_zeit_max <= time.time():
                print('Laggen!')
                abspiel_soll_zeit_max = time.time() + init_warten
            pins1 = pins[:, 0:3]
            pins2 = pins[:, 3:6]
            pins3 = pins[:, 6:9]
            pins4 = pins[:, 9:12]
            pins5 = pins[:, 12:15]
            pins6 = pins[:, 15:18]
            b1 = pins1.tostring()
            b2 = pins2.tostring()
            b3 = pins3.tostring()
            b4 = pins4.tostring()
            b5 = pins5.tostring()
            b6 = pins6.tostring()
            q.put((abspiel_soll_zeit_max, b1, b2, b3, b4, b5, b6))
            abspiel_soll_zeit_max += fpsk
            # print(pins)
            pins = np.roll(pins, 1, axis=1)
        if qsize1 < q_target:
            while q.qsize() > 0:
                ts, b1, b2, b3, b4, b5, b6 = q.get()
                # print(ts)
                socket1.send_pyobj((ts, b1))
                socket2.send_pyobj((ts, b2))
                qsize1 = socket1.recv_pyobj()
                qsize2 = socket2.recv_pyobj()
        socket1.send_pyobj('Weiter!')
        socket2.send_pyobj('Weiter!')
        qsize1 = socket1.recv_pyobj()
        qsize2 = socket2.recv_pyobj()
        # print(qsize1)
        time.sleep(fpsk_min * 3.0)

if __name__ == "__main__":
    main()

