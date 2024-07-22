import obd
from websocket import create_connection
import time
import json
import argparse

DISCORD_CLIENT_ID = "1258728548613619733"
SERVER_PASSWORD = "password"
SERVER_URL = "ws://127.0.0.1:8080"
UPDATE_INTERVAL = 15 # can't be less than 15 seconds to work
SUPPORTED_MODELS = {"skoda-fabia": "Skoda Fabia",
                  "skoda-octavia": "Skoda Octavia",
                  "car": "Car"}

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, help='The name of the model')
args = parser.parse_args()

# Access the model argument
if args.model:
    current_model_key = args.model
else:
    print('No model specified. Choosing default `car`.')
    print("Supported models:", SUPPORTED_MODELS)
    current_model_key = "car"

current_model_name = SUPPORTED_MODELS[current_model_key]
print(f"{current_model_name} has been selected")

print("Connecting to OBD device")
connection = obd.OBD()


CLIENT_TYPE_SENDER = 1

ws = create_connection(SERVER_URL, header={
                                  "client-type": str(CLIENT_TYPE_SENDER),
                                  "password": SERVER_PASSWORD,
                                  "discord-client-id": DISCORD_CLIENT_ID,
                                  "activity-name": "car"
                              })
print("Connected to Presence Server")

while True:
    if connection.is_connected():
        print("Connected to OBD adapter")
    else:
        print(f"Unable to connect to OBD adapter. Attempting to reconnect in {UPDATE_INTERVAL} seconds...")
        time.sleep(UPDATE_INTERVAL)
        break

    rpm = connection.query(obd.commands.RPM).value.magnitude
    speed = connection.query(obd.commands.SPEED).value.magnitude
    run_time = connection.query(obd.commands.RUN_TIME).value.magnitude
    fuel_level = connection.query(obd.commands.FUEL_LEVEL).value.magnitude
    temperature = connection.query(obd.commands.AMBIANT_AIR_TEMP).value.magnitude

    start = time.time() - run_time

    message = {
            "state": "Driving",
            "details": f"{int(speed)} km/h | {int(rpm)} RPM | {int(fuel_level)}% fuel | {temperature}° C",
            "timestamps": {"stdiart": start},
            "assets": {
                "large_image": current_model_key, 
                "large_text": current_model_name
            }
        }
    serialized = json.dumps(message)

    print(serialized)
    ws.send(serialized)
    print("Updated presence")
    time.sleep(UPDATE_INTERVAL)