from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity # <-- Ditambahkan get_jwt_identity
from werkzeug.security import generate_password_hash
from app.models import db, User
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash

# Inisialisasi Blueprint
users_bp = Blueprint('users', __name__, url_prefix='/api/users')
seller_bp = Blueprint('sellers', __name__, url_prefix='/api/sellers')

@seller_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_sellers():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    
    # Hanya Admin dan CS yang boleh melihat data kontak seller
    if user.role not in ['super_admin', 'cs', 'finance', 'admin_cabang']:
        return jsonify({'message': 'Akses ditolak'}), 403

    query = User.query.filter_by(role='seller')

    # ==========================================
    # LOGIKA FILTER CABANG
    # ==========================================
    filter_branch = request.args.get('branch_id')
    
    if user.role == 'admin_cabang':
        # Jika yang login admin cabang, paksa hanya lihat seller di cabangnya
        query = query.filter_by(branch_id=user.branch_id)
    elif user.role == 'super_admin' and filter_branch:
        # Jika Super Admin dan memilih cabang di Navbar, filter sesuai pilihan
        query = query.filter_by(branch_id=filter_branch)

    # Ambil semua user yang memiliki role 'seller'
    sellers = query.order_by(User.created_at.desc()).all()
    
    # ... (kode di atasnya tetap sama)

    result = []
    for s in sellers:
        # Hitung statistik motor titipan seller ini
        total_motors = len(s.motorcycles)
        active_motors = len([m for m in s.motorcycles if m.is_active])
        
        # --- TAMBAHKAN BARIS INI UNTUK NAMA CABANG ---
        branch_name = s.branch.name if s.branch else 'Pusat / Belum Diatur'
        
        result.append({
            'id': s.id,
            'username': s.username,
            'full_name': getattr(s, 'full_name', s.username),
            'phone_number': getattr(s, 'phone_number', '-'),
            'total_motors': total_motors,
            'active_motors': active_motors,
            'branch_name': branch_name, # <--- Tambahkan field ini
            'joined_at': s.created_at.strftime("%d %b %Y")
        })

    return jsonify({'status': 'success', 'data': result}), 200

# 1. READ ALL (Mendapatkan semua daftar akun)
@users_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    result = []
    for u in users:
        result.append({
            'id': u.id,
            'username': u.username,
            'role': u.role,
            'branch_id': getattr(u, 'branch_id', None),
            # --- TAMBAHKAN DUA BARIS INI ---
            'full_name': getattr(u, 'full_name', ''), 
            'phone_number': getattr(u, 'phone_number', ''),
            # -------------------------------
            'created_at': u.created_at.isoformat() if u.created_at else None
        })
    return jsonify({'status': 'success', 'data': result}), 200

# 2. CREATE (Menambahkan akun baru)
@users_bp.route('/', methods=['POST'])
@jwt_required()
def create_user():
    data = request.get_json()
    
    # Validasi input kosong
    if not data or not data.get('username') or not data.get('password') or not data.get('role'):
        return jsonify({'status': 'error', 'message': 'Data tidak lengkap. Username, Password, dan Role wajib diisi.'}), 400
        
    # Validasi jika username sudah dipakai
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'status': 'error', 'message': 'Username tersebut sudah digunakan, silakan pilih yang lain.'}), 400

    # Tentukan branch_id (kosongkan jika Super Admin atau Seller)
    branch_id = data.get('branch_id')
    if data['role'] in ['super_admin']:
        branch_id = None

    new_user = User(
        username=data['username'],
        password_hash=generate_password_hash(data['password']),
        role=data['role'],
        branch_id=branch_id,
        # --- TAMBAHKAN DUA BARIS INI ---
        full_name=data.get('full_name', ''),
        phone_number=data.get('phone_number', '')
        # -------------------------------
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Akun berhasil dibuat.'}), 201

# 3. UPDATE (Mengedit akun, misalnya ganti divisi atau reset password)
@users_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()

    # Update role (divisi) jika ada
    if 'role' in data:
        user.role = data['role']
        
    # Update branch_id jika ada
    if 'branch_id' in data:
        user.branch_id = data['branch_id']
        
    # Pastikan branch_id di-null-kan jika role diubah ke super_admin atau seller
    if user.role in ['super_admin']:
        user.branch_id = None

    if 'full_name' in data:
        user.full_name = data['full_name']
    if 'phone_number' in data:
        user.phone_number = data['phone_number']
        
    # Update password HANYA JIKA field password dikirim dan tidak kosong
    if 'password' in data and data['password'].strip() != '':
        user.password_hash = generate_password_hash(data['password'])

    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Data akun berhasil diupdate.'}), 200

# 4. DELETE (Menghapus akun karyawan)
@users_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Akun berhasil dihapus permanen.'}), 200

# ==========================================
# UPDATE PROFILE (KHUSUS USER LOGIN)
# ==========================================
@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    
    return jsonify({
        'status': 'success',
        'data': {
            'username': user.username,
            'full_name': getattr(user, 'full_name', ''),
            'phone_number': getattr(user, 'phone_number', ''),
            'branch_id': getattr(user, 'branch_id', ''),
            'role': user.role
        }
    }), 200

@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    data = request.get_json()

    # 1. Update Data Profil Dasar
    if 'full_name' in data: 
        user.full_name = data['full_name']
    if 'phone_number' in data: 
        user.phone_number = data['phone_number']
        
    # Seller boleh ganti cabang penempatan mereka
    if 'branch_id' in data and user.role == 'seller': 
        user.branch_id = data['branch_id']

    # 2. Update Password (dengan verifikasi)
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if old_password and new_password:
        # Cek apakah password lama cocok dengan di database
        if not check_password_hash(user.password_hash, old_password):
            return jsonify({'status': 'error', 'message': 'Password lama yang Anda masukkan salah.'}), 400
        
        # Jika cocok, hash password baru dan simpan
        user.password_hash = generate_password_hash(new_password)

    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Profil berhasil diperbarui!'}), 200