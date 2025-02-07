"""Install with pip install brainflow."""
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds

def start_eeg_stream():
    """Initializes the EEG stream and returns the board object."""
    params = BrainFlowInputParams()
    params.serial_port = "/dev/ttyUSB0"
    board = BoardShim(BoardIds.CYTON_DAISY_BOARD.value, params)
    board.prepare_session()
    board.start_stream()
    return board

def get_eeg_data(board, samples=5):
    """Receives last EEG data from the board."""
    data = board.get_current_board_data(samples)
    return data if data.shape[1] > 0 else None
