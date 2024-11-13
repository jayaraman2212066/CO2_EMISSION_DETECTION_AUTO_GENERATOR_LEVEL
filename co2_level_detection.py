import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.metrics import accuracy_score, classification_report

# Load the dataset
def load_manual_dataset(file_path="manual_co2_dataset.csv"):
    data_df = pd.read_csv(file_path)
    X = np.array([np.array(seq).reshape(-1, 1) for seq in data_df['co2_levels'].apply(eval)])
    y = data_df['label'].values
    return X, y

# Load the model
model = load_model("co2_keras_model_improved.keras")
print("Model loaded successfully.")

# Predict function with CO₂ level in ppm
def predict_co2_levels(model, X):
    predictions = model.predict(X)
    predicted_labels = (predictions > 0.5).astype(int)
    return predictions, predicted_labels

# Run predictions
X, y = load_manual_dataset()
predictions, predicted_labels = predict_co2_levels(model, X)

# Evaluation
accuracy = accuracy_score(y, predicted_labels)
print(f"Model Accuracy: {accuracy * 100:.2f}%")
print("Classification Report:")
print(classification_report(y, predicted_labels))

# Real-time sample prediction
new_data_sequence = np.array([[400], [500], [550], [600], [620], [650], [700], [750], [800], [850]]).reshape(1, -1, 1)

# Predict CO₂ level
new_prediction = model.predict(new_data_sequence)
new_label = int(new_prediction[0] > 0.5)

# Interpret CO₂ level in ppm
average_co2_ppm = new_data_sequence.mean()  # Calculate average CO₂ level in ppm

# Define CO₂ level ranges
def interpret_co2_level(co2_ppm):
    if co2_ppm <= 800:
        return "Normal"
    elif 800 < co2_ppm <= 1000:
        return "Moderate (Ventilation Suggested)"
    elif 1000 < co2_ppm <= 1500:
        return "High (Ventilation Needed)"
    else:
        return "Very High (Immediate Ventilation Required)"

# Print real-time CO₂ level information
co2_status = interpret_co2_level(average_co2_ppm)
print(f"Real-time Carbon Dioxide (CO₂) level (ppm): {average_co2_ppm:.2f}")
print(f"Carbon Dioxide (CO₂) Status: {co2_status}")
print(f"Real-time prediction (1=high CO₂, 0=normal): {new_label}")
