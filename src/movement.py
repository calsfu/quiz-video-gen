import numpy as np

def bounce_y(duration, center_y, freq=2, amplitude=50):
    # This formula creates a sine wave bounce
    return center_y + amplitude * np.sin(freq * np.pi * duration)