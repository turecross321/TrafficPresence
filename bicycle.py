import RPi.GPIO as GPIO
import time

# Set up GPIO 23 as an input (physical pin 16)
SPEED_SENSOR = 23
POLLING_DELAY = 0.1
WHEEL_CIRCUMFERENCE = 2.4 # In meters
STOPPED_THRESHOLD = 3 # Amount of seconds before assuming that the bicycle has stopped moving

GPIO.setmode(GPIO.BCM)

GPIO.setup(SPEED_SENSOR, GPIO.IN)

speed = 0 # Speed of bicycle in meters per second
last_speed_value = speed
last_speed_time = time.time()

try:
    while True:
        speed_value = GPIO.input(SPEED_SENSOR) == 0 # True when magnet is detected
        speed_value_changed = speed_value != last_speed_value

        now = time.time()
        delta_time = now - last_speed_time
        if delta_time >= STOPPED_THRESHOLD:
                speed = 0
                last_speed_time = now
        elif speed_value_changed and speed_value:
                print("Setting new speed")
                speed = WHEEL_CIRCUMFERENCE / delta_time
                last_speed_time = now

        print(f"{speed} m/s | {speed * 3.6} km/h")

        last_speed_value = speed_value
        time.sleep(POLLING_DELAY)

except KeyboardInterrupt:
    # Cleanup GPIO settings before exiting
    GPIO.cleanup()