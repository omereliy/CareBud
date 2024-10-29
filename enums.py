from enum import Enum

saturation: float = 0  # 0-100 in percentage
pulse: int = 0
blood_pressure_example: tuple = (0, 0)


class Vitals(Enum):
    SATURATION = "saturation"
    PULSE = "pulse"
    BLOODPRESSURE = "blood pressure"


class Modes(Enum):
    NOTICEONLY = "notice only"
    STATESTREAM = "state stream"


class Colors(Enum):
    GREEN = "green"
    RED = "red"
    ORANGE = "orange"
