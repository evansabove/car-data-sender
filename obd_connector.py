import obd
import time 
from subprocess import call
import pexpect
import platform

def bind_rfcomm_port():
    if platform.system() == 'Linux':
        print("Attempting to bind hci0 device to 00:1D:A5:68:98:8B")
        pexpect.run('sudo rfcomm bind hci0 00:1D:A5:68:98:8B')
        print("Bind complete")

def connect(config):
    bind_rfcomm_port()

    connection_attempt = 1

    while True:
        if connection_attempt > config['connection_attempt_limit']:
            return None

        print("Connection attempt " + str(connection_attempt) + "...")

        obd.logger.setLevel(obd.logging.DEBUG)
        conn = obd.Async(config['communication_port'] or None)
        obd.logger.setLevel(obd.logging.FATAL)

        if conn.is_connected():
            print("Connection made using protocol ", conn.protocol_name())
            print("Supported commands: ", ', '.join([x.name for x in conn.supported_commands]))
            
            return conn

        time.sleep(1)
        connection_attempt = connection_attempt + 1