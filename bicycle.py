# WONT WORK WITH LATER THAN PYTHON 3.10

from pyfirmata import Arduino, util
import time

WHEEL_ANALOG_PIN = 0
WHEEL_CIRCUMEFRENCE = 2.44 # in meters

board = Arduino('COM7')
wheel_sensor = board.get_pin(f"a:{str(WHEEL_ANALOG_PIN)}:i")
board.analog[WHEEL_ANALOG_PIN].enable_reporting()

it = util.Iterator(board)
it.start()

last_status = None
last_true_time = None
speed = 0 # meters / second

while True:
    wheel_reading = wheel_sensor.read()

    if wheel_reading and wheel_reading < 0.3:
        status = True
    else:
        status = False

    #print(f"CHANGE: {status != last_status} | NEW: {status} | LAST: {last_status} | {wheel_reading}")

    now = time.time()
    if last_true_time != None:
        diff = now - last_true_time

        if status and status != last_status: # if it just turned true
            speed = WHEEL_CIRCUMEFRENCE / diff # calculate speed in meters per second
        elif diff > 3: # if it's not gotten a new reading in 3 seconds, assume that it's stopped
            diff = now
            speed = 0

    if status:
        last_true_time = now

    last_status = status

    print(f"SPEED: {speed} m/s | {speed * 3.6} km/h")
    time.sleep(0.05)

    
