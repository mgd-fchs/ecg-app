from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import send_from_directory
from scipy.interpolate import interp1d
import requests
import json
import numpy as np
import os

from app_utils import *

# Import any other necessary modules

app = Flask(__name__)
app.config['STATIC_FOLDER'] = '/frontend/static'
app.config['TF_SERVING_URL'] = 'http://tf-serving:8501/v1/models/gan_model1:predict'

CORS(app)

@app.route('/api/data', methods=['GET'])
def get_data():
    # Replace this with actual data retrieval logic
    data = {"key": "value"}
    return jsonify(data)


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename, as_attachment=True)


@app.route('/generate', methods=['POST'])
def generate_recording():
    if request.method == 'POST':
        data = request.get_json()
        time = data.get('time')
        type_ = data.get('type')
        bpm = data.get('bpm')

        # print(f"Time: {time}, Type: {type_}, BPM: {bpm}")

        # Convert time to seconds
        try:
            time = convert_time_to_seconds(time)
            # print(time)

        except ValueError:
            return jsonify({'status': 'error', 'message': 'Invalid time format'}), 400

        # Validate data
        if time is None or time > 300 or time < 10:
            return jsonify({'status': 'error', 'message': 'Time must be between 10 and 300 seconds'}), 400

        try:
            bpm = int(bpm)
        except ValueError:
            return jsonify({'status': 'error', 'message': 'BPM must be an integer value'}), 400
        
        if bpm is None or bpm > 180 or bpm < 45:
            return jsonify({'status': 'error', 'message': 'BPM must be between 48 and 180'}), 400


        file_path = generate_output_sequence(app.config['STATIC_FOLDER'], time, bpm, type_)
        file_name = os.path.split(file_path)[-1]
        file_url = 'http://localhost:5000/download/' + file_name 

        return jsonify({'status': 'success', 'message': 'Data processed!', 'file_url': file_url})


def generate_output_sequence(results_folder, sec_to_create, bpm, type):
    os.makedirs(results_folder, exist_ok = True)

    default_bpm = 45
    sample_frequency = 128
    num_samples = (sec_to_create / 10)
    num_samples = int(np.ceil((bpm/default_bpm)*num_samples))+10
    noise_dim = 100 
    output_strings = []
    combined_output = np.array([])

    for i in range(0, num_samples):
        seed = np.random.normal(0, 1, (1, noise_dim)).tolist()
        
        # Prepare data for TensorFlow Serving
        serving_data = {
            "signature_name": "serving_default",
            "instances": seed
        }

        # Make a POST request to TensorFlow Serving
        response = requests.post(app.config['TF_SERVING_URL'], json=serving_data)

        if response.status_code == 200:
            predictions = response.json()
            gen_output = np.array(predictions['predictions'])
            combined_output = np.concatenate((combined_output, gen_output.flatten()))
            
            # output_str = ','.join(map(str, gen_output.flatten()))+','
            # output_strings.append(output_str)
        else:
            raise ValueError(f"Error during TensorFlow Serving request: {response.text}")

    # Adjust hear rate
    print("Adjusting heart rate")
    output_df = modulate_bpm(sec_to_create, bpm, combined_output, default_bpm, sample_frequency)

    # Write to csv
    file_path = f'{results_folder}/recording_data.csv'
    output_df.to_csv(file_path, index=False)

    return file_path


if __name__ == '__main__':
    app.run(debug=True)