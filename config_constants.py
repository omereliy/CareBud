from enums import *

bracelet_index_range = range(0, 1)

# ======================== start- medical values =============================
min_saturation = 0
max_saturation = 100

# TODO set values to actual values' they are arbitrary for now

low_critical_saturation = 50
high_critical_saturation = 100
low_good_saturation = 75
high_good_saturation = 100

low_critical_blood_pressure = (50, 5)
high_critical_blood_pressure = (100, 100)
low_good_blood_pressure = (100, 100)
high_good_blood_pressure = (100, 100)

low_critical_pulse = 20
high_critical_pulse = 180
low_good_pulse = 60
high_good_pulse = 120


# ======================== end- medical values =================================
def is_critical_state(state: dict) -> bool:
    return (high_critical_blood_pressure < state[Vitals.BLOODPRESSURE]
            or low_critical_blood_pressure > state[Vitals.BLOODPRESSURE]
            or high_critical_pulse < state[Vitals.PULSE]
            or low_critical_pulse > state[Vitals.PULSE]
            or high_critical_saturation < state[Vitals.SATURATION]
            or low_critical_saturation > state[Vitals.SATURATION])


def is_good_state(state: dict) -> bool:
    return (high_critical_blood_pressure > state[Vitals.BLOODPRESSURE] > low_critical_blood_pressure
            and high_critical_pulse > state[Vitals.PULSE] > low_critical_pulse
            and high_critical_saturation > state[Vitals.SATURATION] > low_critical_saturation)


def state_to_color(state: dict):
    if is_good_state(state):
        return Colors.GREEN
    elif is_critical_state(state):
        return Colors.RED
    else:
        return Colors.ORANGE
