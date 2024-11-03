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


def simulate_states():
    pass


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
