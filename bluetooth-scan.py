# Bluetooth LE scanner
# Prints the name and address of every nearby Bluetooth LE device

import time
import asyncio
from winrt.windows.devices import radios
from bleak import BleakScanner, BleakClient

TARGET_NAME = "Your_device"  # Replace with your target device name
TARGET_ADRESS = None  # Will be set when the target device is found
NB_RETRIES = 5
TRIES = 1

async def bluetooth_power(turn_on):
    all_radios = await radios.Radio.get_radios_async()
    for this_radio in all_radios:
        if this_radio.kind == radios.RadioKind.BLUETOOTH:
            if turn_on:
                result = await this_radio.set_state_async(radios.RadioState.ON)
            else:
                result = await this_radio.set_state_async(radios.RadioState.OFF)

async def main():
    global TARGET_ADRESS
    devices = await BleakScanner.discover()

    for device in devices:
        print(device)
        if device.name == TARGET_NAME:
            TARGET_ADRESS = device.address
            
    if TARGET_ADRESS is None:
        print(f"Target device {TARGET_NAME} not found. Retrying in 5 seconds... (Try {TRIES}/{NB_RETRIES})")
        return False
    else:
        print(f"Found target device: {TARGET_NAME} at {TARGET_ADRESS}")
        async with BleakClient(TARGET_ADRESS) as client:
            # we’ll do the read/write operations here
            print(f"Succesfully connected to {TARGET_NAME} in {TRIES} tries.")
            print(client.is_connected)
            return True
            
if __name__ == '__main__':
    for i in range(0, NB_RETRIES):
        asyncio.run(bluetooth_power(True)) # Ensure Bluetooth is on
        print("Scanning for Bluetooth LE devices...")
        stop = asyncio.run(main())
        if stop:
            break # Exit loop if connected
        TRIES += 1
        