import random

import serial
import time
from configs.enums import Vitals

"""this script should contain all methods to recive stream of vitals after implementation. secveral options exists 
because of technology change and functions only represent the logic of receiving data but not the output that should 
be exactly the same. receiver class will be implemented to receive the streaming function and run it (like adapter 
that has all options)"""


def get_sensor_data_via_usb_port(bracelet_to_update, channel: str = 'COM3'):
    """
    updates the state of the bracelet consecutively
    :param bracelet_to_update: the bracelet object
    :param channel: the usb_port_on pc
    """
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


def simulate_states(bracelet_to_update, is_critical=False):
    """
    Simulates the state of the bracelet, either in a critical condition or normal.
    :param bracelet_to_update: the bracelet object
    :param is_critical: flag to simulate critical conditions
    """
    # Initial state setup
    bracelet_to_update.set_state(
        {Vitals.PULSE: 100,
         Vitals.SATURATION: 75,
         Vitals.BLOODPRESSURE: (120, 100)}
    )

    start_time = time.time()  # Record the start time

    try:
        while True:
            elapsed_time = time.time() - start_time

            # Simulate changes to the pulse, saturation, and blood pressure
            if is_critical and elapsed_time >= 7:
                new_pulse = random.randint(223, 240)  # Escalated pulse after seven seconds or in a critical state
                new_saturation = random.randint(70, 85)  # Low saturation for critical state
                new_bp = (random.randint(140, 180), random.randint(90, 110))  # High blood pressure for critical state
            else:
                new_pulse = random.randint(80, 140)  # Normal pulse range
                new_saturation = random.randint(90, 100)  # Normal saturation range
                new_bp = (random.randint(110, 130), random.randint(70, 90))  # Normal blood pressure range

            bracelet_to_update.set_state(
                {Vitals.PULSE: new_pulse,
                 Vitals.SATURATION: new_saturation,
                 Vitals.BLOODPRESSURE: new_bp}
            )

            # Print the simulated state for debugging purposes
            print(f"Simulated state: Pulse={new_pulse}, Saturation={new_saturation}%, BP={new_bp}")

            time.sleep(1.25)  # Wait before the next update
    except KeyboardInterrupt:
        print("Simulation stopped by the user.")



class Receiver:
    def __init__(self, bracelet_to_update, receive_func):
        self.bracelet_to_update = bracelet_to_update
        self.receive_func = receive_func

    def start(self, **kwargs):
        """
        starts receiving data of vitals until termination
        :param kwargs:
        :return:
        """
        self.receive_func(bracelet_to_update=self.bracelet_to_update, **kwargs)
