import numpy as np
import math
import logging

def downsample_ecg(original_ecg, new_bpm, original_bpm):
    # Compute the scaling factor
    scaling_factor = max(1, new_bpm / original_bpm)

    logging.info(f"Scaling factor: {scaling_factor}")

    # Initialize the resampled ECG
    resampled = []

    # Calculate the size of each interval and iterate over them
    index = 0
    while index < len(original_ecg):
        next_index = min(len(original_ecg), math.ceil((index + 1) * scaling_factor))
        interval = original_ecg[int(math.floor(index * scaling_factor)):int(next_index)]
        if interval:  # Only add if interval is not empty
            resampled.append(max(interval, key=abs))  # Taking max of absolute values
        index += 1

    logging.info(f"Resampled to length: {len(resampled)} from length: {len(original_ecg)}")
    return resampled

# Example
original_ecg = [1, -3, 5, -7, 2, -4, 6, 8] 
new_bpm = 150  # New BPM value
original_bpm = 100  # Original BPM value
resampled_ecg = downsample_ecg(original_ecg, new_bpm, original_bpm)

print(resampled_ecg)
