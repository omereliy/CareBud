from enum import Enum

saturation: float = 0  # 0-100 in percentage
pulse: int = 0
blood_pressure_example: tuple = (0, 0)


class Vitals(Enum):
    SATURATION = "saturation"
    PULSE = "pulse"
    BLOODPRESSURE = "blood pressure"


