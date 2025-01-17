import brainflow
import typing
import time
import numpy as np
import brainflow.board_shim
import matplotlib.pyplot as plt

TIMEOUT = 0
IP_PORT = 5000
IP_ADRESS = '127.0.0.1'
BOARD_ID = brainflow.board_shim.BoardIds.CYTON_DAISY_BOARD

MASTER_BOARD = brainflow.BoardIds.NO_BOARD

def create_boardshim()->brainflow.BoardShim:
    params = brainflow.BrainFlowInputParams()
    params.ip_port = IP_PORT
    params.ip_address = IP_ADRESS
    params.timeout = TIMEOUT
    params.serial_port = "/dev/ttyUSB0"
    return brainflow.BoardShim(BOARD_ID, params)

def print_mean_value(board: brainflow.BoardShim):
    data = board.get_board_data()
    print("Data collected: ", data)
    
    eeg_channels = brainflow.BoardShim.get_ecg_channels(BOARD_ID)
    for channel in eeg_channels:
        mean_value = np.mean(data[channel])
        print(f"Mean value for EEG channel {channel}: {mean_value}")



def main():
    
    print("Creating board")
    board = create_boardshim()
    print("Preparing the session")
    board.prepare_session()
    print("Starting the stream")
    board.start_stream()
    time.sleep(10)
    print("Stopping the stream")
    board.stop_stream()

    print_mean_value(board)

if __name__ == "__main__":
    main()