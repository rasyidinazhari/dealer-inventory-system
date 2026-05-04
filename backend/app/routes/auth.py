from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt # <-- Tambahkan get_jwt
from werkzeug.security import check_password_hash
from app.models import User, db
import datetime
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'status': 'error', 'message': 'Username dan password wajib diisi'}), 400

    username = data.get('username')
    password = data.get('password')

    # Cari user di database
    user = User.query.filter_by(username=username).first()

    # Validasi user dan password
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'status': 'error', 'message': 'Username atau password salah'}), 401

    expires = datetime.timedelta(days=1)
    
    # --- PERBAIKAN DI SINI ---
    # Pisahkan identitas utama (string) dan data tambahan (dictionary)
    access_token = create_access_token(
        identity=str(user.id),  # Harus berupa String
        additional_claims={     # Data dictionary dimasukkan ke sini
            'username': user.username,
            'role': user.role
        },
        expires_delta=expires
    )

    return jsonify({
        'status': 'success',
        'message': 'Login berhasil',
        'data': {
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'role': user.role
            }
        }
    }), 200

# Endpoint untuk mengetes apakah token valid
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    # Ambil identity (berupa ID string yang kita set di atas)
    current_user_id = get_jwt_identity()
    
    # Ambil data tambahan (role, username) menggunakan get_jwt()
    claims = get_jwt()

    return jsonify({
        'status': 'success',
        'data': {
            'id': current_user_id,
            'username': claims.get('username'),
            'role': claims.get('role')
        }
    }), 200

# Contoh di endpoint tempat kamu membuat user baru
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validasi input dasar
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Data tidak lengkap'}), 400
        
    # Cek apakah username sudah ada
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username sudah digunakan'}), 400

    # Ambil branch_id (Wajib untuk Seller, opsional untuk role lain)
    branch_id = data.get('branch_id')
    role = data.get('role', 'seller') # Default role

    new_user = User(
        username=data['username'],
        password_hash=generate_password_hash(data['password']),
        role=role,
        branch_id=int(branch_id) if branch_id else None,
        
        # --- TAMBAHKAN DUA BARIS INI ---
        full_name=data.get('full_name', ''), 
        phone_number=data.get('phone_number', '')
        # -------------------------------
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Pendaftaran berhasil'}), 201