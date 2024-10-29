import threading
import time
import tkinter as tk
from control_unit import ControlUnit
from control_unit_ui import ControlUnitUI
from enums import Vitals

# Initialize Control Unit
control_unit = ControlUnit()


# Function to simulate a patient status change after 10 seconds
def simulate_status_change():
    observed_bracelet = control_unit.obs_bracelet
    initial_state = {
        Vitals.PULSE: 75,  # Normal pulse
        Vitals.SATURATION: 95,  # Normal saturation
        Vitals.BLOODPRESSURE: (100, 80)  # Normal blood pressure
    }
    observed_bracelet.set_state(initial_state)

    # Wait 10 seconds
    time.sleep(3)

    # Trigger a critical state by changing pulse
    critical_state = {
        Vitals.PULSE: 200,  # Critical pulse
        Vitals.SATURATION: 95,  # Normal saturation
        Vitals.BLOODPRESSURE: (100, 80)  # Normal blood pressure
    }
    observed_bracelet.set_state(critical_state)


# Set up the tkinter root and UI
root = tk.Tk()
control_unit_ui = ControlUnitUI(control_unit, root)

# Run the simulation in a separate thread
control_unit_thread = threading.Thread(target=control_unit.run)
simulation_thread = threading.Thread(target=simulate_status_change)
control_unit_thread.start()
simulation_thread.start()

# Start the UI loop
root.mainloop()
