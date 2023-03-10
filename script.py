from threading import Thread
from data_connector import DataConnector
import obd
from argparse import ArgumentParser
import queue
import time
import json
import uuid
import config
import requests

data_points = [obd.commands.SPEED, obd.commands.RPM, obd.commands.COOLANT_TEMP, obd.commands.INTAKE_TEMP, obd.commands.FUEL_LEVEL, obd.commands.ENGINE_LOAD]
live_data = { i.name : None for i in data_points }
data_log = []
outbound_queue = queue.Queue() #bound this?
drive_id = str(uuid.uuid4())

def take_data_sample():
    while True:
        outbound_queue.put(live_data)
        time.sleep(1)

def send_to_azure():
    while True:
        snapshots = []

        for i in range(20):
            try:
                snapshot = outbound_queue.get_nowait()
                snapshots.append(snapshot)
            except queue.Empty:
                break

        message = { 'DRIVE_ID': drive_id, 'SNAPSHOTS': snapshots }

        print("posting")
        result = requests.post(config.snapshot_data_url, json=message)
        print(result)

        time.sleep(5)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--mock", default=False)
    parser.add_argument("--port", default="\\.\\COM3")
    args = parser.parse_args()

    use_mock = args.mock is not None and args.mock == 'True'

    data_connector = DataConnector(live_data, data_points, use_mock, args.port)
    logger_thread = Thread(target=take_data_sample, daemon=True)
    sender_thread = Thread(target=send_to_azure, daemon=True)

    try:
        data_connector.start()
        logger_thread.start()
        sender_thread.start()
    except KeyboardInterrupt:
        data_connector.stop()