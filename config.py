import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///co2_predictions.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Model configuration
    MODEL_PATH = "co2_keras_model_improved.keras"
    
    # Application configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here') 