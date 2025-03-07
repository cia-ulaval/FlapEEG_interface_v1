from enum import Enum
import brainflow
import os
from data_streamer.streamer import Streamer
import numpy as np
import pickle as pk
import pandas as pd


class ModelInference(Streamer):
    
    def __init__(self, output_path, multithread_blink_value, sampling_rate = 125):
        super().__init__(output_path, multithread_blink_value, sampling_rate)
        with open('./EEG-CIA/blink_model.pkl', 'rb') as f:
            self.model = pk.load(f)
        
    def stream_loop(self):
        data = self.board.get_current_board_data(1)

        if data.shape == (32, 0):
            return
                
                
        data_transposed = np.transpose(data)
        df = pd.DataFrame(data_transposed)
        df = df.iloc[:,[1,2]]
        df.columns = ['FP1', 'FP2']
        result = self.model.predict(df)
        print(result)

        
        
