from abc import ABC, abstractmethod
import brainflow
import numpy as np
import pandas as pd
import os

class LoopStrategy(ABC):
    
    def __init__(self, file_prefix = ""):
        self.file_prefix = file_prefix
    
    @abstractmethod
    def before_loop(self, output_path:str):
        pass
    
    @abstractmethod
    def stream_loop(self, board:brainflow.BoardShim, output_path:str, gt_to_append:int):
        pass
    
    def save_header(self, header:pd.DataFrame, output_path:str):
        if not os.path.exists(output_path):
            header[:0].to_csv(output_path + self.file_prefix + ".csv", index=False)
    
    def append_data(self, df:pd.DataFrame, output_path:str):
        df.to_csv(output_path + self.file_prefix + ".csv", mode="a", index=False, header=False)


class LoopStrategyCyton(LoopStrategy):
    
    def __init__(self):
        super().__init__("_cyton")
    
    def before_loop(self, output_path:str):
        # Noms électrodes 10-20 (Cyton 8 canaux)
        header = pd.DataFrame({
            'index': [],
            'FP1': [], 'FP2': [], 'F7': [], 'F8': [],
            'FZ': [], 'CZ': [], 'O1': [], 'O2': [],
            'accelerometer_x' : [], 'accelerometer_y' : [], 'accelerometer_z' : [],
            'empty1': [], 
            'digital_channel_0' : [],'digital_channel_1' : [],'digital_channel_2' : [],'digital_channel_3' : [],
            'empty2': [], 
            'digital_channel_4' : [],
            'analog_channel_0': [], 'analog_channel_1': [], 'analog_channel_2': [],
            'timestamp' : [],
            'marker_channel' : [],
            'our_gt_channel' : [],
        })
        self.save_header(header, output_path)

    def stream_loop(self, board:brainflow.BoardShim, output_path:str, gt_to_append:int):
        data = board.get_board_data()
        amount_of_row_of_data = data.shape[1]
        new_rows_of_gt = np.full((1, data.shape[1]), gt_to_append)
        data_annotated = np.vstack([data, new_rows_of_gt])

        NORMAL_SHAPE_OF_DATA_ANNOTATED = (25,amount_of_row_of_data)
        if(data_annotated.shape != NORMAL_SHAPE_OF_DATA_ANNOTATED):
            return
        
        data_transposed = np.transpose(data_annotated)    
        df = pd.DataFrame(data_transposed)
        self.append_data(df, output_path)


class LoopStrategyCytonDaisy(LoopStrategy):
    
    def __init__(self):
        super().__init__("_cyton_daisy")
    
    def before_loop(self, output_path:str):
        # Noms électrodes 10-20 (Cyton 8 + Daisy 8 canaux)
        header = pd.DataFrame({
            'index': [],
            'FP1': [], 'FP2': [], 'F7': [], 'F8': [],
            'FZ': [], 'CZ': [], 'O1': [], 'O2': [],
            'F3': [], 'F4': [], 'T3': [], 'T4': [],
            'T5': [], 'T6': [], 'P3': [], 'P4': [],
            'accelerometer_x' : [], 'accelerometer_y' : [], 'accelerometer_z' : [],
            'empty1': [], 
            'digital_channel_0' : [],'digital_channel_1' : [],'digital_channel_2' : [],'digital_channel_3' : [],
            'empty2': [], 
            'digital_channel_4' : [],
            'analog_channel_0': [], 'analog_channel_1': [], 'analog_channel_2': [],
            'timestamp' : [],
            'marker_channel' : [],
            'our_gt_channel' : [],
        })
        self.save_header(header, output_path)
    
    def stream_loop(self, board:brainflow.BoardShim, output_path:str, gt_to_append:int):
        data = board.get_board_data()
        amount_of_row_of_data = data.shape[1]
        new_rows_of_gt = np.full((1, data.shape[1]), gt_to_append)
        data_annotated = np.vstack([data, new_rows_of_gt])

        NORMAL_SHAPE_OF_DATA_ANNOTATED = (33,amount_of_row_of_data)
        if(data_annotated.shape != NORMAL_SHAPE_OF_DATA_ANNOTATED):
            return
        
        data_transposed = np.transpose(data_annotated)    
        df = pd.DataFrame(data_transposed)
        self.append_data(df, output_path)


class InvalidBoardTypeException(Exception):
    pass


class LoopStrategyFactory:
    @staticmethod
    def create_strategy(board_type: brainflow.BoardIds) -> LoopStrategy:
        if(board_type == brainflow.BoardIds.CYTON_BOARD):
            return LoopStrategyCyton()
        elif(board_type == brainflow.BoardIds.CYTON_DAISY_BOARD):
            return LoopStrategyCytonDaisy()
        else:
            raise InvalidBoardTypeException("Board type is not handled by the Datasaver")