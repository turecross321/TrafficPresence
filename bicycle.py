import RPi.GPIO as GPIO
import time

SPEED_SENSOR = 23 # physical pin 16
CADENCE_SENSOR = 24 # physical pin 18

POLLING_DELAY = 0.0
WHEEL_CIRCUMFERENCE = 1.885 # In meters
SPEED_STOPPED_THRESHOLD = 3 # Amount of seconds before assuming that the bicycle has stopped moving
CADENCE_STOPPED_THRESHOLD = 2

GPIO.setmode(GPIO.BCM)

GPIO.setup(SPEED_SENSOR, GPIO.IN)
GPIO.setup(CADENCE_SENSOR, GPIO.IN)

speed = 0 # Speed of bicycle in meters per second
last_speed_value = speed
last_speed_time = time.time()

cadence = 0 # How fast the cyclist is pedaling in RPM
last_cadence_value = cadence
last_cadence_time = time.time()

try:
    while True:
        speed_value = GPIO.input(SPEED_SENSOR) == 0 # True when magnet is detected
        speed_value_changed = speed_value != last_speed_value

        cadence_value = GPIO.input(CADENCE_SENSOR) == 0 # True when magnet is detected
        cadence_value_changed = cadence_value != last_cadence_value

        now = time.time()
        delta_speed_time = now - last_speed_time
        delta_cadence_time = now - last_cadence_time

        if delta_speed_time >= SPEED_STOPPED_THRESHOLD:
                speed = 0
                last_speed_time = now
        elif speed_value_changed and speed_value:
                print("Setting new speed")
                speed = WHEEL_CIRCUMFERENCE / delta_speed_time
                last_speed_time = now

        if delta_cadence_time >= CADENCE_STOPPED_THRESHOLD:
              cadence = 0
              last_cadence_time = now
        elif cadence_value_changed and cadence_value:
              print("Setting new RPM")
              cadence = 60 / delta_cadence_time
              last_cadence_time = now

        print(f"{speed} m/s | {speed * 3.6} km/h")
        print(f"{cadence} RPM")

        last_speed_value = speed_value
        last_cadence_value = cadence_value
        time.sleep(POLLING_DELAY)

except KeyboardInterrupt:
    # Cleanup GPIO settings before exiting
    GPIO.cleanup()