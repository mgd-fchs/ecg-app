import tensorflow as tf
import pandas as pd
from matplotlib import pyplot as plt
from tqdm import tqdm
import numpy as np
import os


def load_model(model_path):
    # TODO: Add model selection
    generator = tf.keras.models.load_model(model_path)
    return generator


# def generate_output_sequence(results_folder, model_path, sec_to_create, bpm, type):

#     num_samples = sec_to_create // 10
#     generator = load_model(model_path)
#     noise_dim = 100 

#     for i in range(0, num_samples):
#         seed = np.random.normal(0, 1, (1, noise_dim))
#         gen_output = generator(seed, training=False)
        
#         # Flatten the output and convert it to a string format
#         output_str = ','.join(map(str, gen_output.numpy().flatten()))+','

#         # Define the file path
#         file_path = f'{results_folder}/recording_data.csv'

#         # Write the output to the file
#         with open(file_path, 'a') as file:
#             file.write(output_str)
    
#     return file_path


## Quick test sequence creation
# MODEL_PATH = "C:/_uni/ecg_data_generation/results/results-16272/results/models/gen_model_50.h5"
# RES_FOLDER="C:/_uni/ecg-app-git/frontend/static"
# out_file = generate_output_sequence(RES_FOLDER, MODEL_PATH, 60, 60, "normal")

# data = pd.read_csv(out_file, header=None, sep=',').iloc[0]

# # If your CSV file has timestamps, replace 'range(len(data))' with your timestamp data
# time_series = range(len(data))

# # Plotting
# plt.figure(figsize=(10, 6))
# plt.plot(time_series, data)
# plt.title('Time Series Plot')
# plt.xlabel('Time')
# plt.ylabel('Values')
# plt.grid(True)
# plt.show()