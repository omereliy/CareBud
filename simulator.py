import sys
import threading
import time
import tkinter as tk
from logic_layer.control_unit.control_unit import ControlUnit
from frontend.new_ui import ControlUnitUI
from configs.enums import Vitals
from logic_layer.receiver import get_sensor_data

# Initialize Control Unit
controller = ControlUnit()


# Function to simulate a patient status change after 10 seconds
def simulate_patient(data: list[dict], patient_index):
    counter = 0
    length = len(data)
    while True:
        controller.paired_bracelets[patient_index].set_state(data[counter % length])
        counter += 1


def simulate_status_change():
    brace1 = controller.obs_bracelet
    initial_state = {
        Vitals.PULSE: 75,  # Normal pulse
        Vitals.SATURATION: 95,  # Normal saturation
        Vitals.BLOODPRESSURE: (100, 80)  # Normal blood pressure
    }
    brace1.set_state(initial_state)

    # Wait 10 seconds
    time.sleep(3)

    # Trigger a critical state by changing pulse
    critical_state = {
        Vitals.PULSE: 210,  # Critical pulse
        Vitals.SATURATION: 95,  # Normal saturation
        Vitals.BLOODPRESSURE: (100, 80)  # Normal blood pressure
    }
    brace1.set_state(critical_state)


# Set up the tkinter root and UI
root = tk.Tk()
ui = ControlUnitUI(controller, root)

# Run the simulation in a separate thread
controller_thread = threading.Thread(target=controller.run)
simulation_bracelet_thread = threading.Thread(target=simulate_status_change)
sensor_bracelet_thread = threading.Thread(target=controller.paired_bracelets[1].run, args=[False, 'COM3'])


controller_thread.start()
sensor_bracelet_thread.start()
simulation_bracelet_thread.start()

# Start the UI loop
root.mainloop()

controller_thread.join()
simulation_bracelet_thread.join()
sensor_bracelet_thread.join()
