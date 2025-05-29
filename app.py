import numpy as np
from flask import Flask, request, jsonify, send_from_directory
from tensorflow.keras.models import load_model
from flask_cors import CORS
from models import db, Prediction
from config import Config
import tensorflow as tf

# Set TensorFlow logging level
tf.get_logger().setLevel('ERROR')

# Initialize Flask app and enable CORS
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize database
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

# Load the pre-trained Keras model
try:
    model = load_model(Config.MODEL_PATH, compile=False, safe_mode=False)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Serve index.html at the root URL
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# Serve other static files like CSS and JavaScript
@app.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory('.', filename)

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
            
            # Store prediction in database
            prediction = Prediction(
                co2_levels=data,
                prediction_ppm=co2_ppm * 1000,
                prediction_percentage=co2_percentage,
                prediction_level=label
            )
            db.session.add(prediction)
            db.session.commit()
            
            results.append({
                "co2_ppm": co2_ppm * 1000,
                "co2_percentage": co2_percentage,
                "co2_level": label
            })
        
        # Return the predictions as a JSON response
        return jsonify(results), 200
    
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({"error": str(e)}), 500

# Add endpoint to get prediction history
@app.route('/history', methods=['GET'])
def get_prediction_history():
    try:
        predictions = Prediction.query.order_by(Prediction.timestamp.desc()).limit(10).all()
        return jsonify([pred.to_dict() for pred in predictions]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)





