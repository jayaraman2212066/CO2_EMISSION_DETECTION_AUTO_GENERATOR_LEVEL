#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # exit on error

pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

# Verify TensorFlow installation
python -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__)"

# Verify model file exists
python -c "import os; print('Model file exists:', os.path.exists('co2_keras_model_improved.keras'))"

# Test model loading with fallback
python -c "
try:
    from tensorflow.keras.models import load_model
    model = load_model('co2_keras_model_improved.keras', compile=False)
    print('Model loaded successfully for deployment')
except Exception as e:
    print(f'Model loading warning: {e}')
    print('Will use fallback model during runtime')
"