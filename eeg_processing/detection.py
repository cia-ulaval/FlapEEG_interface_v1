import numpy as np
from eeg_processing.filtering import butter_lowpass_filter

BLINK_THRESHOLD = 200  # MIGHT NEED TO UPDATE THIS VALUE

def detect_blink(data):
    """Detects a blink in the EEG signal by analyzing amplitudes."""
    if data is None:
        return False
    
    eeg_channel = data[1] 
    filtered_signal = butter_lowpass_filter(eeg_channel)

    return np.max(filtered_signal) > BLINK_THRESHOLD
