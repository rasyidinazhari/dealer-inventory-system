import os
import time
import uuid
import json
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Motorcycle, MotorcycleGallery, User, Brand, Wishlist
from sqlalchemy import text, or_, func

inventory_bp = Blueprint('inventory', __name__, url_prefix='/api/inventory')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'webp'}

# ==========================================
# BAGIAN 1: KATALOG & ADMIN DEALER 
# ==========================================

# 1. READ ALL (Dengan Fitur Search & Filter Cabang)
@inventory_bp.route('/', methods=['GET'])
@jwt_required(optional=True) # Bisa diakses publik
def get_all_motorcycles():
    query = Motorcycle.query
    
    # A. Filter by Search Query
    search_query = request.args.get('q', '').strip()
    if search_query:
        query = query.filter(Motorcycle.model_name.ilike(f"%{search_query.lower()}%"))

    # B. Filter by Branch (Untuk Owner / Admin Panel)
    current_user_id = get_jwt_identity()
    if current_user_id:
        user = User.query.get(int(current_user_id))
        filter_branch = request.args.get('branch_id')
        
        if user.role == 'admin_cabang':
            query = query.filter_by(branch_id=user.branch_id)
        elif user.role == 'super_admin' and filter_branch:
            query = query.filter_by(branch_id=filter_branch)

    # C. Filter Sumber (Abu Motor vs Seller Eksternal)
    source = request.args.get('source')
    if source == 'internal':
        query = query.filter(Motorcycle.seller_id.is_(None))
    elif source == 'external':
        query = query.filter(Motorcycle.seller_id.isnot(None))

    motorcycles = query.order_by(Motorcycle.created_at.desc()).all()
    
    result = []
    for motor in motorcycles:
        owner_name = motor.seller_user.username if motor.seller_user else 'Abu Motor'
        
        # Cek Usia Stok (> 2 bulan)
        is_overstock = False
        if motor.incoming_date:
            age_days = (datetime.utcnow().date() - motor.incoming_date).days
            if age_days > 60:
                is_overstock = True

        galleries = MotorcycleGallery.query.filter_by(motorcycle_id=motor.id).all()
        gallery_urls = [g.image_url for g in galleries]        

        result.append({
            'id': motor.id,
            'sku_code': motor.sku_code,
            'vehicle_type': motor.vehicle_type, 
            'condition': motor.condition,       
            'brand': motor.brand_rel.name if motor.brand_rel else 'Unknown',
            'model_name': motor.model_name,
            'category': motor.category_rel.name if motor.category_rel else 'Unknown',
            'color': motor.color,
            'transmission': motor.transmission,
            'year': motor.year,
            
            # --- TAMBAHKAN BARIS INI AGAR TIDAK HILANG SAAT DI-EDIT ---
            'mileage': motor.mileage,
            'body_type': motor.body_type,
            'engine_capacity': motor.engine_capacity,
            'features': motor.features,
            'documents': motor.documents,
            'description': motor.description,
            # ---------------------------------------------------------
            
            'incoming_date': motor.incoming_date.strftime("%Y-%m-%d") if motor.incoming_date else None,
            'capital_price': float(motor.capital_price or 0),
            'repair_cost': float(motor.repair_cost or 0),
            'price': float(motor.price or 0),
            'stock': motor.stock,
            'is_active': motor.is_active,
            'approval_status': motor.approval_status,
            'image_url': motor.image_url,
            'gallery': gallery_urls,
            'seller_name': owner_name,
            'branch_id': motor.branch_id,
            'branch_name': motor.branch.name if motor.branch else 'Unknown',
            'is_overstock': is_overstock
        })
    return jsonify({'status': 'success', 'data': result}), 200

# 2. READ DETAIL (Untuk Halaman Detail Kendaraan Publik)
@inventory_bp.route('/<int:id>', methods=['GET'])
@jwt_required(optional=True) # Bebas diakses publik tanpa login
def get_motorcycle_detail(id):
    motor = Motorcycle.query.get_or_404(id)
    
    # Ambil semua foto galeri tambahan (jika ada)
    galleries = MotorcycleGallery.query.filter_by(motorcycle_id=motor.id).all()
    gallery_urls = [g.image_url for g in galleries]
    
    # Format data agar sesuai dengan permintaan Frontend
    result = {
        'id': motor.id,
        'sku_code': motor.sku_code,
        'vehicle_type': motor.vehicle_type, 
        'condition': motor.condition,       
        'brand': motor.brand_rel.name if motor.brand_rel else 'Unknown',
        'model_name': motor.model_name,
        'category': motor.category_rel.name if motor.category_rel else 'Unknown',
        'color': motor.color,
        'transmission': motor.transmission,
        'year': motor.year,
        'mileage': motor.mileage,
        'body_type': motor.body_type,
        'engine_capacity': motor.engine_capacity,
        'features': motor.features,
        'documents': motor.documents,
        'price': float(motor.price or 0),
        'stock': motor.stock,
        'description': motor.description,
        'image_url': motor.image_url,
        'gallery': gallery_urls, # <-- INI TAMBAHANNYA
        'branch_name': motor.branch.name if motor.branch else 'Unknown'
    }
    
    return jsonify({'status': 'success', 'data': result}), 200

# 3. CREATE (Admin Tambah Internal - Termasuk Multi Foto, Modal & Perbaikan)
@inventory_bp.route('/', methods=['POST'])
@jwt_required()
def create_motorcycle():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    if user.role not in ['super_admin', 'cs', 'admin_cabang']:
        return jsonify({'message': 'Akses ditolak.'}), 403

    data = request.form
    
    # Validasi Cabang (Mencegah bug FormData "null")
    target_branch = user.branch_id
    if user.role == 'super_admin':
        target_branch = data.get('branch_id')
        if not target_branch or str(target_branch).lower() in ['null', 'undefined', '']:
             return jsonify({'message': 'Super Admin harus memilih cabang.'}), 400

    # 1. Handle Foto Utama
    image_file = request.files.get('image')
    image_url = None
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)

    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        unique_filename = f"main_{int(time.time())}_{filename}"
        filepath = os.path.join(upload_folder, unique_filename)
        image_file.save(filepath)
        image_url = f"/static/uploads/{unique_filename}"

    # Parsing Tanggal Masuk
    in_date = datetime.utcnow().date()
    if data.get('incoming_date'):
        in_date = datetime.strptime(data.get('incoming_date'), '%Y-%m-%d').date()

    # Buat Kendaraan
    new_motor = Motorcycle(
        sku_code=data.get('sku_code'),
        branch_id=target_branch,
        vehicle_type=data.get('vehicle_type', 'Motor'),
        condition=data.get('condition', 'Bekas'),
        brand_id=int(data.get('brand_id')) if data.get('brand_id') else None,
        category_id=int(data.get('category_id')) if data.get('category_id') else None,
        model_name=data.get('model_name'),
        color=data.get('color'),
        transmission=data.get('transmission', 'Otomatis'),
        year=int(data.get('year', 0)) if data.get('year') else None,
        
        # --- INI YANG SEBELUMNYA TERTINGGAL ---
        mileage=data.get('mileage', '0 (Baru)'),
        body_type=data.get('body_type', ''),
        engine_capacity=data.get('engine_capacity', ''),
        features=data.get('features', ''),
        documents=data.get('documents', ''),
        # --------------------------------------
        
        incoming_date=in_date,
        capital_price=float(data.get('capital_price', 0)),
        repair_cost=float(data.get('repair_cost', 0)),
        price=float(data.get('price', 0)),
        stock=int(data.get('stock', 0)),
        description=data.get('description', ''),
        is_active=str(data.get('is_active', 'true')).lower() == 'true',
        approval_status='approved',
        image_url=image_url
    )
    db.session.add(new_motor)
    db.session.flush() # Ambil ID motor tanpa commit dulu

    # 2. Handle Multiple Foto (Gallery max 9)
    gallery_files = request.files.getlist('gallery')
    for g_file in gallery_files[:9]: 
        if g_file and allowed_file(g_file.filename):
            g_filename = secure_filename(g_file.filename)
            g_unique = f"gal_{int(time.time())}_{g_filename}"
            g_filepath = os.path.join(upload_folder, g_unique)
            g_file.save(g_filepath)
            
            db.session.add(MotorcycleGallery(
                motorcycle_id=new_motor.id,
                image_url=f"/static/uploads/{g_unique}"
            ))

    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Kendaraan & Galeri berhasil ditambahkan'}), 201


# 4. UPDATE (Admin Edit)
@inventory_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_motorcycle(id):
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    if user.role not in ['super_admin', 'cs', 'admin_cabang']:
        return jsonify({'message': 'Akses ditolak.'}), 403

    motor = Motorcycle.query.get_or_404(id)
    data = request.form
    
    # Update Foto Utama
    image_file = request.files.get('image')
    if 'sku_code' in data: motor.sku_code = data.get('sku_code')
    if 'branch_id' in data and data.get('branch_id'): motor.branch_id = int(data.get('branch_id'))
    if 'vehicle_type' in data: motor.vehicle_type = data.get('vehicle_type')
    if 'condition' in data: motor.condition = data.get('condition')
    if 'stock' in data: motor.stock = int(data.get('stock'))
    
    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        unique_filename = f"main_{int(time.time())}_{filename}"
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, unique_filename)
        image_file.save(filepath)
        motor.image_url = f"/static/uploads/{unique_filename}"

    # Update Kolom Baru (Pastikan mengkonversi tipe data jika ada isinya)
    if data.get('vehicle_type'): motor.vehicle_type = data.get('vehicle_type')
    if data.get('condition'): motor.condition = data.get('condition')
    
    # Perbaikan Relasi Master Data
    if data.get('brand_id') and data.get('brand_id') not in ['null', '', 'undefined']: 
        motor.brand_id = int(data.get('brand_id'))
    if data.get('category_id') and data.get('category_id') not in ['null', '', 'undefined']: 
        motor.category_id = int(data.get('category_id'))
    if data.get('branch_id') and data.get('branch_id') not in ['null', '', 'undefined']: 
        motor.branch_id = int(data.get('branch_id'))
    
    if data.get('model_name') and data.get('model_name') not in ['null', 'undefined']: 
        motor.model_name = data.get('model_name')
        
    motor.color = data.get('color', motor.color)
    motor.transmission = data.get('transmission', motor.transmission)
    
    if data.get('year') and data.get('year') not in ['null', '', 'undefined']: 
        motor.year = int(data.get('year'))
        
    motor.mileage = data.get('mileage', motor.mileage)
    motor.body_type = data.get('body_type', motor.body_type)
    motor.engine_capacity = data.get('engine_capacity', motor.engine_capacity)
    motor.features = data.get('features', motor.features)
    motor.documents = data.get('documents', motor.documents)
    
    # Perbaikan Angka Uang & Stok
    if data.get('capital_price') and data.get('capital_price') != 'null': 
        motor.capital_price = float(data.get('capital_price'))
    if data.get('repair_cost') and data.get('repair_cost') != 'null': 
        motor.repair_cost = float(data.get('repair_cost'))
    if data.get('price') and data.get('price') != 'null': 
        motor.price = float(data.get('price'))
    if data.get('stock') and data.get('stock') != 'null': 
        motor.stock = int(data.get('stock'))
    
    if data.get('description') and data.get('description') != 'null':
        motor.description = data.get('description')
    
    if 'is_active' in data:
        motor.is_active = str(data.get('is_active')).lower() == 'true'

    # ==========================================
    # LOGIKA UPDATE FOTO GALERI TAMBAHAN
    # ==========================================
    gallery_files = request.files.getlist('gallery')
    kept_galleries_str = request.form.get('kept_galleries', '[]')
    kept_galleries = json.loads(kept_galleries_str)

    old_galleries = MotorcycleGallery.query.filter_by(motorcycle_id=motor.id).all()
    for og in old_galleries:
        if og.image_url not in kept_galleries:
            db.session.delete(og)
    
    # Cek apakah ada file galeri yang ikut dikirim dan tidak kosong
    if gallery_files and len(gallery_files) > 0:
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        for file in gallery_files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"gal_{int(time.time())}_{uuid.uuid4().hex[:8]}_{filename}"
                filepath = os.path.join(upload_folder, unique_filename)
                
                file.save(filepath)
                
                new_gallery = MotorcycleGallery(
                    motorcycle_id=motor.id,
                    image_url=f"/static/uploads/{unique_filename}"
                )
                db.session.add(new_gallery)

    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Data berhasil diupdate'}), 200
# (Catatan: Fungsi UPDATE, DELETE, dan SELLER bisa disesuaikan dengan pola relasi yang sama. Untuk menghemat ruang chat, pastikan struktur filter branch_id dan relasi brand/category diterapkan jika mengedit fungsi tersebut).

# ==========================================
# BAGIAN 2: SELLER EKSTERNAL (TITIP JUAL)
# ==========================================

# A. Ambil Daftar Motor Milik Seller
@inventory_bp.route('/seller/motors', methods=['GET'])
@jwt_required()
def get_seller_motors():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    
    # Ambil motor yang hanya dimiliki oleh seller yang sedang login
    motors = Motorcycle.query.filter_by(seller_id=user.id).order_by(Motorcycle.created_at.desc()).all()
    
    result = []
    for motor in motors:
        result.append({
            'id': motor.id,
            'sku_code': motor.sku_code,
            'vehicle_type': motor.vehicle_type,
            'brand': motor.brand_rel.name if motor.brand_rel else 'Unknown',
            'model_name': motor.model_name,
            'category': motor.category_rel.name if motor.category_rel else 'Unknown',
            'year': motor.year,
            'price': float(motor.price or 0),
            'base_price': float(motor.base_price or 0), # Harga yang diminta seller
            'stock': motor.stock,
            'is_active': motor.is_active,
            'approval_status': motor.approval_status,
            'rejection_reason': motor.rejection_reason,
            'image_url': motor.image_url,
            'created_at': motor.created_at.strftime("%Y-%m-%d %H:%M") if motor.created_at else '-',

        })
        
    return jsonify({'status': 'success', 'data': result}), 200


# B. Seller Mengajukan Motor Baru
@inventory_bp.route('/seller/motors', methods=['POST'])
@jwt_required()
def submit_seller_motor():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    
    data = request.form
    submit_seller_motor


    
    # 1. Handle Foto Utama
    image_file = request.files.get('image')
    image_url = None
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)

    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        unique_filename = f"seller_main_{int(time.time())}_{filename}"
        filepath = os.path.join(upload_folder, unique_filename)
        image_file.save(filepath)
        image_url = f"/static/uploads/{unique_filename}"

    # Setup Harga Dasar (Harga yang diinginkan seller)
    base_price = float(data.get('base_price', 0))

    target_branch = user.branch_id if user.branch_id else 1

    # 2. Buat Record Kendaraan (Status: Pending)
    new_motor = Motorcycle(
        sku_code=f"SELL-{int(time.time())}",
        branch_id=target_branch, # Default dimasukkan ke Cabang Pusat sementara
        vehicle_type=data.get('vehicle_type', 'Motor'),
        condition=data.get('condition', 'Bekas'),
        
        # Konversi ke integer jika ada
        brand_id=int(data.get('brand_id')) if data.get('brand_id') else None,
        category_id=int(data.get('category_id')) if data.get('category_id') else None,
        
        model_name=data.get('model_name'),
        color=data.get('color'),
        transmission=data.get('transmission', 'Otomatis'),
        year=int(data.get('year', 0)) if data.get('year') else None,
        mileage=data.get('mileage', '0'),
        body_type=data.get('body_type', ''),
        engine_capacity=data.get('engine_capacity', ''),
        features=data.get('features', ''),
        documents=data.get('documents', ''),
        
        # Harga & Status untuk Titip Jual
        base_price=base_price,
        price=0, # Harga jual akhir ditentukan Admin saat disetujui
        capital_price=base_price, # Harga patokan modal = setoran ke seller
        
        stock=int(data.get('stock', 1)), 
        description=data.get('description', ''),
        is_active=False, # Disembunyikan dari katalog publik
        approval_status='pending', # Menunggu persetujuan Admin
        seller_id=user.id, # Ditautkan ke akun Seller
        image_url=image_url
    )
    db.session.add(new_motor)
    db.session.flush() # Ambil ID tanpa di-commit penuh

    # 3. Handle Multiple Foto Galeri
    gallery_files = request.files.getlist('gallery')
    for g_file in gallery_files[:9]:
        if g_file and allowed_file(g_file.filename):
            g_filename = secure_filename(g_file.filename)
            g_unique = f"seller_gal_{int(time.time())}_{g_filename}"
            g_filepath = os.path.join(upload_folder, g_unique)
            g_file.save(g_filepath)
            
            db.session.add(MotorcycleGallery(
                motorcycle_id=new_motor.id,
                image_url=f"/static/uploads/{g_unique}"
            ))

    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Pengajuan berhasil dikirim! Menunggu persetujuan Admin.'}), 201

# ==========================================
# BAGIAN 3: ADMIN VALIDASI (TITIP JUAL EKSTERNAL)
# ==========================================

# A. Ambil Semua Daftar Pengajuan (Pending)
@inventory_bp.route('/pending', methods=['GET'])
@jwt_required()
def get_pending_motors():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    
    # Hanya manajemen yang bisa melihat daftar antrean
    if user.role not in ['super_admin', 'cs', 'admin_cabang']:
        return jsonify({'message': 'Akses ditolak.'}), 403
    
    query = Motorcycle.query.filter_by(approval_status='pending')

    filter_branch = request.args.get('branch_id')

    if user.role == 'admin_cabang':
        # Admin cabang HANYA melihat pengajuan di cabangnya sendiri
        query = query.filter_by(branch_id=user.branch_id)
    elif user.role == 'super_admin' and filter_branch:
        # Super Admin bisa memfilter berdasarkan dropdown Navbar
        query = query.filter_by(branch_id=filter_branch)

    # Ambil semua motor yang statusnya masih 'pending'
    motors = query.order_by(Motorcycle.created_at.desc()).all()
    
    result = []
    for motor in motors:
        # Ambil data seller untuk ditampilkan ke Admin
        seller_name = motor.seller_user.full_name or motor.seller_user.username if motor.seller_user else 'Unknown'
        seller_phone = motor.seller_user.phone_number if motor.seller_user else '-'
        
        # --- CARA BARU AMBIL GALERI (EKSPLISIT & PASTI BERHASIL) ---
        galleries = MotorcycleGallery.query.filter_by(motorcycle_id=motor.id).all()
        gallery_urls = [g.image_url for g in galleries]
        # -----------------------------------------------------------
        
        result.append({
            'id': motor.id,
            'sku_code': motor.sku_code,
            'vehicle_type': motor.vehicle_type,
            'brand': motor.brand_rel.name if motor.brand_rel else 'Unknown',
            'model_name': motor.model_name,
            'year': motor.year,
            'base_price': float(motor.base_price or 0),
            'seller_name': seller_name,
            'seller_phone': seller_phone,
            'created_at': motor.created_at.strftime("%Y-%m-%d %H:%M"),
            
            # --- FOTO UTAMA & GALERI ---
            'image_url': motor.image_url,
            'gallery': gallery_urls, # <--- Masukkan array URL yang sudah di-query tadi
            
            'description': motor.description,
            'category': motor.category_rel.name if motor.category_rel else '-',
            'color': motor.color,
            'transmission': motor.transmission,
            'mileage': motor.mileage,
            'engine_capacity': motor.engine_capacity,
            'features': motor.features,
            'documents': motor.documents
        })
        
    return jsonify({'status': 'success', 'data': result}), 200


# B. Admin Menyetujui Pengajuan (Approve)
@inventory_bp.route('/<int:id>/approve', methods=['PUT'])
@jwt_required()
def approve_motor(id):
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    if user.role not in ['super_admin', 'cs', 'admin_cabang']:
        return jsonify({'message': 'Akses ditolak.'}), 403

    motor = Motorcycle.query.get_or_404(id)
    data = request.json
    
    # Ambil dealer_fee dari Vue (atau 0 jika tidak diisi)
    dealer_fee = float(data.get('dealer_fee', 0))

    # 1. Tentukan Harga Jual Akhir (Base Price + Dealer Fee)
    motor.dealer_fee = dealer_fee
    motor.price = float(motor.base_price or 0) + dealer_fee
    
    # Default Cabang ke Pusat jika tidak ditentukan
    if data.get('branch_id'):
        motor.branch_id = int(data.get('branch_id'))
    elif not motor.branch_id:
        motor.branch_id = 1 
        
    # 2. Ubah status menjadi disetujui dan tayangkan ke publik
    motor.approval_status = 'approved'
    motor.is_active = True 
    
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Kendaraan disetujui dan kini tayang di Katalog Publik!'}), 200


# C. Admin Menolak Pengajuan (Reject)
@inventory_bp.route('/<int:id>/reject', methods=['PUT'])
@jwt_required()
def reject_motor(id):
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    if user.role not in ['super_admin', 'cs', 'admin_cabang']:
        return jsonify({'message': 'Akses ditolak.'}), 403

    motor = Motorcycle.query.get_or_404(id)
    data = request.json
    
    # Ubah status dan simpan alasan penolakan agar Seller tahu
    motor.approval_status = 'rejected'
    motor.rejection_reason = data.get('rejection_reason', 'Tidak memenuhi standar kualitas dealer.')
    motor.is_active = False
    
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Pengajuan kendaraan berhasil ditolak.'}), 200

# ==========================================
# ARSIPKAN / HAPUS KENDARAAN (SOFT DELETE)
# ==========================================
@inventory_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def archive_motor(id):
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    
    # Validasi akses (Hanya admin/manajemen yang boleh)
    if user.role not in ['super_admin', 'admin_cabang', 'cs']:
        return jsonify({'message': 'Akses ditolak. Anda tidak memiliki izin.'}), 403

    motor = Motorcycle.query.get_or_404(id)
    
    # Soft Delete: Ubah status menjadi tidak aktif dan stok jadi 0
    motor.is_active = False
    motor.stock = 0
    Wishlist.query.filter_by(motorcycle_id=id).delete()
    
    db.session.commit()
    
    return jsonify({
        'status': 'success', 
        'message': f'Kendaraan {motor.brand_rel.name if motor.brand_rel else ""} {motor.model_name} berhasil diarsipkan.'
    }), 200