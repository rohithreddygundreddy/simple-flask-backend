from flask import Flask, request, jsonify
from flask_cors import CORS
import database
from datetime import timedelta
import json
import uuid
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Simple token storage (in production, use a proper database)
active_tokens = {}

def create_token(user_id):
    """Create a simple token for authentication"""
    token = str(uuid.uuid4())
    expiry = time.time() + 24 * 3600  # 24 hours from now
    active_tokens[token] = {
        'user_id': user_id,
        'expiry': expiry
    }
    return token

def verify_token(token):
    """Verify if a token is valid"""
    if token in active_tokens:
        token_data = active_tokens[token]
        if time.time() < token_data['expiry']:
            return token_data['user_id']
        else:
            # Token expired, remove it
            del active_tokens[token]
    return None

@app.route('/')
def home():
    return jsonify({
        'message': 'Welcome to Simple Flask Backend',
        'endpoints': {
            'POST /register': 'Register a new user',
            'POST /login': 'Login with existing user',
            'GET /users': 'Get all users (for testing)',
            'GET /profile': 'Get current user profile (requires token in Authorization header)'
        }
    })

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Check required fields
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({
                'message': 'Username, email and password are required',
                'status': 'error'
            }), 400
        
        # Check password length
        if len(data['password']) < 6:
            return jsonify({
                'message': 'Password must be at least 6 characters',
                'status': 'error'
            }), 400
        
        # Create new user
        user_id = database.add_user(
            data['username'],
            data['email'],
            data['password']
        )
        
        if user_id is None:
            return jsonify({
                'message': 'Username or email already exists',
                'status': 'error'
            }), 400
        
        # Generate token
        access_token = create_token(user_id)
        
        # Get user data
        user = database.get_user_by_id(user_id)
        
        return jsonify({
            'message': 'User created successfully',
            'status': 'success',
            'token': access_token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'created_at': user['created_at']
            }
        }), 201
        
    except Exception as e:
        return jsonify({
            'message': f'Server error: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # Check required fields
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({
                'message': 'Username and password are required',
                'status': 'error'
            }), 400
        
        # Find user
        user = database.get_user_by_username(data['username'])
        
        # Check user and password
        if not user or not database.verify_password(data['password'], user['password_hash']):
            return jsonify({
                'message': 'Invalid username or password',
                'status': 'error'
            }), 401
        
        # Generate token
        access_token = create_token(user['id'])
        
        return jsonify({
            'message': 'Login successful',
            'status': 'success',
            'token': access_token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'created_at': user['created_at']
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'message': f'Server error: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = database.get_all_users()
        return jsonify({
            'users': users,
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({
            'message': f'Server error: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/profile', methods=['GET'])
def get_profile():
    try:
        # Check for token in header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'message': 'Missing or invalid Authorization header',
                'status': 'error'
            }), 401
        
        token = auth_header.split(' ')[1]
        user_id = verify_token(token)
        
        if not user_id:
            return jsonify({
                'message': 'Invalid or expired token',
                'status': 'error'
            }), 401
        
        user = database.get_user_by_id(user_id)
        
        if not user:
            return jsonify({
                'message': 'User not found',
                'status': 'error'
            }), 404
        
        return jsonify({
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'created_at': user['created_at']
            },
            'status': 'success'
        }), 200
        
    except Exception as e:
        return jsonify({
            'message': f'Server error: {str(e)}',
            'status': 'error'
        }), 500

if __name__ == '__main__':
    print("Starting Flask server...")
    print("API endpoints available at:")
    print("  POST http://localhost:5000/register")
    print("  POST http://localhost:5000/login")
    print("  GET  http://localhost:5000/users")
    print("  GET  http://localhost:5000/profile (requires token in Authorization header)")
    print("\nPress Ctrl+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=5000)