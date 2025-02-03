from pylsl import StreamInlet, resolve_byprop
import sys
sys.path.append('../')
from eeg_processing.detection import detect_blink
from game_control.flappy_control import jump
import time

# Need to create an inlet
streams = resolve_byprop("type", "EEG")
inlet = StreamInlet(streams[0])
print("streams : ", streams)
print("inlet : ", inlet)

info = inlet.info()
print("Stream name:", info.name())
print("Channel count:", info.channel_count())
print("Nominal sampling rate:", info.nominal_srate())
print("Type:", info.type())
print("Channel format:", info.channel_format())

desc = info.desc()
channels = desc.child("channels").child("channel")
print("Channel Labels:")
for i in range(info.channel_count()):
    print(f"Channel {i+1}: {channels.child_value('label')}")
    channels = channels.next_sibling()

try:
    while True:
        sample, timestamp = inlet.pull_sample()

        print("=============================================")
        if (detect_blink(sample)):
            jump()

        
except KeyboardInterrupt as e:
    print("Ending program")
    raise e