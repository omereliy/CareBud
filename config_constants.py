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
    """Checks if the given state represents a critical condition."""
    # Comparison logic based on threshold values

def is_good_state(state: dict) -> bool:
    """Checks if the given state represents a good (healthy) condition."""
    # Comparison logic based on threshold values

def state_to_color(state: dict):
    """Maps the vitals state to a color indicator."""
    if is_good_state(state):
        return Colors.GREEN
    elif is_critical_state(state):
        return Colors.RED
    else:
        return Colors.ORANGE
