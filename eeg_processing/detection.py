import numpy as np
from eeg_processing.filtering import butter_lowpass_filter

BLINK_THRESHOLD = 75  # MIGHT NEED TO UPDATE THIS VALUE



def detect_blink(data):
    """Detects a blink in the EEG signal by analyzing amplitudes."""
    if data is None:
        return False
    
    filtered_signal = data 
    # filtered_signal = butter_lowpass_filter(eeg_channel)
    # print(f"Detecting signals : {filtered_signal}")
    filtered_signal = np.absolute(filtered_signal[:2])
    print(f"{np.max(filtered_signal)} ")
    return np.max(filtered_signal) > BLINK_THRESHOLD
