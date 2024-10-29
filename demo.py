import pyttsx3

engine = pyttsx3.init()
# engine.say("I will speak this text")
# engine.runAndWait()

saturation: float = 0  # 0-100 in percentage
pulse: int = 0
blood_pressure_example: tuple = (0, 0)


def blood_pressure_to_sentence(blood_pressure: tuple):
    return f"{blood_pressure[0]} on {blood_pressure[1]}"


def read_stats():
    engine.say(f"saturation is {saturation}")
    engine.runAndWait()
    engine.say(f"pulse is {pulse}")
    engine.runAndWait()
    engine.say(f"blood pressure is {blood_pressure_to_sentence(blood_pressure_example)}")
    engine.runAndWait()


# read_stats()


import pandas as pd

# Sample data for bracelets; you can replace this with your actual data
data = {
    "time": ["08:00", "08:30", "09:00", "09:30"],
    "pulse": [72, 75, 78, 76],
    "blood_pressure": ["120/80", "118/78", "122/81", "119/79"],
    "saturation": [98, 97, 96, 98]
}

# Create a DataFrame for bracelet data
bracelet_df = pd.DataFrame(data)

# Display the table
print(bracelet_df)