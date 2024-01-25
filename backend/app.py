from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import send_from_directory
from scipy.interpolate import interp1d
import requests
import json
import numpy as np
import heartpy as hp
import os

from app_utils import *
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

def log_request_response(request, response):
    request_data = request.get_json() if request.method == 'POST' else {}
    logging.info(f"Request URL: {request.url}")
    logging.info(f"Request Method: {request.method}")
    logging.info(f"Request Data: {request_data}")
    logging.info(f"Response Data: {response}")

def log_external_request_response(url, request_data, response):
    logging.info(f"External Request URL: {url}")
    logging.info(f"Request Data: {request_data}")
    logging.info(f"Response Status Code: {response.status_code}")
    logging.info(f"Response Data: {response.text}")



app = Flask(__name__)
app.config['STATIC_FOLDER'] = '/frontend/static'
app.config['TF_SERVING_URL'] = 'http://tf-serving:8501/v1/models/'

CORS(app)

@app.route('/api/data', methods=['GET'])
def get_data():
    # Replace this with actual data retrieval logic
    data = {"key": "value"}
    return jsonify(data)


@app.route('/download/<filename>')
def download_file(filename):
    logging.info(f"Providing download: {filename}")

    return send_from_directory(app.config['STATIC_FOLDER'], filename, as_attachment=True)


@app.route('/generate', methods=['POST'])
def generate_recording():
    if request.method == 'POST':
        data = request.get_json()
        time = data.get('time')
        type_ = data.get('type')
        bpm = data.get('bpm')

        # log_request_response(request, data)
        print(f"Got data: {type_}")
        # Convert time to seconds
        try:
            time = convert_time_to_seconds(time)
        except ValueError:
            return jsonify({'status': 'error', 'message': 'Invalid time format'}), 400

        # Validate time
        if time is None or time > 300 or time < 10:
            return jsonify({'status': 'error', 'message': 'Time must be between 10 and 300 seconds'}), 400

        # Validate BPM
        try:
            bpm = int(bpm)
            if bpm < 45 or bpm > 180:
                raise ValueError
        except ValueError:
            return jsonify({'status': 'error', 'message': 'BPM must be an integer between 45 and 180'}), 400
        
        try:
            file_path = generate_output_sequence(app.config['STATIC_FOLDER'], time, bpm, type_)
        except Exception as e:
            # Handle exceptions that might occur during file generation
            return jsonify({'status': 'error', 'message': str(e)}), 500

        file_name = os.path.split(file_path)[-1]
        file_url = 'http://localhost:5000/download/' + file_name 

        return jsonify({'status': 'success', 'message': 'Data processed successfully!', 'file_url': file_url})


def generate_output_sequence(results_folder, sec_to_create, bpm, type_):
    os.makedirs(results_folder, exist_ok = True)

    default_bpm = 45
    sample_frequency = 128
    num_samples = (sec_to_create / 10)
    num_samples = int(num_samples)*10
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
        model_url = app.config['TF_SERVING_URL'] + f"{type_}:predict"
        response = requests.post(model_url, json=serving_data)
        # log_external_request_response(model_url, serving_data, response)

        if response.status_code == 200:
            predictions = response.json()
            gen_output = np.array(predictions['predictions'])

            wd, m = hp.process(gen_output.flatten(), sample_frequency)
            gen_bpm = m['bpm']

            combined_output = np.concatenate((combined_output, gen_output.flatten()))

        else:
            raise ValueError(f"Error during TensorFlow Serving request: {response.text}")

    # Adjust hear rate

    logging.info(f"Combined output size: {combined_output.size}")
    wd, m = hp.process(combined_output, sample_frequency)
    original_bpm = m['bpm']
    original_bpm = 55
    
    logging.info(f"Original BPM: {original_bpm}")

    output_df = modulate_bpm(sec_to_create, bpm, combined_output, original_bpm, sample_frequency)
    wd, m = hp.process(gen_output.flatten(), sample_frequency)
    gen_bpm = m['bpm']

    # Write to csv
    file_path = f'{results_folder}/recording_data.csv'
    output_df.to_csv(file_path, index=False)

    return file_path


if __name__ == '__main__':
    app.run(debug=True)
