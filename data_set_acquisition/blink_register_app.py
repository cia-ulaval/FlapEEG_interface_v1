import cv2
import numpy as np
from mss import mss
from datetime import datetime
import pygame
import random
import threading
from threading import Event
import sys
import os
import keyboard
import multiprocessing

class BlinkRegisterApp:
    def __init__(self, output_path, multithread_blink_value):
        self.isRunning=True
        self.output_path = output_path
        self.PATH_TO_ASSETS = os.path.join("data_set_acquisition", "asset")
        self.multithread_blink_value = multithread_blink_value
    
    def stop(self):
        self.isRunning=False
        
    def start(self):
        self.main()
        
    def gt_true(self):
        self.multithread_blink_value.value = 44
        
    def gt_false(self):
        self.multithread_blink_value.value = -44
    
    def log_info(self, message:str):
        print(f"->->BLINK-TASK-INFO : {message}")
    def log_warning(self, message:str):
        print(f"->->BLINK-TASK-WARNING  : {message}")
    def log_error(self, message:str):
        print(f"->->BLINK-TASK-ERROR  : {message}")
        
    ###############################################################################
    # 1) SCREEN RECORDER
    ###############################################################################
    def screen_recorder(
            self,
            base_filename="session",
            frame_rate=30.0,
            stop_event=None
    ):
        """
        Captures the entire primary monitor at 'frame_rate' FPS until 'stop_event' is set.
        Saves the output to an MP4 file with a timestamp in the name.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{self.output_path}.mp4"

        # Use MSS to capture full screen
        with mss() as sct:
            # For the entire primary monitor, use monitors[1].
            # For the entire virtual screen (all monitors), use monitors[0].
            monitor = sct.monitors[1]
            mon_width = monitor["width"]
            mon_height = monitor["height"]

            # Define codec and VideoWriter using the actual screen size
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(output_file, fourcc, frame_rate, (mon_width, mon_height))

            try:
                while not stop_event.is_set():
                    screenshot = sct.grab(monitor)
                    frame = np.array(screenshot)
                    # Convert BGRA to BGR
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                    out.write(frame)

            except Exception as e:
                print(f"Error during screen recording: {e}")
            finally:
                out.release()
                print("Screen recording stopped.")

    ###############################################################################
    # 2) HELPER FUNCTIONS
    ###############################################################################
    def display_timer(self, screen, font, start_time):
        """
        Displays an elapsed-seconds timer in the top-left corner of the screen.
        """
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        timer_text = f"{elapsed_time}s"
        timer_surface = font.render(timer_text, True, (255, 255, 255))  # White text
        screen.blit(timer_surface, (10, 10))


    def convert_cv2_frame_to_pygame_surface(self, cv2_frame):
        """
        Converts an OpenCV (BGR) frame to a pygame.Surface (RGB).
        """
        # Convert BGR -> RGB
        cv2_frame_rgb = cv2.cvtColor(cv2_frame, cv2.COLOR_BGR2RGB)
        # Get shape (height, width, channels)
        height, width, _ = cv2_frame_rgb.shape
        # Convert to bytes
        frame_data = cv2_frame_rgb.tobytes()
        # Create pygame surface
        surface = pygame.image.frombuffer(frame_data, (width, height), 'RGB')
        return surface


    ###############################################################################
    # 3) MAIN APP
    ###############################################################################

    def main(self):
        

                
        import sys





        pygame.init()
        # ------------------------- SETUP WINDOW -----------------------------------
        # Start in fullscreen at the display's native resolution
        screen = pygame.display.set_mode((800,600))
        pygame.display.set_caption("EEG Blink Task")


        # ------------------------- SETUP SCREEN RECORDER THREAD -------------------
        stop_event = Event()
        recorder_thread = threading.Thread(
            target=self.screen_recorder,
            args=("game_session", 30.0, stop_event)
        )
        recorder_thread.start()

        # ------------------------- SETUP WEBCAM -----------------------------------
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not access the webcam.")
            # We won't exit entirely so you can still run the game logic.

        # ------------------------- DETERMINE WINDOW SIZE --------------------------
        # Now that we've created a fullscreen display, let's ask Pygame
        # for the actual width/height in case we need them.
        WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()

        # ------------------------- LOAD ASSETS ------------------------------------
        background = pygame.image.load(os.path.join(self.PATH_TO_ASSETS, "bg.png"))
        background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        flapEEG = pygame.image.load(os.path.join(self.PATH_TO_ASSETS,"brainMidFlap.png"))
        flapEEG = pygame.transform.scale(flapEEG, (150, 150))
        GRAY = (68, 68, 68)
        flapEEG.set_colorkey(GRAY)

        # ------------------------- FONTS & CLOCK ----------------------------------
        font = pygame.font.SysFont("comicsans", 30)
        clock = pygame.time.Clock()

        # ------------------------- TIMER SETUP ------------------------------------
        start_time = pygame.time.get_ticks()

        # ------------------------- BIRD TIMING ------------------------------------
        bird_display_duration = 1000  # ms
        next_bird_time = pygame.time.get_ticks() + random.randint(1000, 3000)
        bird_visible = False
        bird_end_time = 0
        bird_x, bird_y = 0, 0

        # ------------------------- MAIN LOOP --------------------------------------
        while self.isRunning:
            # 1) Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    elif event.key == pygame.K_f:
                        # Toggle fullscreen
                        if fullscreen:
                            # Switch to windowed mode (e.g., 1280x720)
                            screen = pygame.display.set_mode((1280, 720))
                            fullscreen = False
                        else:
                            # Switch back to fullscreen
                            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                            fullscreen = True

                        # Update window dimensions after toggling
                        WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
                        # Rescale background to match new window size
                        background = pygame.image.load("asset/bg.png")
                        background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

            # 2) Draw background
            screen.blit(background, (0, 0))

            # 3) Display timer
            self.display_timer(screen, font, start_time)

            # 4) Capture webcam frame and blit
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    # Resize to smaller, optional
                    frame = cv2.resize(frame, (320, 240))
                    frame = cv2.flip(frame, 1)
                    cam_surface = self.convert_cv2_frame_to_pygame_surface(frame)
                    screen.blit(cam_surface, (WINDOW_WIDTH - 320, 0))

            # 5) Bird logic
            now = pygame.time.get_ticks()
            if not bird_visible and now >= next_bird_time:
                bird_visible = True
                self.gt_true()
                
                bird_end_time = now + bird_display_duration
                # Random position
                bird_x = random.randint(0, WINDOW_WIDTH - flapEEG.get_width())
                bird_y = random.randint(0, WINDOW_HEIGHT - flapEEG.get_height())

            # If bird is visible, draw it until end time
            if bird_visible:
                screen.blit(flapEEG, (bird_x, bird_y))
                if now >= bird_end_time:
                    bird_visible = False
                    self.gt_false()
                    next_bird_time = now + random.randint(1000, 3000)

            # 6) Update display
            pygame.display.flip()

            # 7) Cap frame rate
            clock.tick(30)

        # ------------------------- SHUTDOWN ---------------------------------------
        print("Exiting game. Stopping screen recorder...")

        stop_event.set()
        recorder_thread.join()

        if cap.isOpened():
            cap.release()

        pygame.quit()
        sys.exit()


# -----------------------------------------------------------------------------
# Run the integrated app
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
