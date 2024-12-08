from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User, Transaction
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)

# Create tables
with app.app_context():
    db.create_all()
    # Create admin user if not exists
    admin_username = app.config['ADMIN_USERNAME']
    admin_password = app.config['ADMIN_PASSWORD']
    
    existing_admin = User.query.filter_by(username=admin_username, is_admin=True).first()
    if not existing_admin:
        hashed_password = bcrypt.generate_password_hash(admin_password).decode('utf-8')
        admin_user = User(
            username=admin_username, 
            email=f'{admin_username}@bytecurrency.com', 
            password=hashed_password, 
            is_admin=True,
            byte_balance=1000000  # Initial admin balance
        )
        db.session.add(admin_user)
        db.session.commit()

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Validate input
    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    # Hash password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    # Create new user
    new_user = User(
        username=username, 
        email=email, 
        password=hashed_password,
        byte_balance=100.0  # Initial signup bonus
    )
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully", "username": username}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token, is_admin=user.is_admin), 200
    
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/transfer', methods=['POST'])
@jwt_required()
def transfer_bytes():
    current_username = get_jwt_identity()
    sender = User.query.filter_by(username=current_username).first()
    
    data = request.get_json()
    recipient_username = data.get('recipient')
    amount = float(data.get('amount'))
    description = data.get('description', 'Transfer')

    if not sender or amount <= 0:
        return jsonify({"error": "Invalid transfer"}), 400

    recipient = User.query.filter_by(username=recipient_username).first()
    
    if not recipient:
        return jsonify({"error": "Recipient not found"}), 404

    if sender.byte_balance < amount:
        return jsonify({"error": "Insufficient balance"}), 400

    # Perform transfer
    sender.byte_balance -= amount
    recipient.byte_balance += amount

    # Record transaction
    transaction = Transaction(
        sender_id=sender.id, 
        recipient_id=recipient.id, 
        amount=amount,
        description=description
    )
    
    db.session.add(transaction)
    db.session.commit()

    return jsonify({
        "message": "Transfer successful", 
        "new_balance": sender.byte_balance
    }), 200

@app.route('/admin/adjust_balance', methods=['POST'])
@jwt_required()
def admin_adjust_balance():
    current_username = get_jwt_identity()
    admin_user = User.query.filter_by(username=current_username, is_admin=True).first()
    
    if not admin_user:
        return jsonify({"error": "Admin access required"}), 403

    data = request.get_json()
    target_username = data.get('username')
    adjustment_amount = float(data.get('amount'))
    
    target_user = User.query.filter_by(username=target_username).first()
    
    if not target_user:
        return jsonify({"error": "User not found"}), 404

    # Adjust balance
    target_user.byte_balance += adjustment_amount
    
    # Record admin transaction
    transaction = Transaction(
        sender_id=admin_user.id, 
        recipient_id=target_user.id, 
        amount=adjustment_amount,
        description='Admin Balance Adjustment'
    )
    
    db.session.add(transaction)
    db.session.commit()

    return jsonify({
        "message": "Balance adjusted successfully", 
        "new_balance": target_user.byte_balance
    }), 200

@app.route('/transactions', methods=['GET'])
@jwt_required()
def get_user_transactions():
    current_username = get_jwt_identity()
    user = User.query.filter_by(username=current_username).first()
    
    sent_transactions = [t.to_dict() for t in user.transactions_sent]
    received_transactions = [t.to_dict() for t in user.transactions_received]
    
    return jsonify({
        "sent_transactions": sent_transactions,
        "received_transactions": received_transactions
    }), 200

@app.route('/balance', methods=['GET'])
@jwt_required()
def get_balance():
    current_username = get_jwt_identity()
    user = User.query.filter_by(username=current_username).first()
    
    return jsonify({"balance": user.byte_balance}), 200

if __name__ == '__main__':
    app.run(debug=True)
