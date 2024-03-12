from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import boto3
import os
from servs.celebRekog import celebDetails
from servs.delete_file import delete_file
import cv2
import numpy as np
from tensorflow.keras.models import model_from_json

app = Flask(__name__)
CORS(app, origins="*")

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the ResNet model architecture and weights
try:
    with open('model_resnet50_architecture.json', 'r') as json_file:
        model_json = json_file.read()

    resnet_model = model_from_json(model_json)
    resnet_model.load_weights('model_resnet50_weights.h5')
except Exception as e:
    print("Error loading model:", e)
    exit()

@app.route('/')
def index():
    return render_template('index.html', result=None)

@app.route('/recognize_celebrities', methods=['POST'])
def recognize_celebrities():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Save the uploaded file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    celebrities_data, error = celebDetails(file_path)
    if error:
        delete_file(file_path)
        return jsonify({'error': error})

    delete_file(file_path)
    return jsonify(celebrities_data)

@app.route('/detect', methods=['POST'])
def detect():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Save the uploaded file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Classify the frame
    frame = cv2.imread(file_path)
    prediction = classify_frame(frame, resnet_model)

    delete_file(file_path)

    if prediction is not None:
        # Interpret the results
        threshold = 0.25  # Adjust based on your model and requirements
        result = "Frame classified as a deepfake." if prediction[0] < threshold else "Frame classified as real."
        return jsonify({'result': result})

if __name__ == '__main__':
    port = 5000
    app.run(port=port, debug=True)
