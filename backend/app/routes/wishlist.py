from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Wishlist, Motorcycle

wishlist_bp = Blueprint('wishlist', __name__, url_prefix='/api/wishlist')

# 1. AMBIL SEMUA WISHLIST MILIK USER
@wishlist_bp.route('/', methods=['GET'])
@jwt_required()
def get_user_wishlist():
    current_user_id = get_jwt_identity()
    
    # Ambil semua data wishlist beserta relasi motornya
    wishlists = Wishlist.query.filter_by(user_id=current_user_id).order_by(Wishlist.created_at.desc()).all()
    
    result = []
    for item in wishlists:
        motor = item.motorcycle
        if motor: # Pastikan motor belum dihapus
            result.append({
                'wishlist_id': item.id,
                'motorcycle_id': motor.id,
                'brand': motor.brand_rel.name if motor.brand_rel else 'Unknown',
                'model_name': motor.model_name,
                'price': float(motor.price or 0),
                'image_url': motor.image_url,
                'condition': motor.condition,
                'vehicle_type': motor.vehicle_type,
                'stock': motor.stock,
                'added_at': item.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
            
    return jsonify({'status': 'success', 'data': result}), 200

# 2. TOGGLE WISHLIST (Tambah jika belum ada, Hapus jika sudah ada)
@wishlist_bp.route('/toggle', methods=['POST'])
@jwt_required()
def toggle_wishlist():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    motor_id = data.get('motorcycle_id')

    if not motor_id:
        return jsonify({'message': 'ID Motor diperlukan'}), 400

    # Cek apakah motor ada di database
    motor = Motorcycle.query.get(motor_id)
    if not motor:
        return jsonify({'message': 'Kendaraan tidak ditemukan'}), 404

    # Cek apakah sudah ada di wishlist
    existing_item = Wishlist.query.filter_by(user_id=current_user_id, motorcycle_id=motor_id).first()

    if existing_item:
        # Jika sudah ada, HAPUS (Un-wishlist)
        db.session.delete(existing_item)
        db.session.commit()
        return jsonify({'status': 'success', 'is_wishlisted': False, 'message': 'Dihapus dari Wishlist'}), 200
    else:
        # Jika belum ada, TAMBAH (Wishlist)
        new_item = Wishlist(user_id=current_user_id, motorcycle_id=motor_id)
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'status': 'success', 'is_wishlisted': True, 'message': 'Ditambahkan ke Wishlist'}), 201

# 3. CEK STATUS WISHLIST (Untuk update UI tombol love di Detail Motor)
@wishlist_bp.route('/check/<int:motor_id>', methods=['GET'])
@jwt_required()
def check_wishlist_status(motor_id):
    current_user_id = get_jwt_identity()
    existing_item = Wishlist.query.filter_by(user_id=current_user_id, motorcycle_id=motor_id).first()
    
    is_wishlisted = existing_item is not None
    return jsonify({'status': 'success', 'is_wishlisted': is_wishlisted}), 200