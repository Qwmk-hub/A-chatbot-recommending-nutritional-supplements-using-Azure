from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10), nullable=False)  # 'male' or 'female'
    age = db.Column(db.Integer, nullable=False)
    interested_supplements = db.Column(db.Text, nullable=True)  # JSON string으로 저장
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """비밀번호를 해시화하여 저장"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """비밀번호 확인"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'gender': self.gender,
            'age': self.age,
            'interested_supplements': self.interested_supplements,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
