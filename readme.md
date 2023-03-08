# Setup instructions

Start with:
- Raspberry Pi Zero W
- A Raspbian installation - 32-bit lite
- ELM 327 bluetooth OBD reader

## Set up access to your local network:

- Create wpa_supplicant.conf in the root of the D drive:

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
country=<Insert 2 letter ISO 3166-1 country code here>
update_config=1

network={
 ssid="<Name of your wireless LAN>"
 psk="<Password for your wireless LAN>"
}
```

## Enable SSH
- Create empty file called `ssh` in the root of the D drive.

## Software

Install git

- `sudo apt-get update`
- `sudo apt-get upgrade`
- `sudo apt-get install git`

Get this code:

- `git clone https://github.com/evansabove/car-data.git`

Install dependencies

- `sudo apt-get install python3-pip`
- `python -m pip install obd`
- `python -m pip install azure-storage-queue`
- `python -m pip install pexpect`

Create config file

- `nano car-data-sender/config.py`

With the following content

```
  azure_queue_connection_string = {your connection string}
  azure_queue_name = {your queue name}
```

Use bluetoothctl to get MAC address of OBDII adapter. Keep a note of it.

## Bluetooth setup

- `bluetoothctl`
- `agent on`
- `scan on`
- `pair [XX:XX:XX:XX:XX:XX]`
- `trust [XX:XX:XX:XX:XX:XX]`

where `[XX:XX:XX:XX:XX:XX]` is the MAC address of the OBD adapter.

## Script setup
- `mkdir {your-home-dir}/.config/autostart`
- `nano {your-home-dir}/.config/autostart/cardata.desktop`
- Add the following code to the file:
  ```
  [Desktop Entry]
  Type=Application
  Name=CarData
  Exec=/usr/bin/python3 {your-home-dir}/car-data-sender/script.py --log=False --port=/dev/rfcomm0
  ```




00:1D:A5:68:98:8B



sudo rfcomm connect hci0 00:1D:A5:68:98:8B 0h