import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import heartpy as hp
import logging
import scipy.interpolate

# Set up logging
logging.basicConfig(level=logging.INFO)


def interpolate_points(p1, p2, n_steps=10):
    """ Linear interpolation between two points in the latent space. """
    ratios = np.linspace(0, 1, num=n_steps)
    return [(1.0 - ratio) * p1 + ratio * p2 for ratio in ratios]


def convert_time_to_seconds(time_str):
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds


def max_abs_val_interval(interval):
    # Find the index of the value with the maximum absolute value
    idx_max_abs = interval.abs().idxmax()
    # Return the value from the original interval using the index
    return interval.loc[idx_max_abs]


def modulate_bpm(sec_to_create, new_bpm, original_ecg, original_bpm, sampling_freq):

    # time_index = pd.date_range(start='2024-01-01', periods=len(original_ecg), freq=f'{round(original_interval_ms)}L')
    df = pd.DataFrame({'Value': original_ecg})

    logging.info(f"New BPM: {new_bpm}")
    logging.info(f"Original BPM: {original_bpm}")

    # Resample df
    if new_bpm > original_bpm:
        scaling_factor = new_bpm / original_bpm

        logging.info(f"Scaling factor: {scaling_factor}")

        resampled = []

        # Calculate size of each interval and iterate over them
        index = 0
        while index < len(original_ecg):
            next_index = min(len(original_ecg), math.ceil((index + 1) * scaling_factor))
            interval = original_ecg[int(math.floor(index * scaling_factor)):int(next_index)]
            if len(interval) > 0:  # Check if the interval is not empty
                resampled.append(max(interval, key=abs))  # Taking max of absolute values
            index += 1

        logging.info(f"Resampled to length: {len(resampled)} from length: {len(original_ecg)}")

    else:
        scaling_factor = original_bpm / new_bpm
        logging.info(f"Scaling factor: {scaling_factor}")

        # Original array length
        n = len(original_ecg)
        
        # New length after resampling
        new_length = int(np.ceil(n * scaling_factor))
        
        # Original indices
        original_indices = np.arange(n)
        
        # New indices for interpolation
        new_indices = np.linspace(0, n - 1, new_length)
        
        # Interpolate using linear method
        interpolator = scipy.interpolate.interp1d(original_indices, original_ecg, kind='linear')
        resampled = interpolator(new_indices)
        
        logging.info(f"Resampled to length: {len(resampled)} from length: {len(original_ecg)}")

    # Calculate the number of data points to include
    num_data_points = int(sec_to_create * sampling_freq)
    # Ensure that we do not exceed the length of downsampled data
    num_data_points = min(num_data_points, len(resampled))

    # Slice the downsampled dataframe to the desired length
    sliced_ecg = resampled[:num_data_points]


    start_time = pd.Timestamp('2024-01-01 00:00:00')
    frequency = '7.8125L'  # 1/128 seconds in milliseconds
    num_samples = len(sliced_ecg)
    date_time_index = pd.date_range(start=start_time, periods=num_samples, freq=frequency)

    # Create the DataFrame
    df = pd.DataFrame(sliced_ecg, index=date_time_index, columns=['Values'])
    return df