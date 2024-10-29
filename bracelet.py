from vitals import Vitals


class Bracelet:
    saturation: int = 0  # 0-100 in percentage
    pulse: int = 0
    blood_pressure: tuple = (0, 0)
    num: int
    record: dict[str, list] = {"time": [],
                               "pulse": [],
                               "blood pressure": [],
                               "saturation": []
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

    def __str__(self):
        return (
            f"blood pressure: {self.blood_pressure}"
            f"pulse: {self.pulse}"
            f"saturation: {self.saturation}")
