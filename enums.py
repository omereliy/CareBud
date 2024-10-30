from enum import Enum


class Vitals(Enum):
    """Enum for types of vitals measured by the bracelet."""
    SATURATION = "saturation"
    PULSE = "pulse"
    BLOODPRESSURE = "blood pressure"


class Modes(Enum):
    """Enum for ControlUnit modes."""
    NOTICEONLY = "notice only"
    STATESTREAM = "state stream"


class Colors(Enum):
    """Enum for health status color indicators."""
    GREEN = "green"
    RED = "red"
    ORANGE = "orange"
