# EEG Recording Protocol Quick Version

### 1. Objective
To collect and annotate EEG signals associated with blinking events for training, analysis, and model-building purposes.

###  2. Equipment
- EEG device with at least 8 electrodes (include frontal electrodes like Fp1, Fp2 for optimal detection of blinks).
- Computer with EEG recording software and storage capacity.
- Comfortable chair and room setup.
- Video recording device for synchronized blink validation.

### 3. Participant Preparation
- Ensure participants have clean and dry skin on the scalp to maximize electrode contact.
- Seat participants in a comfortable chair in a quiet, dimly lit room.
- Explain the process and provide a consent form for data collection.
- Fit the EEG cap or electrodes according to the device's guidelines, ensuring placement is accurate for detecting frontal lobe activity.

### 4. Task Design
1. Baseline Recording (2 minutes):
- Objective: Establish a "no-blink" baseline signal for comparison.
- Instructions: Participants keep their eyes open and avoid blinking as much as possible. A relaxing focus point (e.g., crosshair) is provided on the screen to help maintain attention.
2. Controlled Voluntary Blinks (5 minutes):
- Objective: Collect data with precisely timed blinking events.
- Instructions: Participants blink deliberately following an on-screen or auditory cue:
  - Phase 1: Blink every 2 seconds.
  - Phase 2: Blink every 5 seconds.
  - Phase 3: Blink twice in quick succession every 5 seconds (to capture double-blink patterns).

Annotations: Each blink must be labeled in real time (e.g., "start" and "end" timestamps) for training the model.
3. Unsupervised Natural Blinking (5 minutes):
- Objective: Capture data with spontaneous blinking behavior.
- Instructions: Participants watch a short video or image slideshow designed to hold their attention without inducing excessive eye strain.
- Annotations: Use video recording or real-time monitoring to label detected natural blinks.

### 5. Data Collection Procedure
Start EEG recording, ensuring synchronization with time-stamped annotations for tasks and stimuli.
Begin the tasks in the specified order.
Annotate data in real time for each task (e.g., voluntary, involuntary, or stimulated blink).
Monitor participants to ensure comfort and compliance with instructions.