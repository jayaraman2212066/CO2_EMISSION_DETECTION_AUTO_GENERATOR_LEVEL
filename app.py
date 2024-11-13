import numpy as np
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from flask_cors import CORS



# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Load the pre-trained Keras model
MODEL_PATH = "co2_keras_model_improved.keras"
try:
    model = load_model(MODEL_PATH)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Define a function to preprocess the input data
def preprocess_input(data):
    try:
        # Convert input CO2 levels into a numpy array
        X = np.array([np.array(seq).reshape(-1, 1) for seq in data])
        return X
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        return None

# Define a function to calculate CO2 level percentage and label
def categorize_co2_level(ppm_value):
    ppm_value = ppm_value * 1000
    co2_percentage = (ppm_value /1501) * 100  # Assuming 1501 ppm is 100%
    
    # Determine CO2 level category based on ppm_value thresholds
    if ppm_value <= 800:
        label = "Normal"
    elif 800 < ppm_value <= 1500:
        label = "Moderate"
    else:
        label = "High"
    
    return co2_percentage, label

# Define the /predict endpoint
@app.route('/predict', methods=['POST'])
def predict_co2_levels():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        # Extract JSON data from the request
        data = request.json.get("co2_levels", None)
        if not data:
            return jsonify({"error": "No CO2 data provided"}), 400
        
        # Preprocess the data
        X = preprocess_input(data)
        if X is None:
            return jsonify({"error": "Invalid input format"}), 400
        
        # Make predictions using the model
        predictions = model.predict(X)
        
        # Assuming each prediction represents a CO2 level in PPM
        co2_ppm_values = predictions.flatten().tolist()
        
        # Convert PPM values to percentages and categorize based on thresholds
        results = []
        for co2_ppm in co2_ppm_values:
            co2_percentage, label = categorize_co2_level(co2_ppm)
            results.append({
                "co2_ppm": co2_ppm * 1000 ,
                "co2_percentage": co2_percentage,
                "co2_level": label
            })
        
        # Return the predictions as a JSON response
        return jsonify(results), 200
    
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)





