import datetime
from datetime import datetime, timedelta
import pandas as pd
from configs.config_constants import *
from logic_layer.patient.bracelet import Bracelet
import pyttsx3
from configs.enums import *
import serial
import time


# =========================== functions ========================================================

def blood_pressure_to_sentence(blood_pressure: tuple):
    """
    Converts a blood pressure tuple into a readable string format.

    Args:
        blood_pressure (tuple): Blood pressure values (systolic, diastolic).

    Returns:
        str: Formatted blood pressure description.
    """
    return f"{blood_pressure[0]} on {blood_pressure[1]}"


def read_bracelets_stats(bracelet: Bracelet):
    """
    Uses text-to-speech to read the current stats of a bracelet.

    Args:
        bracelet (Bracelet): The bracelet instance.
    """
    engine = pyttsx3.init()
    engine.say(f"saturation is {bracelet.saturation}")
    engine.runAndWait()
    engine.say(f"pulse is {bracelet.pulse}")
    engine.runAndWait()
    engine.say(f"blood pressure is {blood_pressure_to_sentence(bracelet.blood_pressure)}")
    engine.runAndWait()


# =============================== control unit class ======================================================

class ControlUnit:
    """
    Manages multiple bracelet devices and monitors their statuses in real-time.
    Provides functionality to switch between patients, stream status, and trigger alerts.

    Attributes:
        paired_bracelets (list): List of paired Bracelet objects.
        mode (Modes): Operating mode of the control unit (e.g., NOTICEONLY).
        obs_bracelet (Bracelet): Currently observed bracelet.
        terminate (bool): Termination flag for the control unit.
    """
    paired_bracelets: list[Bracelet]
    mode: Modes
    obs_bracelet: Bracelet
    terminate: bool = False
    last_alert_from_patient: list = [None for _ in bracelet_index_range]

    def __init__(self):
        self.paired_bracelets = [Bracelet(i, 0, 0, (0, 0)) for i in bracelet_index_range]
        self.mode = Modes.NOTICEONLY
        self.obs_bracelet = self.paired_bracelets[0]
        for bracelet in self.paired_bracelets:
            bracelet.add_listener(self.on_bracelet_update)

    def set_observed_bracelet(self, observed_bracelet_index: int):
        """Sets the observed bracelet by index."""
        self.obs_bracelet = self.paired_bracelets[observed_bracelet_index]

    def increment_bracelet_index(self):
        """Increments the observed bracelet index by one."""
        self.set_observed_bracelet(self.obs_bracelet.num + 1)

    def decrement_bracelet_index(self):
        """Decrements the observed bracelet index by one."""
        self.set_observed_bracelet(self.obs_bracelet.num - 1)

    def switch_mode(self):
        """Toggles between NOTICEONLY and STATESTREAM modes."""
        if self.mode == Modes.STATESTREAM:
            self.mode = self.mode.NOTICEONLY
        else:
            self.mode = self.mode.STATESTREAM

    def get_all_states(self) -> pd.DataFrame:
        """Returns a DataFrame with the current state of all bracelets."""
        info: dict[str, list] = \
            {"patient": [i for i in bracelet_index_range],
             "pulse": [None for _ in bracelet_index_range],
             "blood pressure": [None for _ in bracelet_index_range],
             "saturation": [None for _ in bracelet_index_range]}

        for bracelet in self.paired_bracelets:
            info["pulse"][bracelet.num] = bracelet.pulse
            info["saturation"][bracelet.num] = bracelet.saturation
            info["blood pressure"][bracelet.num] = bracelet.blood_pressure

        return pd.DataFrame(info)

    def sound_pulse_and_saturation(self):
        exit_signal = False
        self.obs_bracelet.get_color()  # no meaning, squiggle for method from function irritates me
        while not exit_signal:
            pass

    def notice_only(self):
        """Monitors bracelet status, alerting only if bracelet color is critical."""
        exit_signal = False
        while not exit_signal:
            for bracelet in self.paired_bracelets:
                current_time = datetime.now()
                last_alert_time = self.last_alert_from_patient[bracelet.num]
                if (bracelet.get_color() == Colors.RED and
                        (last_alert_time is None or current_time - last_alert_time >= timedelta(seconds=20))):
                    bracelet.alert_if_critical()
                    self.last_alert_from_patient[bracelet.num] = datetime.now()

    def on_bracelet_update(self, bracelet_num):
        """Handle updates when a bracelet's state changes."""
        # Notify the UI or other parts of the system about the change
        if hasattr(self, 'ui_reference'):  # Check if UI reference exists
            print(f"Updating bracelet {bracelet_num}")
            self.ui_reference.on_data_change(bracelet_num)

    def toggle_head_injury(self):
        self.obs_bracelet.toggle_is_head_injured()

    def run(self):
        """Main control loop for the ControlUnit based on the current mode."""
        while not self.terminate:
            if self.mode == Modes.STATESTREAM:
                self.sound_pulse_and_saturation()
            else:
                self.notice_only()
