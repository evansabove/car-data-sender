import obd_connector
import mock_obd_connector
import time

class DataConnector:
    config = { 'connection_attempt_limit': 30 }
    use_mock = False
    running = True

    def __init__(self, live_data, data_points, mock_data, port):
        self.live_data = live_data
        self.data_points = data_points
        self.use_mock = mock_data
        self.config['communication_port'] = port

    def process_response(self, response):
        #print("Processing response for " + response.command.name + ". Value " + str(response.value.magnitude))
        if not response.is_null():
            self.live_data[response.command.name] = round(response.value.magnitude, 2)

    def configure_watches(self):
        for i in self.data_points:
            print("Registering watch for " + str(i))
            self.connection.watch(i, callback=self.process_response)

        print("Watches configured")

    def get_connector(self):
        return mock_obd_connector.connect if self.use_mock else obd_connector.connect

    def start(self):
        self.connection = self.get_connector()(self.config)

        if self.connection is None:
            print("Connection could not be made. Not trying any more!")
            return

        self.live_data['TIMESTAMP'] = None

        self.configure_watches()
        self.connection.start()
        print("Connection started")

        while True:
            time.sleep(1)

    def stop(self):
        print("Stopping connection")
        self.connection.stop()
        self.running = False