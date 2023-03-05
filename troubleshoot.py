import obd
from time import sleep

def print_magnitude(response):
    print(response.value.magnitude)

def try_connect():
    obd.logger.setLevel(obd.logging.DEBUG)

    print("Trying to connect to blank")
    conn = obd.Async(fast=False, timeout=30)

    if conn.is_connected():
        print("Connection made with blank")
    else:
        print("Trying to connect to /dev/rfcomm0")
        conn = obd.Async('/dev/rfcomm0', fast=False, timeout=10)

        if conn.is_connected():
            print("Connection made with rfcomm0")
        else:
            print("Failed to make a connection")
            return None

    return conn

connection = try_connect()

if not connection is None:
    connection.watch(obd.commands.RPM, callback=print_magnitude)

sleep(1000)