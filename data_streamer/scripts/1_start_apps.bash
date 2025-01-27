#!/bin/bash
GAME_PYTHON_FILE_PATH="../EEG_flappy_bird/main.py"
OPENBCI_GUI_FILE_PATH="../OpenBCI_GUI/OpenBCI_GUI"
STREAMER_SCRIPT_FILE_PATH="data_streamer/streamer_v2.py"


$OPENBCI_GUI_FILE_PATH &
python $STREAMER_SCRIPT_FILE_PATH & 
