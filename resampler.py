import numpy as np
import resampy


def resample(input_rate, target_rate, raw_data):
    data = np.frombuffer(raw_data, dtype=np.int16)
    y_low = resampy.resample(data, input_rate, target_rate)

    return y_low.tobytes()
