import numpy as np
from eeg_processing.filtering import butter_lowpass_filter

BLINK_THRESHOLD_OVER_CIRCULAR_BUFFER = 2 # MIGHT NEED TO UPDATE THIS VALUE

CIRCULAR_BUFFER = [25] * 800
CIRCULAR_BUFFER_SIZE = 800

def add_element_to_circular_buffer(value):
    if len(CIRCULAR_BUFFER) < CIRCULAR_BUFFER_SIZE:
        CIRCULAR_BUFFER.append(value)
    else:
        CIRCULAR_BUFFER.pop()
        CIRCULAR_BUFFER.insert(0, value)

def get_circular_buffer_average():
    valeur = np.mean(CIRCULAR_BUFFER)
    if valeur < 25:
         return 25
    else:
         return valeur

def detect_blink(data):
    """Detects a blink in the EEG signal by analyzing amplitudes."""
    if data is None:
        return False
    
    filtered_signal = data 
    filtered_signal = np.absolute(filtered_signal[:2])
    max_signal = np.max(filtered_signal)
    threshold = get_circular_buffer_average() * BLINK_THRESHOLD_OVER_CIRCULAR_BUFFER
    print(f"buffer average : {get_circular_buffer_average()}")
    
    if max_signal > threshold:
            print(f"jumped! : {max_signal}")
    if max_signal < 100:
        add_element_to_circular_buffer(max_signal)
    

    return max_signal > threshold
