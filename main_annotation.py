import data_streamer.datasaver as saver
import data_streamer.streamer as streamer
import brainflow





# Steps for annotation : 
## 1. Launch GUI with the necessary informations
## 2. Connect the helmet
## 3. Connect GUI Start Recording with Jo's application
## 4. Allow for stop
## 5. Annotate data

def main():
    saver_gui = saver.Datasaver(board_type=brainflow.BoardIds.CYTON_BOARD)
    saver_gui.start_main_loop()
    

if __name__ == "__main__":
    main()