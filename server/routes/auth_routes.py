from flask import Blueprint, jsonify, request
from models.user import User
from extensions import db
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')

        if not username or not email or not password:
            return jsonify({'success': False, 'error': 'Username, email, and password are required'}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'error': 'Username already exists'}), 409

        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'error': 'Email already registered'}), 409

        user = User(
            username=username,
            email=email,
            first_name=data.get('first_name', '').strip(),
            last_name=data.get('last_name', '').strip(),
            phone=data.get('phone', '').strip()
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=str(user.id))

        return jsonify({
            'success': True,
            'data': user.to_dict(),
            'token': token
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
