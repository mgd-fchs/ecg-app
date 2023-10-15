from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/data', methods=['GET'])
def get_data():
    # Replace this with actual data retrieval logic
    data = {"key": "value"}
    return jsonify(data)



@app.route('/generate', methods=['POST'])
def generate_recording():
    if request.method == 'POST':
        # Parse the JSON data from the request
        data = request.get_json()
        time = data.get('time')
        type = data.get('type')  # "type" is a built-in function in Python, consider renaming this variable
        bpm = data.get('bpm')

        print(f"Time: {time}, Type: {type}, BPM: {bpm}")

        # Validate data
        if time is None or time > 300 or time < 10:
            return jsonify({'status': 'error', 'message': 'Time must be between 10 and 300 seconds'}), 400

        if bpm is None or bpm > 180 or bpm < 48:
            return jsonify({'status': 'error', 'message': 'BPM must be between 48 and 180'}), 400

        # TODO: Handle data (e.g., generate recording)

        # Send a success response back to the frontend
        return jsonify({'status': 'success', 'message': 'Data received and validated!'})

if __name__ == '__main__':
    app.run(debug=True)
