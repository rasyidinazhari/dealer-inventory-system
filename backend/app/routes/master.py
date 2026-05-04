from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Customer, Branch, Brand, Category, User, VehicleModel, Branch

master_bp = Blueprint('master', __name__, url_prefix='/api/master')


# ==========================================
# 2. API MEREK & KATEGORI (Khusus Owner)
# ==========================================
@master_bp.route('/brands', methods=['GET'])
# @jwt_required()
def get_brands():
    brands = Brand.query.order_by(Brand.name).all()
    result = []
    for b in brands:
        result.append({
            'id': b.id, 
            'name': b.name,
            'models': [{'id': m.id, 'name': m.name} for m in b.models] # Include model
        })
    return jsonify({'status': 'success', 'data': result}), 200

@master_bp.route('/brands', methods=['POST'])
@jwt_required()
def create_brand():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    if user.role != 'super_admin':
        return jsonify({'message': 'Akses ditolak. Khusus Owner.'}), 403

    name = request.get_json().get('name')
    if Brand.query.filter_by(name=name).first():
        return jsonify({'status': 'error', 'message': 'Merek sudah ada'}), 400
    db.session.add(Brand(name=name))
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Merek ditambahkan'}), 201

@master_bp.route('/categories', methods=['GET'])
# @jwt_required()
def get_categories():
    categories = Category.query.all()
    return jsonify({'status': 'success', 'data': [{'id': c.id, 'name': c.name} for c in categories]}), 200

@master_bp.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    if user.role != 'super_admin':
        return jsonify({'message': 'Akses ditolak.'}), 403

    name = request.get_json().get('name')
    if Category.query.filter_by(name=name).first():
        return jsonify({'status': 'error', 'message': 'Kategori sudah ada'}), 400
    db.session.add(Category(name=name))
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Kategori ditambahkan'}), 201


# ==========================================
# 3. API CUSTOMERS (PELANGGAN)
# ==========================================
@master_bp.route('/customers', methods=['GET'])
@jwt_required()
def get_customers():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    
    # Filter cabang via query param (?branch_id=1)
    filter_branch_id = request.args.get('branch_id')
    
    query = Customer.query
    filter_branch = request.args.get('branch_id')
    
    # Jika admin_cabang, paksa filter hanya untuk cabangnya
    if user.role == 'admin_cabang':
        query = query.filter_by(branch_id=user.branch_id)
    elif user.role == 'super_admin' and filter_branch:
        query = query.filter_by(branch_id=filter_branch)

    customers = query.all()
    result = [{
        'id': c.id, 
        'nik': c.nik, 
        'full_name': c.full_name, 
        'phone_number': c.phone_number, 
        'address': c.address,
        'branch_id': c.branch_id,
        'branch_name': c.branch.name if c.branch else 'Unknown'
    } for c in customers]
    
    return jsonify({'status': 'success', 'data': result}), 200

@master_bp.route('/customers', methods=['POST'])
@jwt_required()
def create_customer():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    data = request.get_json()
    
    if not data or not data.get('nik') or not data.get('full_name'):
        return jsonify({'status': 'error', 'message': 'NIK dan Nama Lengkap wajib diisi'}), 400
    
    if Customer.query.filter_by(nik=data['nik']).first():
        return jsonify({'status': 'error', 'message': 'NIK sudah terdaftar'}), 400

    # Tentukan cabang
    target_branch = user.branch_id
    if user.role == 'super_admin' and data.get('branch_id'):
        target_branch = data.get('branch_id')

    new_customer = Customer(
        nik=data['nik'],
        full_name=data['full_name'],
        phone_number=data.get('phone_number', ''),
        address=data.get('address', ''),
        branch_id=target_branch
    )
    db.session.add(new_customer)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Data pelanggan berhasil ditambahkan'}), 201

@master_bp.route('/customers/<int:id>', methods=['PUT'])
@jwt_required()
def update_customer(id):
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    
    customer = Customer.query.get_or_404(id)
    data = request.get_json()
    
    # Validasi Hak Akses Cabang
    if user.role == 'admin_cabang' and customer.branch_id != user.branch_id:
        return jsonify({'message': 'Akses ditolak. Pelanggan ini milik cabang lain.'}), 403

    if 'nik' in data: customer.nik = data['nik']
    if 'full_name' in data: customer.full_name = data['full_name']
    if 'phone_number' in data: customer.phone_number = data['phone_number']
    if 'address' in data: customer.address = data['address']
    
    # Update cabang (hanya Super Admin yang boleh)
    if 'branch_id' in data and user.role == 'super_admin':
        customer.branch_id = data['branch_id']
        
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Data pelanggan diupdate'}), 200

@master_bp.route('/customers/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_customer(id):
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    
    customer = Customer.query.get_or_404(id)
    
    # Validasi Hak Akses Cabang
    if user.role == 'admin_cabang' and customer.branch_id != user.branch_id:
        return jsonify({'message': 'Akses ditolak. Pelanggan ini milik cabang lain.'}), 403

    db.session.delete(customer)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Pelanggan dihapus'}), 200

# --- TAMBAHAN CRUD MEREK ---
@master_bp.route('/brands/<int:id>', methods=['PUT'])
@jwt_required()
def update_brand(id):
    brand = Brand.query.get_or_404(id)
    brand.name = request.get_json().get('name', brand.name)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Merek diupdate'})

@master_bp.route('/brands/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_brand(id):
    brand = Brand.query.get_or_404(id)
    db.session.delete(brand)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Merek dihapus'})

# --- TAMBAHAN CRUD KATEGORI ---
@master_bp.route('/categories/<int:id>', methods=['PUT'])
@jwt_required()
def update_category(id):
    cat = Category.query.get_or_404(id)
    cat.name = request.get_json().get('name', cat.name)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Kategori diupdate'})

@master_bp.route('/categories/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    cat = Category.query.get_or_404(id)
    db.session.delete(cat)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Kategori dihapus'})

# ==========================================
# 3. API MODEL KENDARAAN
# ==========================================
@master_bp.route('/models', methods=['POST'])
@jwt_required()
def create_model():
    data = request.get_json()
    new_model = VehicleModel(name=data['name'], brand_id=data['brand_id'])
    db.session.add(new_model)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Model ditambahkan'}), 201

@master_bp.route('/models/<int:id>', methods=['PUT'])
@jwt_required()
def update_model(id):
    v_model = VehicleModel.query.get_or_404(id)
    v_model.name = request.get_json().get('name', v_model.name)
    db.session.commit()
    return jsonify({'status': 'success'})

@master_bp.route('/models/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_model(id):
    v_model = VehicleModel.query.get_or_404(id)
    db.session.delete(v_model)
    db.session.commit()
    return jsonify({'status': 'success'})

# 1. READ ALL BRANCHES (Ini sepertinya sudah ada)
@master_bp.route('/branches', methods=['GET'])
def get_branches():
    branches = Branch.query.all()
    result = [{'id': b.id, 'name': b.name, 'address': getattr(b, 'address', ''), 'phone': getattr(b, 'phone', '')} for b in branches]
    return jsonify({'status': 'success', 'data': result}), 200

# 2. CREATE BRANCH
@master_bp.route('/branches', methods=['POST'])
@jwt_required()
def create_branch():
    data = request.get_json()
    
    # Pastikan data ada
    if not data or not data.get('name'):
        return jsonify({'status': 'error', 'message': 'Nama cabang wajib diisi'}), 400
        
    try:
        new_branch = Branch(
            name=data['name'],
            address=data.get('address', ''), # Gunakan .get() agar tidak error jika kosong
            phone=data.get('phone', '')
        )
        db.session.add(new_branch)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Cabang berhasil dibuat'}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}") # Cek error spesifik di terminal backend
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan pada server'}), 500

# 3. UPDATE BRANCH
@master_bp.route('/branches/<int:id>', methods=['PUT'])
@jwt_required()
def update_branch(id):
    branch = Branch.query.get_or_404(id)
    data = request.get_json()
    
    if 'name' in data: branch.name = data['name']
    if 'address' in data: branch.address = data['address']
    if 'phone' in data: branch.phone = data['phone']
    
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Cabang berhasil diupdate'}), 200

# 4. DELETE BRANCH
@master_bp.route('/branches/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_branch(id):
    branch = Branch.query.get_or_404(id)
    # Catatan: Hati-hati menghapus cabang jika relasinya tidak diatur dengan 'cascade' di database
    db.session.delete(branch)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Cabang berhasil dihapus'}), 200