import pandas as pd
from datetime import datetime, timedelta
import config_constants
from enums import Vitals


class Bracelet:
    saturation: int = 0  # 0-100 in percentage
    pulse: int = 0
    blood_pressure: tuple = (0, 0)
    num: int
    record: dict[str, list] = {"time": [],
                               Vitals.PULSE: [],
                               Vitals.BLOODPRESSURE: [],
                               Vitals.SATURATION: []
                               }

    def __init__(self, num: int, saturation: int, pulse: int, blood_pressure: tuple):
        self.saturation = saturation
        self.pulse = pulse
        self.blood_pressure = blood_pressure
        self.num = num

    def get_state(self):
        return {Vitals.PULSE: self.pulse,
                Vitals.SATURATION: self.saturation,
                Vitals.BLOODPRESSURE: self.blood_pressure}

    def set_state(self, state: dict[Vitals, any]):
        self.saturation = state[Vitals.SATURATION]
        self.blood_pressure = state[Vitals.BLOODPRESSURE]
        self.pulse = state[Vitals.PULSE]
        self.update_record()

    def get_color(self):
        return config_constants.state_to_color(self.get_state())

    def get_record(self):
        d = {k.value if isinstance(k, Vitals) else k: v for k, v in self.record.items()}
        return pd.DataFrame(d)

    def update_record(self):
        current_time = datetime.now()
        self.record["time"].append(current_time)
        self.record["Vitals.PULSE"].append(self.pulse)
        self.record["Vitals.SATURATION"].append(self.saturation)

    def __str__(self):
        return (
            f"{Vitals.BLOODPRESSURE.value}: {self.blood_pressure}"
            f"{Vitals.PULSE.value}: {self.pulse}"
            f"{Vitals.SATURATION.value}: {self.saturation}")
