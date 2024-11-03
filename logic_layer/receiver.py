import serial
import time
from configs.enums import Vitals


def get_sensor_data(bracelet_to_update, channel: str = 'COM3'):
    # Set up the serial connection
    arduino_port = channel  # Update with your port, e.g., '/dev/ttyUSB0' on Linux
    baud_rate = 9600  # Must match the baud rate in the Arduino code
    ser = serial.Serial(arduino_port, baud_rate)
    time.sleep(2)  # Give some time to establish the connection

    print("Starting to read data from pulse sensor...")

    try:
        while True:
            if ser.in_waiting > 0:
                # Read the incoming data from the Arduino
                pulse_value = ser.readline().decode('utf-8').strip()
                if pulse_value == 'We created a pulseSensor Object !':
                    continue
                bracelet_to_update.set_state(
                    {Vitals.PULSE: int(pulse_value),
                     Vitals.SATURATION: bracelet_to_update.saturation,
                     Vitals.BLOODPRESSURE: bracelet_to_update.blood_pressure}
                )
    except KeyboardInterrupt:
        print("Data reading stopped by the user.")
    finally:
        ser.close()  # Close the serial connection when done


def simulate_states():
    pass
