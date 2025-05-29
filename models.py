from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    co2_levels = db.Column(db.JSON, nullable=False)
    prediction_ppm = db.Column(db.Float, nullable=False)
    prediction_percentage = db.Column(db.Float, nullable=False)
    prediction_level = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'co2_levels': self.co2_levels,
            'prediction_ppm': self.prediction_ppm,
            'prediction_percentage': self.prediction_percentage,
            'prediction_level': self.prediction_level,
            'timestamp': self.timestamp.isoformat()
        } 