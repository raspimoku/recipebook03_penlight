import bluetooth
from machine import Pin
import time
import ubinascii

ble = bluetooth.BLE()
ble.active(True)

SERVICE_UUID = bluetooth.UUID("12345678-1234-1234-1234-123456789abc")   # <1>
CHAR_UUID = bluetooth.UUID("12345678-1234-1234-1234-123456789abd")      # <1>

char = (CHAR_UUID, bluetooth.FLAG_WRITE | bluetooth.FLAG_READ)          # <2>
service = (SERVICE_UUID, (char,))
((char_handle,),) = ble.gatts_register_services((service,))             # <3>

def on_ble_event(event, data):                                          # <4>
    if event == 1:  # _IRQ_CENTRAL_CONNECT                              # <5>
        conn_handle, addr_type, addr = data
        print(f"Connected: {ubinascii.hexlify(addr).decode()}")

    elif event == 2:  # _IRQ_CENTRAL_DISCONNECT                         # <6>
        conn_handle, addr_type, addr = data
        print(f"Disconnected: {ubinascii.hexlify(addr).decode()}")
        # re-advertise
        ble.gap_advertise(100, b'\x02\x01\x06\x0A\x09SimpleBLE')

    if event == 3:  # _IRQ_GATTS_WRITE                                  # <7>
        value_handle = data[1] if isinstance(data, tuple) and len(data) > 1 else data
        value = ble.gatts_read(value_handle)

        if len(value) >= 3:
            r, g, b = value[0], value[1], value[2]
            print(f"Received RGB: ({r}, {g}, {b})")
        else:
            print(f"Received raw bytes: {value}")

ble.irq(on_ble_event)                                                  # <8>
ble.gap_advertise(100, b'\x02\x01\x06\x0A\x09SimpleBLE')               # <9>
