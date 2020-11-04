import itertools
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import queue
import RPi.GPIO as GPIO
import requests
# import sys
import time
import zmq


def temperature():
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?appid=35b4c5927df9fb5401cd572426127ff2&q=Kirdorf&units=metric')
    data = r.json()
    temp = data['main']['temp']  # feels_like
    print(temp)
    return temp


def text_phantom(text, height, width):
    # Availability is platform dependent
    font = 'arial'

    # Create font
    # size_ = size // len(text)
    # print(size_)
    size_ = 11
    pil_font = ImageFont.truetype(font + ".ttf", size=size_, encoding="unic")
    text_width, text_height = pil_font.getsize(text)

    # create a blank canvas with extra space between lines
    canvas = Image.new('RGB', [width, height], (255, 255, 255))

    # draw the text onto the canvas
    draw = ImageDraw.Draw(canvas)
    # offset = ((size - text_width) // 2,
    #           (size - text_height) // 2)
    offset = (0, -2)
    white = "#000000"
    draw.text(offset, text, font=pil_font, fill=white)

    # Convert the canvas into an array with values in [0, 1]
    # return (255 - np.asarray(r)) / 255.0
    thresh = 200
    fn = lambda x: 255 if x > thresh else 0
    r = canvas.convert('L').point(fn, mode='1')
    return np.asarray(r)


def main():
    init_warten = 3.0
    fps = 10.0  # Attention! Don't make smaller than 1.0!
    fpsk_min = 1.0 / 500.0
    q_target = 100

    fpsk = 1.0 / fps
    q = queue.Queue()

    height = 8
    width = 18

    active_shows = ('temperature',)

    shows = {}
    #
    shows['random'] = {
        'only_one_run': False,
        'pins': np.random.choice((GPIO.LOW, GPIO.HIGH), [height, width]),
        'roll': 1,  # -1: move to left  # 0: idle  # 1: move to right
        'size': (height, width)
    }
    #
    pins = np.full([height, width], GPIO.HIGH, dtype=np.int32)
    pins[:, 0] = GPIO.LOW  # first column
    shows['debugging'] = {
        'only_one_run': False,
        'pins': pins,
        'roll': 1,  # -1: move to left  # 0: idle  # 1: move to right
        'size': (height, width)
    }
    #
    shows['christmas'] = {
        'only_one_run': False,
        'pins': text_phantom('F r o h e  W e i h n a c h t e n', height, width * 10),
        'roll': -1,  # -1: move to left  # 0: idle  # 1: move to right
        'size': (height, width)
    }
    # 
    # x = 0
    # y = 5
    # pins[x:x+text_.shape[0], y:y+text_.shape[1]] = text_
    shows['temperature'] = {
        'duration': 60,
        'only_one_run': True,
        'pins': lambda height, width: np.where(text_phantom(f'{round(temperature())}°', height, width) == True, GPIO.LOW, GPIO.HIGH),
        'roll': 0,  # -1: move to left  # 0: idle  # 1: move to right
        'size': (height, width)
    }

    context = zmq.Context()
    socket1 = context.socket(zmq.REQ)  # Client
    socket2 = context.socket(zmq.REQ)  # Client
    socket3 = context.socket(zmq.REQ)  # Client
    socket4 = context.socket(zmq.REQ)  # Client
    socket5 = context.socket(zmq.REQ)  # Client
    socket6 = context.socket(zmq.REQ)  # Client
    socket1.connect('tcp://zero1:26231')
    socket2.connect('tcp://zero2:26231')
    socket3.connect('tcp://zero3:26231')
    socket4.connect('tcp://zero4:26231')
    socket5.connect('tcp://zero5:26231')
    socket6.connect('tcp://zero6:26231')

    for show in itertools.cycle(active_shows):
        duration = shows[show]['duration']
        end = time.time() + duration
        only_one_run = shows[show]['only_one_run']
        pins = shows[show]['pins']
        roll = shows[show]['roll']
        height, width = shows[show]['size']

        pins = pins(height, width) if callable(pins) else pins
        print(pins)

        video_start_zeit = time.time() + init_warten
        abspiel_soll_zeit_max = video_start_zeit
        qsize1 = 0
        first_round = True
        second_round = False
        while True:
            while q.qsize() < q_target:
                if abspiel_soll_zeit_max <= time.time():
                    print('Laggen!')
                    abspiel_soll_zeit_max = time.time() + init_warten
                if first_round:
                    pins_alt = np.full([height, width], 0, dtype=np.int32)
                    pins_diff = np.full([height, width], -1, dtype=np.int32)
                pins1 = pins_diff[:, 0:3]
                pins2 = pins_diff[:, 3:6]
                pins3 = pins_diff[:, 6:9]
                pins4 = pins_diff[:, 9:12]
                pins5 = pins_diff[:, 12:15]
                pins6 = pins_diff[:, 15:18]
                b1 = pins1.tostring()
                b2 = pins2.tostring()
                b3 = pins3.tostring()
                b4 = pins4.tostring()
                b5 = pins5.tostring()
                b6 = pins6.tostring()
                q.put((abspiel_soll_zeit_max, b1, b2, b3, b4, b5, b6))
                abspiel_soll_zeit_max += fpsk
                pins = np.roll(pins, roll, axis=1)
                pins_diff = pins - pins_alt
                pins_alt = np.copy(pins)
                if second_round and only_one_run:
                    break
                if first_round:
                    first_round = False
                    second_round = True
            if qsize1 < q_target:
                while q.qsize() > 0:
                    ts, b1, b2, b3, b4, b5, b6 = q.get()
                    # print(ts)
                    socket1.send_pyobj((ts, b1))
                    socket2.send_pyobj((ts, b2))
                    socket3.send_pyobj((ts, b3))
                    socket4.send_pyobj((ts, b4))
                    socket5.send_pyobj((ts, b5))
                    socket6.send_pyobj((ts, b6))
                    qsize1 = socket1.recv_pyobj()
                    qsize2 = socket2.recv_pyobj()
                    qsize3 = socket3.recv_pyobj()
                    qsize4 = socket4.recv_pyobj()
                    qsize5 = socket5.recv_pyobj()
                    qsize6 = socket6.recv_pyobj()
            socket1.send_pyobj('Weiter!')
            socket2.send_pyobj('Weiter!')
            socket3.send_pyobj('Weiter!')
            socket4.send_pyobj('Weiter!')
            socket5.send_pyobj('Weiter!')
            socket6.send_pyobj('Weiter!')
            qsize1 = socket1.recv_pyobj()
            qsize2 = socket2.recv_pyobj()
            qsize3 = socket3.recv_pyobj()
            qsize4 = socket4.recv_pyobj()
            qsize5 = socket5.recv_pyobj()
            qsize6 = socket6.recv_pyobj()
            # print(qsize1)
            if only_one_run:
                break
            time.sleep(fpsk_min * 3.0)

        show_time_left = end - time.time()
        if show_time_left > 0.0:
            time.sleep(show_time_left)

if __name__ == "__main__":
    main()

