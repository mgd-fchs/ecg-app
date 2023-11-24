from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import send_from_directory
import json

from app_utils import *
from model_inference import *

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'C:/_uni/ecg-app-git/frontend/static'
app.config['MODEL_PATH'] = "C:/_uni/ecg_data_generation/results/results-16272/results/models/gen_model_50.h5"

CORS(app)


@app.route('/api/data', methods=['GET'])
def get_data():
    # Replace this with actual data retrieval logic
    data = {"key": "value"}
    return jsonify(data)


# Assuming your files are saved in a 'static' directory
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename, as_attachment=True)


@app.route('/generate', methods=['POST'])
def generate_recording():
    if request.method == 'POST':
        # Parse the JSON data from the request

        print(app.config['STATIC_FOLDER'])
        data = request.get_json()
        time = data.get('time')
        type_ = data.get('type')  # "type" is a built-in function in Python, consider renaming this variable
        bpm = data.get('bpm')

        print(f"Time: {time}, Type: {type_}, BPM: {bpm}")


        # Convert time to seconds
        try:
            time = convert_time_to_seconds(time)
            print(time)

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

        # TODO: Dummy data creation, replace with actual data file
        # TODO: Handle data (e.g., generate recording)
        file_data = {
            'time': time,
            'type': type_,
            'bpm': bpm
        }

        # TODO: Handle file paths

        full_file_path = generate_output_sequence(app.config['STATIC_FOLDER'], app.config['MODEL_PATH'], time, bpm, type_)
        file_name = os.path.split(full_file_path)[-1]

        file_url = 'http://localhost:5000/' + '/download/' + file_name 

        # Send a success response and generated file back to the frontend
        return jsonify({'status': 'success', 'message': 'Data received and validated!', 'file_path': full_file_path, 'file_url': file_url})


if __name__ == '__main__':
    app.run(debug=True)
