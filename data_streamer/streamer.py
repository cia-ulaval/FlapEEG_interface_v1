import brainflow
from enum import Enum
import time
import os
import threading
import keyboard
import pandas as pd
import numpy as np
import data_streamer.blink_register_thread as blink_register_thread
import multiprocessing

class StreamerThread(threading.Thread):
    
    def __init__(self, output_path:str, sampling_rate:float):
        threading.Thread.__init__(self, daemon=True)
        self.continue_streaming = True

        self.multithread_blink_value = multiprocessing.Value('i', -44)
        self.blink_register_app_thread = blink_register_thread.BlinkRegisterThread(
            output_path=output_path,
            multithread_blink_value=self.multithread_blink_value,
        )
        self.blink_register_app_thread.start()
        self.streamer = Streamer(output_path, self.multithread_blink_value, sampling_rate)
        self.streamer.log_info(f"Saving data to : {output_path}")
        self.streamer.log_info(f"Starting visual widget")
                                                     
        
    def run(self):
        self.streamer.log_info("Creating the Streamer")
        self.streamer.start_streaming()
        self.streamer.log_info("Streamer started")
        while self.continue_streaming:
            self.streamer.stream_loop()
        self.streamer.log_info("Streamer thread stopped")
    
    def stop(self):
        self.blink_register_app_thread.stop()
        self.continue_streaming = False
        self.streamer.whipe_clean()
        
        
class Streamer:
    class OS(Enum):
        WINDOWS = "nt"
        LINUX = "posix"
    
    def __init__(self, output_path:str, multithread_blink_value, sampling_rate:float = 125, ):
        self.SERIAL_PORT = "/dev/ttyUSB0" if os.name == Streamer.OS.LINUX.value else "COM3"  # Could also be : COM5, COM3, COM7 on Windows
        self.BOARD_ID = brainflow.board_shim.BoardIds.CYTON_DAISY_BOARD
        self.board = self.create_boardshim()
        self.output_path = output_path
        self.sampling_rate = sampling_rate
        self.multithread_blink_value = multithread_blink_value
        
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
    
    def whipe_clean(self):
        keyboard.unhook_all()
        
    def get_delta_time_from_sampling_rate(self):
        return 1. / self.sampling_rate
    
    def space_down(self):
        return 44

    def space_up(self):
        return -44
    
    def get_if_input(self) -> bool:
        if self.multithread_blink_value.value > 0:
            return self.space_down()
        else:
            return self.space_up()
    
    def stream_loop(self):
        data = self.board.get_current_board_data(1)
        gt_to_append = self.get_if_input()                    
        new_row = np.full((1, data.shape[1]), gt_to_append)
        data_annotated = np.vstack([data, new_row])

        NORMAL_SHAPE_OF_DATA_ANNOTATED = (33,1)
        if(data_annotated.shape != NORMAL_SHAPE_OF_DATA_ANNOTATED):
            return
        
        data_transposed = np.transpose(data_annotated)    
        df = pd.DataFrame(data_transposed)
        df.to_csv(self.output_path + ".csv", mode="a", index=False, header=False)
        time.sleep(self.get_delta_time_from_sampling_rate())        
        

            
