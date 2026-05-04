import os
import time
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app.models import db, Banner, User

banners_bp = Blueprint('banners', __name__, url_prefix='/api/banners')

def allowed_file(filename):
    # Tambahan format 'gif' barangkali admin mau upload banner animasi
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'webp', 'gif'}

# ==========================================
# 1. GET PUBLIC BANNERS (Untuk Home.vue)
# ==========================================
@banners_bp.route('/public', methods=['GET'])
def get_public_banners():
    # Hanya ambil yang aktif, urutkan berdasarkan order, lalu yang paling baru
    banners = Banner.query.filter_by(is_active=True).order_by(Banner.order.asc(), Banner.id.desc()).all()
    result = [{
        'id': b.id,
        'title': b.title,
        'image_url': b.image_url,
        'link_url': b.link_url
    } for b in banners]
    return jsonify({'status': 'success', 'data': result}), 200

# ==========================================
# 2. GET ALL BANNERS (Untuk Tabel Admin)
# ==========================================
@banners_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_banners():
    # Ambil semua banner (aktif maupun tidak)
    banners = Banner.query.order_by(Banner.order.asc(), Banner.id.desc()).all()
    result = [{
        'id': b.id,
        'title': b.title,
        'image_url': b.image_url,
        'order': b.order,
        'is_active': b.is_active,
        'link_url': b.link_url
    } for b in banners]
    return jsonify({'status': 'success', 'data': result}), 200

# ==========================================
# 3. UPLOAD NEW BANNER (POST)
# ==========================================
@banners_bp.route('/', methods=['POST'])
@jwt_required()
def add_banner():
    data = request.form
    file = request.files.get('image')
    
    if not file or not allowed_file(file.filename):
        return jsonify({'message': 'File gambar wajib diunggah dan format harus sesuai'}), 400

    filename = secure_filename(file.filename)
    unique_filename = f"banner_{int(time.time())}_{filename}"
    
    # KUNCI ABSOLUT: Pastikan selalu tersimpan di app/static/uploads/banners
    current_dir = os.path.abspath(os.path.dirname(__file__))
    upload_folder = os.path.abspath(os.path.join(current_dir, '..', 'static', 'uploads', 'banners'))
    os.makedirs(upload_folder, exist_ok=True)
    
    filepath = os.path.join(upload_folder, unique_filename)
    file.save(filepath)
    
    new_banner = Banner(
        title=data.get('title', ''),
        image_url=f"/static/uploads/banners/{unique_filename}",
        link_url=data.get('link_url', ''),
        order=int(data.get('order', 0)),
        is_active=True
    )
    db.session.add(new_banner)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Banner berhasil ditambahkan'}), 201

# ==========================================
# 4. UPDATE BANNER (PUT - Edit status/urutan)
# ==========================================
@banners_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_banner(id):
    banner = Banner.query.get_or_404(id)
    
    # Kita gunakan request.json karena biasanya edit status hanya kirim teks, bukan file
    data = request.json 
    if not data:
        data = request.form # Fallback jika frontend mengirim Form Data
        
    if 'title' in data: banner.title = data.get('title')
    if 'link_url' in data: banner.link_url = data.get('link_url')
    if 'order' in data: banner.order = int(data.get('order', banner.order))
    
    # Handle konversi string ke boolean jika dari Form Data
    if 'is_active' in data: 
        is_active_val = data.get('is_active')
        banner.is_active = str(is_active_val).lower() == 'true' if isinstance(is_active_val, str) else bool(is_active_val)
        
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Data banner berhasil diperbarui'}), 200

# ==========================================
# 5. DELETE BANNER (Hapus Permanen)
# ==========================================
@banners_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_banner(id):
    banner = Banner.query.get_or_404(id)
    
    # Hapus file fisik dari komputer/server
    if banner.image_url:
        current_dir = os.path.abspath(os.path.dirname(__file__))
        # Mengupas prefix "/static/" agar path gabungannya pas
        clean_url = banner.image_url.replace('/static/', '') 
        filepath = os.path.abspath(os.path.join(current_dir, '..', 'static', clean_url))
        
        if os.path.exists(filepath):
            try: os.remove(filepath)
            except Exception as e: print(f"Gagal menghapus gambar fisik: {e}")
            
    # Hapus dari database
    db.session.delete(banner)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Banner berhasil dihapus beserta filenya'}), 200