import requests

API_URL = "https://api-inference.huggingface.co/models/dima806/deepfake_vs_real_image_detection"
API_TOKEN = "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"  # Replace with your actual API token
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

def detect_deepfake(image_path):
    try:
        # Use the query function to get the API response
        api_response = query(image_path)

        # Check if the response is a list and extract relevant information
        if isinstance(api_response, list) and api_response:
            first_prediction = api_response[0].get("prediction", "unknown")
            first_confidence = api_response[0].get("confidence", 0.0)
        else:
            # Handle the case where the response is not a list or is empty
            first_prediction = "unknown"
            first_confidence = 0.0

        result = {
            "prediction": first_prediction,
            "confidence": first_confidence
            # Add more information based on the API response structure if needed
        }

        return result
    except Exception as e:
        # Handle any exceptions that may occur during the detection process
        return {"error": f"An error occurred: {str(e)}"}

# Example usage:
image_path = "sallu.jpg"
detection_result = detect_deepfake(image_path)
print(detection_result)
