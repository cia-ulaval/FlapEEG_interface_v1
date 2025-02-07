export LD_LIBRARY_PATH=/home/louis/.conda/envs/flapeeg/lib:$LD_LIBRARY_PATH

DATA_STREAMER_PATH="data_streamer"
source $DATA_STREAMER_PATH/venv/bin/activate
pip install -r $DATA_STREAMER_PATH/requirements.txt

xhost + #To allow keyboard access