import pandas as pd
import numpy as np

def get_dummy_bio_sensor_data():
    # Generate dummy sport activity data (steps per day for the last month)
    dates = pd.date_range(end=pd.Timestamp.now(), periods=30)
    sport_activity = np.random.randint(1000, 10000, size=(30,))

    # Generate dummy heart beat history (average beats per minute each day for the last month)
    heart_beat_history = np.random.randint(60, 100, size=(30,))

    # Generate dummy sleep data (hours of sleep per day for the last month)
    sleep_data = np.random.uniform(4, 9, size=(30,))

    # Create DataFrame
    data = {
        'sport_activity': pd.Series(sport_activity, index=dates),
        'heart_beat_history': pd.Series(heart_beat_history, index=dates),
        'sleep_data': pd.Series(sleep_data, index=dates)
    }

    return data
