import threading
import time
import tkinter as tk
from logic_layer.control_unit.control_unit import ControlUnit
from frontend.new_ui import ControlUnitUI
from configs.enums import Vitals

# Initialize Control Unit
controller = ControlUnit()
# Set up the tkinter root and UI
root = tk.Tk()
ui = ControlUnitUI(controller, root)

# Run the simulation in a separate thread
controller_thread = threading.Thread(target=controller.run)
simulation_bracelet_threads = [threading.Thread(target=controller.paired_bracelets[i].run,
                                                args=[True, '', True] if i % 3 == 0 else [True, '', False]) for i in
                               range(len(controller.paired_bracelets))]
def terminate_threads_on_ui_exit(threads: list):
    def on_closing():
        for thread in threads:
            if thread.is_alive():
                thread.join(timeout=1)  # Attempt to join all threads gracefully
        root.destroy()

    return on_closing

for t in simulation_bracelet_threads:
    t.start()
# Start the UI loop
root.protocol("WM_DELETE_WINDOW", terminate_threads_on_ui_exit(simulation_bracelet_threads + [controller_thread]))
root.mainloop()
controller_thread.start()


controller_thread.join()
