import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database configuration - Force SQLite for free deployment
    database_url = os.getenv('DATABASE_URL', 'sqlite:///co2_predictions.db')
    if database_url.startswith('postgres://'):
        database_url = 'sqlite:///co2_predictions.db'
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Model configuration
    MODEL_PATH = "co2_keras_model_improved.keras"
    
    # Application configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'co2-detection-secret-key-2024') 