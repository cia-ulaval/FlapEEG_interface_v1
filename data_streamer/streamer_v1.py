import brainflow
import typing
import time
import numpy as np
import brainflow.board_shim
import matplotlib.pyplot as plt
import matplotlib.animation
import pandas as pd
import os
import glob
import datetime
import uuid
import time

SERIAL_PORT = "/dev/ttyUSB0"
# SERIAL_PORT = "COM3"
# SERIAL_PORT = "COM7" could be one of those if  

BOARD_ID = brainflow.board_shim.BoardIds.CYTON_DAISY_BOARD
MASTER_BOARD = brainflow.BoardIds.NO_BOARD
PLAYBACK_FOLDER_PATH = os.path.join("raw_recordings")
TOTAL_DATA_POINTS_TO_PRINT = 250
COLOR_CHANNELS = ["grey", "purple", "blue", "green", "yellow", "orange", "red", "brown"]

def create_boardshim()->brainflow.BoardShim:
    params = brainflow.BrainFlowInputParams()
    params.serial_port = "/dev/ttyUSB0"
    return brainflow.BoardShim(BOARD_ID, params)

def print_mean_value(board: brainflow.BoardShim):
    data = board.get_board_data()
    print("Data shape :", data.shape)
    print("Data collected: ", data)
    eeg_channels = brainflow.BoardShim.get_eeg_channels(BOARD_ID)
    for channel in eeg_channels:
        mean_value = np.mean(data[channel])
        print(f"Shape of {channel}: {data[channel].shape}")
        print(f"Mean value for EEG channel {channel}: {mean_value}")



def live_plotting_16_channels(board: brainflow.BoardShim):
    plt.style.use("fivethirtyeight")
    eeg_channels = brainflow.BoardShim.get_eeg_channels(BOARD_ID)
    
    # Create a figure
    fig = plt.figure()
    axes = []
    lines = []
    fig.suptitle("EEG live reading data")
    plt.subplots_adjust(hspace=0.5)
    
    # Create subplots for each EEG channel
    for i, channel in enumerate(eeg_channels):
        ax = fig.add_subplot(len(eeg_channels), 1, i + 1)
        ax.set_title(f"Channel {i+1}")
        
        line, = ax.plot([], [], lw=1, color=COLOR_CHANNELS[i%len(COLOR_CHANNELS)]) 
        axes.append(ax)
        lines.append(line)

    # Animate function
    def animate(i):
        data = board.get_current_board_data(250)
        for idx, channel in enumerate(eeg_channels):
            # print(range(data.shape[1]), data[channel])
            x_axis = range(data.shape[1])
            y_axis = data[channel]
            
            lines[idx].set_data(range(data.shape[1]), data[channel]) 
            axes[idx].set_xlim(min(x_axis), max(x_axis))
            axes[idx].set_ylim(min(y_axis) - 10, max(y_axis) + 10)
        return lines


    # Create animation
    ani = matplotlib.animation.FuncAnimation(
        fig, animate, interval=16, blit=True
    )
 
    plt.show()

def save_all_data_to_files(board: brainflow.BoardShim):
    formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
    current_uuid_string = str(uuid.uuid4())
    where_to_save = os.path.join(PLAYBACK_FOLDER_PATH, formatted_date + "-" + current_uuid_string + ".csv")
    all_data = board.get_board_data()
    print("Data saved shape : ", all_data.shape)
    brainflow.DataFilter.write_file(all_data, where_to_save, 'w')
    
    
def playback_recorded_data(file: str):
    print("###################################")
    print(f"STARTING PLAYBACK WITH FILE : {file}")
    print("###################################")
    file_path = os.path.join(PLAYBACK_FOLDER_PATH, file)
    restored_data = brainflow.DataFilter.read_file(file_path)
    eeg_channels = brainflow.BoardShim.get_eeg_channels(BOARD_ID)
    sample_rate = brainflow.BoardShim.get_sampling_rate(BOARD_ID)
    print("DATAFRAME SHAPE : ",  restored_data.shape) # usually (32, WIDTH)
    print("eeg_channels : ", eeg_channels)
    
    # We want to plot X datapoint, at time Y
    # 1. We have 125 datapoint per second -> 0.008s per datapoint
    # 2. We need a timer that count and on time Y, we need to cursor that position itself at that index and get the last X datapoints
    
    cursor_timer = time.time() # starting the timer
    time_per_tick = 1.0 / sample_rate
    max_tick = restored_data.shape[1] # the width of the data 
    
    print("Time per tick : ", time_per_tick)
    print("Max-tick : ", max_tick)
    # Plot the data
    plt.style.use("dark_background")
    # Create a figure
    fig = plt.figure()
    axes = []
    lines = []
    fig.suptitle("EEG playback data")
    plt.subplots_adjust(hspace=0.5)
    
    # Create subplots for each EEG channel
    for i, channel in enumerate(eeg_channels):
        ax = fig.add_subplot(len(eeg_channels), 1, i + 1)
        ax.set_title(f"Channel {i+1}")
        
        line, = ax.plot([], [], lw=1, color=COLOR_CHANNELS[i%len(COLOR_CHANNELS)]) 
        axes.append(ax)
        lines.append(line)

    # Animate function
    def animate(i):
        delta_time = time.time() - cursor_timer
        index_data_point = int(delta_time/time_per_tick)
        print("delta_time : ", delta_time)
        # Three cases : 
        # 1. The index_data_point < TOTAL_DATA_POINTS_TO_PRINT
        # 2. The index_data_point >= TOTAL_DATA_POINTS_TO_PRINT && index_data_point < max_tick
        # 3. The index_data_point > max_tick
        
        for idx, channel in enumerate(eeg_channels):
            if index_data_point < TOTAL_DATA_POINTS_TO_PRINT:
                y_axis = restored_data[channel][:index_data_point]
                length_missing = TOTAL_DATA_POINTS_TO_PRINT - len(y_axis)
                y_axis = np.pad(y_axis, (length_missing, 0), mode='constant') # pad front of array with 0 to fill 250
                    

            elif index_data_point >= TOTAL_DATA_POINTS_TO_PRINT and index_data_point < max_tick:
                y_axis = restored_data[channel][index_data_point-TOTAL_DATA_POINTS_TO_PRINT:index_data_point]
            
            else : # index_dataPoint > max_tick

                diff_between_max_index = index_data_point - max_tick
                possible_overlap = TOTAL_DATA_POINTS_TO_PRINT - diff_between_max_index
                if possible_overlap > 0:
                    y_axis = restored_data[channel][-possible_overlap:]
                    length_missing = TOTAL_DATA_POINTS_TO_PRINT - possible_overlap
                    y_axis = np.pad(y_axis, (0, length_missing), mode='constant')
                else:
                    y_axis = np.zeros(TOTAL_DATA_POINTS_TO_PRINT)
            
            x_axis = range(1, 251)
            lines[idx].set_data(x_axis, y_axis) 
            # if i < 1:
            #     axes[idx].set_xlim(min(x_axis), max(x_axis))
            #     axes[idx].set_ylim(-200000, 200000)
            axes[idx].set_xlim(min(x_axis), max(x_axis))
            axes[idx].set_ylim(min(restored_data[channel])-10, max(restored_data[channel])+10)
        
        
        print("Index data point : ", index_data_point)
        return lines

    # Create animation
    ani = matplotlib.animation.FuncAnimation(
        fig, animate, interval=16, blit=True
    )
 
    plt.show()
    

def start_stream_and_record():
    print("###################################")
    print("STARTING STREAM AND RECORDING")
    print("###################################")
    brainflow.BoardShim.enable_dev_board_logger()
    print("Creating board")
    board = create_boardshim()
    print("Preparing the session")
    board.prepare_session()
    
    sampling_rate = brainflow.BoardShim.get_sampling_rate(brainflow.BoardIds.CYTON_DAISY_BOARD)
    eeg_channels = brainflow.BoardShim.get_eeg_channels(brainflow.BoardIds.CYTON_DAISY_BOARD)
    print(f"Sampling : {sampling_rate}")
    print(f"eeg_channels : {eeg_channels}")
    time_per_info = 1.0/sampling_rate
    start_time_recording = time.time()
    print(f"")
        
    print("Starting the stream")
    board.start_stream()
    
    live_plotting_16_channels(board)
    
    print("Recording time")
    end_time = time.time() - start_time_recording
    print(end_time)
    
    print("Saving the stream")
    save_all_data_to_files(board)
    
    print("Stopping the stream")
    board.stop_stream()
    board.release_session()

    # print_mean_value(board)

def main():
    # playback_recorded_data("2025-01-20-aee1f314-20c1-41da-b7b8-d13b88477eb9.csv")
    start_stream_and_record()



if __name__ == "__main__":
    main()