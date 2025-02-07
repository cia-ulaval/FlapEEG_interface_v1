import brainflow
from enum import Enum
import time
import os
import threading
import pandas as pd
import numpy as np

class StreamerThread(threading.Thread):
    
    def __init__(self, output_path:str):
        threading.Thread.__init__(self, daemon=True)
        self.continue_streaming = True
        self.streamer = Streamer(output_path)

        self.streamer.log_info(f"Saving data to : {output_path}")
        
    def run(self):
        self.streamer.log_info("Creating the Streamer")
        self.streamer.start_streaming()
        self.streamer.log_info("Streamer started")
        while self.continue_streaming:
            self.streamer.stream_loop()
        self.streamer.log_info("Streamer thread stopped")
            
    def stop(self):
        self.continue_streaming = False
        
        
class Streamer:
    class OS(Enum):
        WINDOWS = "nt"
        LINUX = "posix"
    
    def __init__(self, output_path:str):
        self.SERIAL_PORT = "/dev/ttyUSB0" if os.name == Streamer.OS.LINUX.value else "COM3" 
        self.BOARD_ID = brainflow.board_shim.BoardIds.CYTON_DAISY_BOARD
        self.board = self.create_boardshim()
        self.output_path = output_path
    
    def log_info(self, message:str):
        print(f"->STREAMER-INFO : {message}")
    def log_warning(self, message:str):
        print(f"->STREAMER-WARNING : {message}")
    def log_error(self, message:str):
        print(f"->STREAMER-ERROR : {message}")
        
    def create_boardshim(self)->brainflow.BoardShim:

        params = brainflow.BrainFlowInputParams()
        params.serial_port = self.SERIAL_PORT
        return brainflow.BoardShim(self.BOARD_ID, params)    
    
    def start_streaming(self):
        
        if self.board.is_prepared():
            self.board.release_all_sessions()
        self.board.prepare_session()
        self.board.start_stream()
        
    def stream_loop(self):
        data = self.board.get_current_board_data(1)
        df = pd.DataFrame(np.transpose(data))
        df.to_csv(self.output_path, mode="a", index=False, header=False)
        time.sleep(1)
            
