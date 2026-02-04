"""
EEG Blink Pattern Analysis Script
Analyzes EEG data to identify patterns when a patient blinks.

The ground truth channel (our_gt_channel) contains:
- -44: Baseline/resting state
- 44: Blink prompt shown to patient
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.stats import zscore

# Load the data
print("Loading EEG data...")
df = pd.read_csv('khaled_6_cyton.csv')

# Display basic info
print(f"\nDataset shape: {df.shape}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nMarker channel values: {df['our_gt_channel'].unique()}")

# EEG channels (frontal and occipital)
eeg_channels = ['FP1', 'FP2', 'F7', 'F8', 'FZ', 'CZ', 'O1', 'O2']

# Separate data by marker condition
baseline_data = df[df['our_gt_channel'] == -44]
blink_data = df[df['our_gt_channel'] == 44]

print(f"\nBaseline samples (-44): {len(baseline_data)}")
print(f"Blink prompt samples (44): {len(blink_data)}")

# ============================================================
# PLOT 1: Time Series Comparison - FP1 and FP2 (Frontal electrodes)
# ============================================================
fig, axes = plt.subplots(4, 2, figsize=(16, 12))
fig.suptitle('EEG Channel Comparison: Baseline (-44) vs Blink Prompt (44)', fontsize=14, fontweight='bold')

for idx, channel in enumerate(eeg_channels):
    row = idx // 2
    col = idx % 2
    ax = axes[row, col]
    
    # Plot baseline
    baseline_values = baseline_data[channel].values[:500]  # First 500 samples
    ax.plot(baseline_values, label='Baseline (-44)', alpha=0.7, color='blue')
    
    # Plot blink prompt data
    blink_values = blink_data[channel].values[:500] if len(blink_data) >= 500 else blink_data[channel].values
    ax.plot(blink_values, label='Blink Prompt (44)', alpha=0.7, color='red')
    
    ax.set_title(f'{channel} Channel', fontweight='bold')
    ax.set_xlabel('Sample')
    ax.set_ylabel('Amplitude (µV)')
    ax.legend(loc='upper right', fontsize=8)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('plot1_channel_comparison.png', dpi=150, bbox_inches='tight')
print("\nSaved: plot1_channel_comparison.png")

# ============================================================
# PLOT 2: Statistical Distribution Comparison
# ============================================================
fig, axes = plt.subplots(2, 4, figsize=(16, 8))
fig.suptitle('Amplitude Distribution: Baseline vs Blink Prompt', fontsize=14, fontweight='bold')

for idx, channel in enumerate(eeg_channels):
    ax = axes[idx // 4, idx % 4]
    
    baseline_vals = baseline_data[channel].dropna()
    blink_vals = blink_data[channel].dropna()
    
    ax.hist(baseline_vals, bins=50, alpha=0.5, label='Baseline (-44)', color='blue', density=True)
    ax.hist(blink_vals, bins=50, alpha=0.5, label='Blink (44)', color='red', density=True)
    
    ax.set_title(f'{channel}', fontweight='bold')
    ax.set_xlabel('Amplitude (µV)')
    ax.set_ylabel('Density')
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('plot2_amplitude_distribution.png', dpi=150, bbox_inches='tight')
print("Saved: plot2_amplitude_distribution.png")

# ============================================================
# PLOT 3: Mean and Std Comparison Bar Chart
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Mean comparison
means_baseline = [baseline_data[ch].mean() for ch in eeg_channels]
means_blink = [blink_data[ch].mean() for ch in eeg_channels]

x = np.arange(len(eeg_channels))
width = 0.35

ax = axes[0]
bars1 = ax.bar(x - width/2, means_baseline, width, label='Baseline (-44)', color='blue', alpha=0.7)
bars2 = ax.bar(x + width/2, means_blink, width, label='Blink (44)', color='red', alpha=0.7)
ax.set_ylabel('Mean Amplitude (µV)')
ax.set_title('Mean Amplitude by Channel', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(eeg_channels)
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

# Standard deviation comparison
std_baseline = [baseline_data[ch].std() for ch in eeg_channels]
std_blink = [blink_data[ch].std() for ch in eeg_channels]

ax = axes[1]
bars1 = ax.bar(x - width/2, std_baseline, width, label='Baseline (-44)', color='blue', alpha=0.7)
bars2 = ax.bar(x + width/2, std_blink, width, label='Blink (44)', color='red', alpha=0.7)
ax.set_ylabel('Std Deviation (µV)')
ax.set_title('Amplitude Variability by Channel', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(eeg_channels)
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('plot3_statistics_comparison.png', dpi=150, bbox_inches='tight')
print("Saved: plot3_statistics_comparison.png")

# ============================================================
# PLOT 4: Frontal Channels Focus (FP1, FP2) - Blink Detection
# ============================================================
fig, axes = plt.subplots(2, 1, figsize=(16, 8))
fig.suptitle('Frontal Electrodes (FP1, FP2) - Most Sensitive to Blinks', fontsize=14, fontweight='bold')

# Get transition points where marker changes
df['marker_change'] = df['our_gt_channel'].diff().abs()
transitions = df[df['marker_change'] > 0].index.tolist()

for idx, channel in enumerate(['FP1', 'FP2']):
    ax = axes[idx]
    
    # Plot full data
    ax.plot(df.index[:3000], df[channel].values[:3000], color='black', alpha=0.7, linewidth=0.5)
    
    # Highlight blink regions
    for i in range(len(df[:3000])):
        if df.iloc[i]['our_gt_channel'] == 44:
            ax.axvspan(i, i+1, color='red', alpha=0.1)
    
    ax.set_title(f'{channel} - Red shaded = Blink Prompt Period', fontweight='bold')
    ax.set_xlabel('Sample Index')
    ax.set_ylabel('Amplitude (µV)')
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('plot4_frontal_blink_detection.png', dpi=150, bbox_inches='tight')
print("Saved: plot4_frontal_blink_detection.png")

# ============================================================
# PLOT 5: Power Spectral Density Comparison
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Power Spectral Density: Baseline vs Blink', fontsize=14, fontweight='bold')

# Focus on frontal and one occipital channel
focus_channels = ['FP1', 'FP2', 'FZ', 'O1']
fs = 250  # Assuming 250 Hz sampling rate (typical for Cyton)

for idx, channel in enumerate(focus_channels):
    ax = axes[idx // 2, idx % 2]
    
    # Baseline PSD
    baseline_signal = baseline_data[channel].dropna().values
    if len(baseline_signal) > 256:
        f_baseline, psd_baseline = signal.welch(baseline_signal[:1000], fs=fs, nperseg=256)
        ax.semilogy(f_baseline, psd_baseline, label='Baseline (-44)', color='blue', alpha=0.8)
    
    # Blink PSD
    blink_signal = blink_data[channel].dropna().values
    if len(blink_signal) > 256:
        f_blink, psd_blink = signal.welch(blink_signal[:1000], fs=fs, nperseg=256)
        ax.semilogy(f_blink, psd_blink, label='Blink (44)', color='red', alpha=0.8)
    
    ax.set_title(f'{channel} Power Spectrum', fontweight='bold')
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Power Spectral Density')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim([0, 50])

plt.tight_layout()
plt.savefig('plot5_power_spectrum.png', dpi=150, bbox_inches='tight')
print("Saved: plot5_power_spectrum.png")

# ============================================================
# PLOT 6: Blink Event Analysis - Zoomed views
# ============================================================
# Find the exact transition points from -44 to 44
df['next_marker'] = df['our_gt_channel'].shift(-1)
transitions_to_blink = df[(df['our_gt_channel'] == -44) & (df['next_marker'] == 44)].index.tolist()

if len(transitions_to_blink) > 0:
    fig, axes = plt.subplots(min(3, len(transitions_to_blink)), 2, figsize=(14, 10))
    fig.suptitle('Blink Events - FP1 & FP2 Around Transition Points', fontsize=14, fontweight='bold')
    
    for event_idx in range(min(3, len(transitions_to_blink))):
        transition = transitions_to_blink[event_idx]
        
        # Window around transition: 200 samples before, 300 after
        start_idx = max(0, transition - 200)
        end_idx = min(len(df), transition + 300)
        
        window_data = df.iloc[start_idx:end_idx]
        
        for ch_idx, channel in enumerate(['FP1', 'FP2']):
            if len(transitions_to_blink) == 1:
                ax = axes[ch_idx]
            else:
                ax = axes[event_idx, ch_idx]
            
            # Plot the signal
            x_vals = range(start_idx, end_idx)
            ax.plot(x_vals, window_data[channel].values, color='black', linewidth=1)
            
            # Mark transition point
            ax.axvline(x=transition, color='green', linestyle='--', linewidth=2, label='Transition')
            
            # Shade blink region
            for i in range(len(window_data)):
                if window_data.iloc[i]['our_gt_channel'] == 44:
                    ax.axvspan(start_idx + i, start_idx + i + 1, color='red', alpha=0.2)
            
            ax.set_title(f'{channel} - Event {event_idx + 1}', fontweight='bold')
            ax.set_xlabel('Sample Index')
            ax.set_ylabel('Amplitude (µV)')
            ax.grid(True, alpha=0.3)
            if event_idx == 0:
                ax.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig('plot6_blink_events.png', dpi=150, bbox_inches='tight')
    print("Saved: plot6_blink_events.png")

# ============================================================
# Statistical Summary
# ============================================================
print("\n" + "="*70)
print("STATISTICAL SUMMARY")
print("="*70)

print("\n📊 Channel Statistics Comparison:")
print("-" * 70)
print(f"{'Channel':<10} {'Baseline Mean':<18} {'Blink Mean':<18} {'Difference':<15} {'% Change':<10}")
print("-" * 70)

for channel in eeg_channels:
    baseline_mean = baseline_data[channel].mean()
    blink_mean = blink_data[channel].mean()
    diff = blink_mean - baseline_mean
    pct_change = (diff / abs(baseline_mean)) * 100 if baseline_mean != 0 else 0
    print(f"{channel:<10} {baseline_mean:<18.2f} {blink_mean:<18.2f} {diff:<15.2f} {pct_change:<10.2f}%")

print("\n📊 Amplitude Variability (Standard Deviation):")
print("-" * 70)
print(f"{'Channel':<10} {'Baseline Std':<18} {'Blink Std':<18} {'Ratio (B/A)':<15}")
print("-" * 70)

for channel in eeg_channels:
    baseline_std = baseline_data[channel].std()
    blink_std = blink_data[channel].std()
    ratio = blink_std / baseline_std if baseline_std != 0 else 0
    print(f"{channel:<10} {baseline_std:<18.2f} {blink_std:<18.2f} {ratio:<15.2f}")

print("\n" + "="*70)
print("KEY FINDINGS FOR BLINK DETECTION:")
print("="*70)
print("""
🔍 WHAT TO LOOK FOR IN BLINK PATTERNS:

1. **Amplitude Spikes**: Blinks typically cause large positive deflections
   followed by negative deflections in frontal channels (FP1, FP2).

2. **Frontal Dominance**: FP1 and FP2 show the largest changes because
   they are closest to the eyes.

3. **Duration**: A typical blink lasts 100-400ms. At 250 Hz sampling,
   this is approximately 25-100 samples.

4. **Frequency Content**: Blink artifacts are typically low-frequency
   (< 4 Hz), so they affect the delta band.

5. **Bilateral Symmetry**: Since blinks affect both eyes, FP1 and FP2
   should show similar patterns.

📈 RECOMMENDED DETECTION APPROACHES:
- Threshold-based: Set amplitude threshold on FP1/FP2
- Z-score based: Detect outliers (z > 2-3)
- Template matching: Compare with known blink waveform
- Machine learning: Train classifier on labeled data
""")

plt.show()
print("\n✅ Analysis complete! Check the generated plots.")
