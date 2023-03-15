from threading import Thread
from data_connector import DataConnector
import obd
from argparse import ArgumentParser
import queue
import time
import uuid
import config
import requests
import copy 

data_points = [obd.commands.SPEED, obd.commands.RPM, obd.commands.COOLANT_TEMP, obd.commands.INTAKE_TEMP, obd.commands.FUEL_LEVEL, obd.commands.ENGINE_LOAD]
live_data = { i.name : None for i in data_points }
data_log = []
outbound_queue = queue.Queue()
drive_id = str(uuid.uuid4())

def take_data_sample():
    print("Taking data samples...")
    sequence_number = 0

    while True:
        sequence_number += 1
        
        item = copy.deepcopy(live_data)
        item['SEQUENCE_NUMBER'] = sequence_number

        add_to_queue(item)

        time.sleep(1)

def add_to_queue(item):
    try:
        outbound_queue.put_nowait(item)
    except queue.Full:
        print("Queue is full, discarding item")

def send_to_azure():
    while True:
        snapshots = []

        while True:
            try:
                snapshot = outbound_queue.get_nowait()
                snapshots.append(snapshot)
            except queue.Empty:
                break

        message = { 'DRIVE_ID': drive_id, 'SNAPSHOTS': snapshots }

        try:
            print("Trying to post data...")
            response = requests.post(config.snapshot_data_url, json=message)
            print("Posted data, response " + str(response.status_code))
        except requests.exceptions.ConnectionError:
            print("Could not get connection.")

            # Put these items back on the queue to process again
            for snapshot in snapshots:
                add_to_queue(snapshot)

        except Exception as e:
            print(e)
            pass

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
    data_connector_thread = Thread(target=data_connector.start)

    try:
        data_connector_thread.start()
        logger_thread.start()
        sender_thread.start()
    except KeyboardInterrupt:
        data_connector.stop()
    except Exception as e:
        print(e)

    print("Program finished")