import serial
import time


def get_sensor_data(out_stream):
    # Set up the serial connection
    arduino_port = 'COM3'  # Update with your port, e.g., '/dev/ttyUSB0' on Linux
    baud_rate = 9600       # Must match the baud rate in the Arduino code
    ser = serial.Serial(arduino_port, baud_rate)
    time.sleep(2)  # Give some time to establish the connection

    print("Starting to read data from pulse sensor...")

    try:
        while True:
            if ser.in_waiting > 0:
                # Read the incoming data from the Arduino
                pulse_value = ser.readline().decode('utf-8').strip()
                print(pulse_value)
    except KeyboardInterrupt:
        print("Data reading stopped by the user.")
    finally:
        ser.close()  # Close the serial connection when done
