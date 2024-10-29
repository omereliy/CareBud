import datetime

import pandas as pd

from bracelet import Bracelet
from enum import Enum
import pyttsx3

bracelet_index_range = range(0, 10)


class Modes(Enum):
    NOTICEONLY = "notice only"
    STATESTREAM = "state stream"


def blood_pressure_to_sentence(blood_pressure: tuple):
    return f"{blood_pressure[0]} on {blood_pressure[1]}"


def read_bracelets_stats(self, bracelet: Bracelet):
    self.engine.say(f"saturation is {bracelet.saturation}")
    self.engine.runAndWait()
    self.engine.say(f"pulse is {bracelet.pulse}")
    self.engine.runAndWait()
    self.engine.say(f"blood pressure is {blood_pressure_to_sentence(
        bracelet.blood_pressure)}")
    self.engine.runAndWait()


def sound_pulse_and_saturation():
    exit_signal = False
    while not exit_signal:
        pass


def notice_only():
    exit_signal = False
    while not exit_signal:
        pass


class ControlUnit:
    engine = pyttsx3.init()
    paired_bracelets: list[Bracelet]
    mode: Modes
    observed_bracelet_index: int
    obs_bracelet: Bracelet
    terminate: bool = False
    record: list[dict[datetime.time,]]

    def __init__(self):
        self.paired_bracelets = [Bracelet(i, 0, 0, (0, 0)) for i in bracelet_index_range]
        self.mode = Modes.NOTICEONLY
        self.observed_bracelet_index = 0
        self.obs_bracelet = self.paired_bracelets[0]

    def set_observed_bracelet(self, observed_bracelet_index: int):
        self.obs_bracelet = self.paired_bracelets[observed_bracelet_index]
        self.observed_bracelet_index = observed_bracelet_index

    def increment_bracelet_index(self):
        self.set_observed_bracelet(self.observed_bracelet_index + 1)

    def decrement_bracelet_index(self):
        self.set_observed_bracelet(self.observed_bracelet_index - 1)

    def switch_mode(self):
        if self.mode == Modes.STATESTREAM:
            self.mode = self.mode.NOTICEONLY
        else:
            self.mode = self.mode.STATESTREAM

    def get_all_states(self) -> pd.DataFrame:
        df: dict[str, list] = \
            {"patient": [i for i in bracelet_index_range],
             "pulse": [None for _ in bracelet_index_range],
             "blood pressure": [None for _ in bracelet_index_range],
             "saturation": [None for _ in bracelet_index_range]}

        for bracelet in self.paired_bracelets:
            df["pulse"][bracelet.num] = bracelet.pulse
            df["saturation"][bracelet.num] = bracelet.saturation
            df["blood pressure"][bracelet.num] = bracelet.blood_pressure
        bracelet_df = pd.DataFrame(df)

        return bracelet_df

    def run(self):
        while not self.terminate:
            if self.mode == Modes.STATESTREAM:
                sound_pulse_and_saturation()
            else:
                notice_only()
