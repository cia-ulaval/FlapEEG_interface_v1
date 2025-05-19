"""Install with pip install scipy."""
from scipy.signal import butter, lfilter

def butter_lowpass_filter(data, cutoff=5, fs=250, order=3):
    """Filters the data with a low-pass Butterworth"""
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return lfilter(b, a, data)
