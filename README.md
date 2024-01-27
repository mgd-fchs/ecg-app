# Synthetic ECG Generation Web App

This app is designed to generate synthetic ECG signals, using pre-trained GANs or a VAE. The backend is built with Flask and TensorFlow Serving, generating and serving synthetic data. The frontend allows users to specify parameters for the signal generation, such as duration, BPM, and the type of generative model used.

## Features

- Generate synthetic heart rate signals based on user-defined parameters.
- Download generated signals as CSV files.
- Docker-compose setup for deployment, including TensorFlow Serving for model serving.

## Installation and Usage

1. **Prerequisites**: Docker and Docker Compose

2. **Build and Run with Docker Compose**: 

    ```bash
    docker-compose up --build
    ```

    This command will start the backend, frontend, and TensorFlow Serving containers.

3. **Accessing the Application**: 
    - Frontend at `http://localhost:3000`
    - Backend API at `http://localhost:5000`
    - TensorFlow Serving at `http://localhost:8501`

3. **Generating Synthetic Signals**:
    - Use the frontend interface to specify signal generation parameters and submit the request.
    - The backend will process the request, generate the synthetic signal, and provide a link to download the CSV file.
