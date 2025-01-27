import cv2
import numpy as np
from mss import mss

def screen_recorder(output_file, frame_rate=60.0, resolution=(1920, 1080)):
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(output_file, fourcc, frame_rate, resolution)

    # Define the screen capture region
    sct = mss()
    monitor = {"top": 0, "left": 0, "width": resolution[0], "height": resolution[1]}

    print("Recording started. Press 'q' to stop.")

    try:
        while True:
            # Capture the screen
            screenshot = sct.grab(monitor)
            # Convert to a numpy array
            frame = np.array(screenshot)
            # Convert BGRA to BGR (for OpenCV compatibility)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            # Write the frame to the output file
            out.write(frame)
            # Display the recording screen
            cv2.imshow("Recording Screen", frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("\nRecording stopped manually.")

    # Release resources
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    output_file = "screen_recording.avi"
    screen_recorder(output_file)
