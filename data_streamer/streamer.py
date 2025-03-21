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
from abc import ABC, abstractmethod
from data_streamer.LoopStrategy import LoopStrategyFactory

class StreamerThread(threading.Thread):
    
    def __init__(self, output_path:str, board_type:brainflow.BoardIds):
        threading.Thread.__init__(self, daemon=True)
        self.continue_streaming = True

        self.multithread_blink_value = multiprocessing.Value('i', -44)
        self.blink_register_app_thread = blink_register_thread.BlinkRegisterThread(
            output_path=output_path,
            multithread_blink_value=self.multithread_blink_value,
        )
        self.blink_register_app_thread.start()
        self.streamer = Streamer(output_path, self.multithread_blink_value, board_type)
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
    
    def __init__(self, output_path:str, multithread_blink_value:int, board_type:brainflow.BoardIds):
        self.SERIAL_PORT = "/dev/ttyUSB0" if os.name == Streamer.OS.LINUX.value else "COM3"  # Could also be : COM5, COM3, COM7 on Windows
        self.BOARD_ID = board_type
        self.board = self.create_boardshim()
        self.strategy = LoopStrategyFactory.create_strategy(board_type)
        self.output_path = output_path
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
        self.strategy.before_loop(self.output_path)
        if self.board.is_prepared():
            self.board.release_all_sessions()
        self.board.prepare_session()
        self.board.start_stream()
    
    def whipe_clean(self):
        keyboard.unhook_all()
    
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
        number_of_data = self.board.get_board_data_count()
        if(number_of_data > 0):
            gt_to_append = self.get_if_input()
            self.strategy.stream_loop(self.board, output_path=self.output_path, gt_to_append=gt_to_append)
            

     

            
