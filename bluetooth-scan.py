# Bluetooth LE scanner
# Prints the name and address of every nearby Bluetooth LE device

import time
import asyncio
from winrt.windows.devices import radios
from bleak import BleakScanner, BleakClient

TARGET_NAME = "My_BLE_Device"  # Replace with your target device name
ble_address = ''  # Will be set when the target device is found

async def bluetooth_power(turn_on):
    all_radios = await radios.Radio.get_radios_async()
    for this_radio in all_radios:
        if this_radio.kind == radios.RadioKind.BLUETOOTH:
            if turn_on:
                result = await this_radio.set_state_async(radios.RadioState.ON)
            else:
                result = await this_radio.set_state_async(radios.RadioState.OFF)

async def main():
    devices = await BleakScanner.discover()

    for device in devices:
        print(device)
        if device.name == TARGET_NAME:
            ble_address = device.address
            print(f"Found target device: {device.name} at {device.address}")
            
    if ble_address == None:
        print("Target device {TARGET_NAME} not found. Retrying in 5 seconds...")
        
    else:
        async with BleakClient(ble_address) as client:
            # we’ll do the read/write operations here
            print("Succesfully connected to {Target_NAME}")
            print(client.is_connected)
            quit()

if __name__ == '__main__':
    asyncio.run(bluetooth_power(True)) # Ensure Bluetooth is on
while True:
    print("Scanning for Bluetooth LE devices...")
    asyncio.run(main())
