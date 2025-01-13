# FlagEEG_v1
Repo of the winter EEG project by the Club d'Intelligence Artificielle of Laval University. The goal of this project is to interpret EEG signals in order to transform them into realtime game inputs.

# How to get started 
## 1. Install the OpenBCI GUI : [download](https://openbci.com/downloads)
This is the official OpenBCI support user interface to allow streaming and seeing data from the EEG. Please download it and follow the installation instructions.
- [Download](https://openbci.com/downloads)
- [Installation instructions](https://docs.openbci.com/Software/OpenBCISoftware/GUIDocs/)

**Important for Linux users** : For Linux users only, there is a necessary hardware step, to make in order to allow the necessary permissions for your USB ports. Go look at the [tutorial](https://docs.openbci.com/Software/OpenBCISoftware/GUIDocs/#linux-users-serial-port-permissions) of the fix. The fix is in the section : _Linux Users: Serial Port Permissions_

## 2. Connect your computer to the helmet
1. Connect the Daisy dongle to your USB port
2. Run the OpenBCI GUI on your computer and start a streaming session : CYTON -> Serial (from Dongle) 

## 3. Read the OpenBCI docs
To help connect your python scripts and the EEG helmet, OpenBCI provides us with a SDK : [Brainflow](https://docs.openbci.com/ForDevelopers/SoftwareDevelopment/). Go read the docs to learn how python and the EEG interacts.
