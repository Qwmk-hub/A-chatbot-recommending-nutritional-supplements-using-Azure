from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# user.py에서 이미 db를 정의했으므로 import
from src.models.user import db

class Supplement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=False)  # 'trending', 'male', 'female'
    age_group = db.Column(db.String(20), nullable=True)  # '20s', '30s', '40s', '50s+'
    benefits = db.Column(db.Text, nullable=True)  # JSON string으로 저장
    price_range = db.Column(db.String(20), nullable=True)
    brand = db.Column(db.String(50), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    is_trending = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Supplement {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'age_group': self.age_group,
            'benefits': self.benefits,
            'price_range': self.price_range,
            'brand': self.brand,
            'image_url': self.image_url,
            'is_trending': self.is_trending,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

