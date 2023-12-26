import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def convert_time_to_seconds(time_str):
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds

def max_abs_val_interval(interval):
    # Find the index of the value with the maximum absolute value
    idx_max_abs = interval.abs().idxmax()
    # Return the value from the original interval using the index
    return interval.loc[idx_max_abs]


def modulate_bpm(sec_to_create, new_bpm, original_ecg, original_bpm, sampling_freq):

    original_freq = 1000/sampling_freq
    original_freq = f'{round(original_freq, 4)}L'

    # Create a time series dataframe
    time_index = pd.date_range(start='2023-01-01', periods=len(original_ecg), freq=original_freq)  # 1000ms/128Hz ≈ 7.8125 milliseconds
    # Create a DataFrame
    df = pd.DataFrame({'Value': original_ecg}, index=time_index)

    # Calculate the scaling factor for the total time based on bpm change
    scaling_factor = new_bpm / original_bpm
    sampling_interval_ms = 1000/sampling_freq
    scaled_interval_ms = sampling_interval_ms * scaling_factor
    scaled_freq = f'{round(scaled_interval_ms, 4)}L'

    # Downsample to 64Hz using the mean as the aggregation method
    # 1000ms/64Hz = 15.625 milliseconds
    downsampled = df.resample(scaled_freq).apply(max_abs_val_interval)

    # Calculate the number of data points to include
    num_data_points = int(sec_to_create * sampling_freq)

    # Slice the downsampled dataframe to the desired length
    sliced_ecg = downsampled.iloc[:num_data_points]

    return sliced_ecg