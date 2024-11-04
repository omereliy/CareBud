from configs.enums import Vitals, Colors, Modes

bracelet_index_range = range(0, 6)

# ======================== start- medical values =============================
min_saturation = 0
max_saturation = 100

low_bound_blood_pressure = 90
high_bound_blood_pressure = 170
low_bound_head_injury_blood_pressure = 140

low_bound_pulse = 40
high_bound_pulse = 200


# ======================== end- medical values =================================

def is_pulse_ok(state: dict) -> bool:
    return low_bound_pulse <= state[Vitals.PULSE] <= high_bound_pulse


def is_blood_pressure_ok(state: dict, is_head_injured: bool) -> bool:
    if is_head_injured:
        return low_bound_head_injury_blood_pressure <= state[Vitals.BLOODPRESSURE][0] <= high_bound_blood_pressure
    else:
        return low_bound_blood_pressure <= state[Vitals.BLOODPRESSURE][0] <= high_bound_blood_pressure


def is_good_state(state: dict, is_head_injured: bool) -> bool:
    """
    Checks if the given state represents a good (healthy) condition based on the threshold values
    defined in config_constants.py.

    Args:
        state (dict): A dictionary containing the current vitals with keys as Vitals enums.
        is_head_injured: is the patient suffering from, head injury

    """
    return is_pulse_ok(state) and is_blood_pressure_ok(state, is_head_injured)


def state_to_color(state: dict, is_head_injured: bool):
    """Maps the vitals state to a color indicator."""
    if is_good_state(state, is_head_injured):
        return Colors.GREEN
    else:
        return Colors.RED
