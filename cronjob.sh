#/bin/bash

exec &> /home/pi/git/blinken-leds/cronjob.log

echo 'Start: '$(date)

[ "$1" = '--wait-for-network' ] && sleep 60

# /usr/bin/screen -d -m

# /usr/bin/python3 /home/pi/git/blinken-leds/LED_24_rider.py 0.1
# /usr/bin/python3 /home/pi/git/blinken-leds/LED_24_timer.py

# Slaves
/usr/bin/python3 /home/pi/git/blinken-leds/zw.py

[ "$1" = '--wait-for-network' ] && sleep 60

# Master
[ "$(hostname)" = 'zero1' ] && /usr/bin/python3 /home/pi/git/blinken-leds/rpi3.py

echo 'Ende: '$(date)

echo '---'

