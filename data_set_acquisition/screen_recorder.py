import cv2
import numpy as np
from mss import mss
from datetime import datetime

def screen_recorder(base_filename="session", frame_rate=60.0, resolution=(1920, 1080), stop_event=None):
    # Generating files for each recording
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{base_filename}_{timestamp}.mp4"

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_file, fourcc, frame_rate, resolution)

    # Define the screen capture region
    sct = mss()
    monitor = {"top": 0, "left": 0, "width": resolution[0], "height": resolution[1]}

    try:
        while not stop_event.is_set():  # Check if the stop event is triggered
            # Capture the screen
            screenshot = sct.grab(monitor)
            # Convert to a numpy array
            frame = np.array(screenshot)
            # Convert BGRA to BGR (for OpenCV compatibility)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            # Write the frame to the output file
            out.write(frame)

    except Exception as e:
        print(f"Error during recording: {e}")

    # Release resources
    out.release()
    print("Recording stopped.")
