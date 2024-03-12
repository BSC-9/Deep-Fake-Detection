# import os
# import boto3
# from flask import jsonify

# # Initialize AWS Rekognition client
# rekognition = boto3.client('rekognition')

# def celebRekog(file_path):
#     try:
#         # Call Amazon Rekognition API to recognize celebrities
#         with open(file_path, 'rb') as img_file:
#             response = rekognition.recognize_celebrities(
#                 Image={'Bytes': img_file.read()}
#             )
        
#         # Return recognized celebrities
#         celebrities = []
#         for celebrity in response['CelebrityFaces']:
#             celebrities.append({
#                 'Name': celebrity['Name']})
        
#         return {'celebrities': celebrities}, None
#     except Exception as e:
#         return None, str(e)

import os
import boto3
import json
import google.generativeai as genai
from flask import Flask, jsonify

app = Flask(__name__)

# Initialize AWS Rekognition client
rekognition = boto3.client('rekognition')

def celebRekog(file_path):
    try:
        # Call Amazon Rekognition API to recognize celebrities
        with open(file_path, 'rb') as img_file:
            response = rekognition.recognize_celebrities(
                Image={'Bytes': img_file.read()}
            )
        
        # Return recognized celebrities
        celebrities = []
        for celebrity in response['CelebrityFaces']:
            celebrities.append({
                'Name': celebrity['Name']})
        
        return {'celebrities': celebrities}, None
    except Exception as e:
        return None, str(e)

def celebDetails(file_path):
    celeb_info, error = celebRekog(file_path)

    if error:
        return jsonify({'error': error}), None

    celeb_details = []
    for celeb in celeb_info['celebrities']:
        genai.configure(api_key='AIzaSyA5XSNSmCedWb0IKmyRfsjI9-b5686Gp3s')
        model = genai.GenerativeModel('gemini-pro')

        h = "Tell me about this celebrity in two lines: "
        h += celeb['Name']
        response = model.generate_content(h)

        celeb_details.append({
            'Name': celeb['Name'],
            'Summary': response.text
        })

    return celeb_details, None

@app.route('/recognize_celebrities', methods=['POST'])
def recognize_celebrities():
    file_path = request.files['image'].read()
    celebrities_data, error = celebDetails(file_path)

    if error:
        return jsonify({'error': error}), 500

    return jsonify(celebrities_data)

if __name__ == '__main__':
    app.run(debug=True)