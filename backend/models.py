from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    byte_balance = db.Column(db.Float, default=0.0)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    transactions_sent = db.relationship('Transaction', 
                                        foreign_keys='Transaction.sender_id', 
                                        backref='sender', 
                                        lazy='dynamic')
    transactions_received = db.relationship('Transaction', 
                                            foreign_keys='Transaction.recipient_id', 
                                            backref='recipient', 
                                            lazy='dynamic')

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'sender_username': self.sender.username,
            'recipient_username': self.recipient.username,
            'amount': self.amount,
            'timestamp': self.timestamp.isoformat(),
            'description': self.description
        }
