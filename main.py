from eeg_processing.acquisition import start_eeg_stream, get_eeg_data
from eeg_processing.detection import detect_blink
from game_control.flappy_control import jump

import time

# Initialisation of the EEG stream
board = start_eeg_stream()

print("Detecting blinks...")

try:
    while True:
        data = get_eeg_data(board)
        if detect_blink(data):
            jump()
            time.sleep(0.3)  # Avoids multiple jumps

except KeyboardInterrupt:
    print("Program stopped by the user.")
    board.stop_stream()
    board.release_session()
