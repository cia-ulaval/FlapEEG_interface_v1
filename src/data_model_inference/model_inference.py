from enum import Enum
import brainflow
import os
from data_streamer.streamer import Streamer
import numpy as np
import pickle as pk
import pandas as pd

NUM_EEG_CHANNELS = 16


class ModelInference(Streamer):
    
    def __init__(self, output_path, multithread_blink_value, board_type=brainflow.BoardIds.CYTON_DAISY_BOARD):
        super().__init__(output_path, multithread_blink_value, board_type)
        with open('./EEG-CIA/blink_model.pkl', 'rb') as f:
            self.model = pk.load(f)
        
    def stream_loop(self):
        data = self.board.get_current_board_data(1)

        if data.shape[1] == 0:
            return

        data_transposed = np.transpose(data)
        df = pd.DataFrame(data_transposed)
        df = df.iloc[:, list(range(1, NUM_EEG_CHANNELS + 1))]
        df.columns = [f'ch{i}' for i in range(1, NUM_EEG_CHANNELS + 1)]
        result = self.model.predict(df)
        print(result)

        
        
