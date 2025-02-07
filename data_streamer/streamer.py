import brainflow

class streamer:
    def __init__(self):
        self.SERIAL_PORT = "/dev/ttyUSB0"
        self.BOARD_ID = brainflow.board_shim.BoardIds.CYTON_DAISY_BOARD
        self.board = self.create_boardshim()
        
    def create_boardshim(self)->brainflow.BoardShim:
        params = brainflow.BrainFlowInputParams()
        params.serial_port = self.SERIAL_PORT
        return brainflow.BoardShim(self.BOARD_ID, params)    
    
    def start_streaming(self):
        self.board.prepare_session()
        self.board.start_stream()
        self.stream_loop()
        
    def stream_loop(self):
        data = self.board.get_current_board_data(1)
        
    