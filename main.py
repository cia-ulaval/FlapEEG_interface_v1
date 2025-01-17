import brainflow
import typing
import time
import numpy as np
import brainflow.board_shim
import matplotlib.pyplot as plt
import matplotlib.animation

SERIAL_PORT = "/dev/ttyUSB0"
# SERIAL_PORT = "COM3"
# SERIAL_PORT = "COM7" could be one of those if  

BOARD_ID = brainflow.board_shim.BoardIds.CYTON_DAISY_BOARD

MASTER_BOARD = brainflow.BoardIds.NO_BOARD

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
    eeg_channels = brainflow.BoardShim.get_eeg_channels(brainflow.BoardIds.CYTON_DAISY_BOARD)
    
    # Create a figure
    fig = plt.figure()
    axes = []
    lines = []
    
    # Create subplots for each EEG channel
    for i, channel in enumerate(eeg_channels):
        ax = fig.add_subplot(len(eeg_channels), 1, i + 1)
        ax.set_title(f"Channel {i+1}")
        ax
        line, = ax.plot([], [], lw=1) 
        axes.append(ax)
        lines.append(line)

    # Animate function
    def animate(i):
        data = board.get_current_board_data(250)
        for idx, channel in enumerate(eeg_channels):
            print(range(data.shape[1]), data[channel])
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

def main():
    
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
    
        
    print("Starting the stream")
    board.start_stream()
    
    live_plotting_16_channels(board)
    
    
    print("Stopping the stream")
    board.stop_stream()

    print_mean_value(board)

if __name__ == "__main__":
    main()