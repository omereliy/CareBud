import pandas as pd
from datetime import datetime
from configs import config_constants
from configs.enums import Vitals
from logic_layer.patient.receiver import get_sensor_data_via_usb_port, simulate_states
import pyttsx3


class Bracelet:
    """
        Represents a bracelet device that monitors a patient's vitals, including
        saturation, pulse, and blood pressure. Each bracelet maintains a record
        of these metrics over time.

        Attributes:
            saturation (int): Oxygen saturation level (0-100%).
            pulse (int): Pulse rate.
            blood_pressure (tuple): Blood pressure in (systolic, diastolic) format.
            num (int): The ID number of the bracelet.
            record (dict): A dictionary tracking historical data of vitals.
        """
    saturation: int = 0  # 0-100 in percentage
    pulse: int = 0
    blood_pressure: tuple = (0, 0)
    num: int
    record: dict[any, list] = dict()
    is_head_injured: bool = False

    def __init__(self, num: int, saturation: int, pulse: int, blood_pressure: tuple):
        """
        Initializes a Bracelet with a given ID, saturation, pulse, and blood pressure.

        Args:
            num (int): The ID number of the bracelet.
            saturation (int): Initial oxygen saturation level.
            pulse (int): Initial pulse rate.
            blood_pressure (tuple): Initial blood pressure (systolic, diastolic).
        """
        self.saturation = saturation
        self.pulse = pulse
        self.blood_pressure = blood_pressure
        self.num = num
        self.is_head_injured = False
        self.record = {"time": [],
                       Vitals.PULSE: [],
                       Vitals.BLOODPRESSURE: [],
                       Vitals.SATURATION: []
                       }
        self._listeners = []

    def get_state(self):
        """Returns the current vitals state as a dictionary."""
        return {Vitals.PULSE: self.pulse,
                Vitals.SATURATION: self.saturation,
                Vitals.BLOODPRESSURE: self.blood_pressure}

    def set_state(self, state: dict[Vitals, any]):
        """
         Sets the bracelet's vitals to new values and updates the record.

         Args:
             state (dict): New values for Vitals.
         """
        self.saturation = state[Vitals.SATURATION]
        self.blood_pressure = state[Vitals.BLOODPRESSURE]
        self.pulse = state[Vitals.PULSE]
        self.update_record()
        self.notify_listeners()

    def get_color(self):
        """Returns the health status color based on current vitals."""
        return config_constants.state_to_color(self.get_state(), self.is_head_injured)

    def alert_if_critical(self):
        """
        collects
        :return:
        """
        to_alert = False
        warning = f"warning on patient {self.num + 1}, "

        if not config_constants.is_pulse_ok(state=self.get_state()):
            warning += "check pulse"
            to_alert = True
        if not config_constants.is_blood_pressure_ok(self.get_state(), self.is_head_injured):
            if to_alert:
                warning += "and blood pressure"
            else:
                to_alert = True
                warning += "check blood pressure"
        if to_alert:
            engine = pyttsx3.init()
            engine.setProperty("rate", 150)
            engine.say(warning)
            engine.runAndWait()

    def get_record(self):
        """Returns a DataFrame containing the bracelet's historical data."""
        d = {k.value if isinstance(k, Vitals) else k: v for k, v in self.record.items()}
        return pd.DataFrame(d)

    def update_record(self):
        """Updates the bracelet's record with the current vitals and timestamp."""
        current_time = datetime.now()
        self.record["time"].append(current_time)
        self.record[Vitals.PULSE].append(self.pulse)
        self.record[Vitals.BLOODPRESSURE].append(self.blood_pressure)
        self.record[Vitals.SATURATION].append(self.saturation)

    def toggle_is_head_injured(self):
        """
        changes the value of is_head_injured to its opposite
        :return:
        """
        self.is_head_injured = not self.is_head_injured

    def add_listener(self, listener):
        """Register a new listener function to be notified when the state changes."""
        self._listeners.append(listener)

    def notify_listeners(self):
        """Call all registered listener functions when the state changes."""
        print(f"Notifying listeners for Bracelet {self.num}")
        for listener in self._listeners:
            listener(self.num)  # Notify with bracelet number as an identifier

    def __str__(self):
        """Returns a string representation of the bracelet's current vitals."""
        return (
            f"{Vitals.BLOODPRESSURE.value}: {self.blood_pressure}"
            f"{Vitals.PULSE.value}: {self.pulse}"
            f"{Vitals.SATURATION.value}: {self.saturation}")

    def run(self, is_simulation, channel: str, is_critical: bool):
        """

        :param is_critical: states if the patient is critical in simulation
        :param is_simulation: states if the bracelet's current vitals are simulated
        :param channel: the channel/port of the receiver
        :return:
        """
        if is_simulation:
            simulate_states(self, is_critical)
        else:
            get_sensor_data_via_usb_port(self, channel)


