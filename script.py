from threading import Thread
from data_connector import DataConnector
import obd
from argparse import ArgumentParser

data_points = [obd.commands.SPEED, obd.commands.RPM, obd.commands.COOLANT_TEMP, obd.commands.INTAKE_TEMP, obd.commands.FUEL_LEVEL, obd.commands.ENGINE_LOAD]
live_data = { i.name : None for i in data_points }

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--mock", default=False)
    parser.add_argument("--port", default="\\.\\COM3")
    args = parser.parse_args()

    use_mock = args.mock is not None and args.mock == 'True'

    data_connector = DataConnector(live_data, data_points, use_mock, args.port)
    data_connector.start()