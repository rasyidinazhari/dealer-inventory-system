import os
import time
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Sale, Motorcycle, Customer, User 
from flask import current_app

sales_bp = Blueprint('sales', __name__, url_prefix='/api/sales')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'webp', 'pdf'}

# ==========================================
# 1. READ ALL SALES (DENGAN FILTER CABANG)
# ==========================================
@sales_bp.route('/', methods=['GET'])
@jwt_required()
def get_sales():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    
    query = Sale.query
    filter_branch_id = request.args.get('branch_id')

    # Filter berdasarkan Cabang
    if user.role == 'admin_cabang' or user.role in ['cs', 'finance', 'seller']:
        query = query.filter_by(branch_id=user.branch_id)
    elif user.role == 'super_admin' and filter_branch_id:
        query = query.filter_by(branch_id=filter_branch_id)

    sales = query.order_by(Sale.sale_date.desc()).all()
    result = []
    for s in sales:
        brand_name = s.motorcycle_sold.brand_rel.name if (s.motorcycle_sold and s.motorcycle_sold.brand_rel) else 'Unknown'
        motor_name = f"{brand_name} {s.motorcycle_sold.model_name}" if s.motorcycle_sold else 'Unknown'
        
        result.append({
            'id': s.id,
            'invoice_number': s.invoice_number,
            'branch_name': s.branch.name if s.branch else 'Unknown',
            'customer_name': s.customer.full_name if s.customer else 'Unknown',
            'motor_name': motor_name,
            'payment_type': s.payment_type,
            'status': s.status,
            'is_deal_price': s.is_deal_price,
            'total_price': float(s.total_price),
            'dp_amount': float(s.dp_amount) if s.dp_amount else 0,
            'tenor': s.tenor,
            'ktp_url': s.ktp_image_url,
            'kk_url': s.kk_image_url,
            'sale_date': s.sale_date.isoformat() if s.sale_date else None
        })
    return jsonify({'status': 'success', 'data': result}), 200

# ==========================================
# 2. GET FORM DATA (LIST MOTOR & CUSTOMER)
# ==========================================
@sales_bp.route('/form-data', methods=['GET'])
@jwt_required()
def get_form_data():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    
    # Filter agar kasir hanya melihat customer dan motor di cabangnya
    branch_id = user.branch_id
    if user.role == 'super_admin' and request.args.get('branch_id'):
        branch_id = request.args.get('branch_id')

    cust_query = Customer.query
    motor_query = Motorcycle.query.filter(Motorcycle.is_active == True, Motorcycle.stock > 0)

    if branch_id:
        cust_query = cust_query.filter_by(branch_id=branch_id)
        motor_query = motor_query.filter_by(branch_id=branch_id)

    customers = cust_query.order_by(Customer.full_name).all()
    motors = motor_query.all()
    
    cust_list = [{'id': c.id, 'name': c.full_name, 'nik': c.nik} for c in customers]
    motor_list = []
    for m in motors:
        brand_name = m.brand_rel.name if m.brand_rel else ''
        motor_list.append({
            'id': m.id, 
            'name': f"{brand_name} {m.model_name} ({m.color})", 
            'price': float(m.price), 
            'stock': m.stock
        })
    
    return jsonify({
        'status': 'success', 
        'data': {
            'customers': cust_list,
            'motors': motor_list
        }
    }), 200

# ==========================================
# 3. CREATE SALE (POS / TRANSAKSI BARU)
# ==========================================
@sales_bp.route('/', methods=['POST'])
@jwt_required()
def create_sale():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    
    # Karena frontend mengirim via FormData, kita gunakan request.form
    data = request.form
    motor_id = data.get('motorcycle_id')
    payment_type = data.get('payment_type', 'Cash')
    
    motor = Motorcycle.query.get(motor_id)
    if not motor or motor.stock < 1:
        return jsonify({'message': 'Motor tidak tersedia atau stok habis'}), 400

    # 1. Tentukan Harga Final (Cek apakah pakai harga Deal/Nego)
    is_deal_price = str(data.get('is_deal_price', 'false')).lower() == 'true'
    final_price = float(data.get('deal_price')) if is_deal_price else motor.price

    # 2. Setup Folder Upload
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'documents')
    os.makedirs(upload_folder, exist_ok=True)
    
    ktp_url = None
    kk_url = None

    # 3. Proses Upload File KTP & KK JIKA KREDIT
    if payment_type == 'Kredit':
        ktp_file = request.files.get('ktp_image')
        kk_file = request.files.get('kk_image')

        if ktp_file and allowed_file(ktp_file.filename):
            filename = secure_filename(ktp_file.filename)
            unique_filename = f"ktp_{int(time.time())}_{filename}"
            filepath = os.path.join(upload_folder, unique_filename)
            ktp_file.save(filepath)
            ktp_url = f"/static/uploads/documents/{unique_filename}"
            
        if kk_file and allowed_file(kk_file.filename):
            filename = secure_filename(kk_file.filename)
            unique_filename = f"kk_{int(time.time())}_{filename}"
            filepath = os.path.join(upload_folder, unique_filename)
            kk_file.save(filepath)
            kk_url = f"/static/uploads/documents/{unique_filename}"

    # 4. Buat Record Transaksi Baru
    new_sale = Sale(
        invoice_number=f"INV-{int(time.time())}",
        branch_id=motor.branch_id, # <--- GANTI JADI INI (Ambil dari cabang motornya)
        user_id=user.id, # Kasir yang melayani
        customer_id=data.get('customer_id'),
        motorcycle_id=motor.id,
        payment_type=payment_type,
        
        # Simpan flag harga deal
        is_deal_price=is_deal_price,
        total_price=final_price,
        
        # Simpan rincian kredit (Jika ada)
        dp_amount=float(data.get('dp_amount', 0)),
        tenor=int(data.get('tenor', 0)) if data.get('tenor') else None,
        installment_amount=float(data.get('installment_amount', 0)),
        
        # Simpan URL dokumen
        ktp_url=ktp_url,
        kk_url=kk_url,
        
        # Jika Cash langsung selesai, jika Kredit masuk ke Pengajuan
        status='Selesai' if payment_type == 'Cash' else 'Pengajuan'
    )
    
    # 5. Kurangi Stok
    motor.stock -= 1
    
    db.session.add(new_sale)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Transaksi berhasil dibuat'}), 201

# ==========================================
# 4. UPDATE STATUS (Setujui Kredit / Batal)
# ==========================================
@sales_bp.route('/<int:id>/status', methods=['PUT'])
@jwt_required()
def update_sale_status(id):
    sale = Sale.query.get_or_404(id)
    data = request.json
    new_status = data.get('status')
    if not new_status:
        return jsonify({'status': 'error', 'message': 'Status tidak valid'}), 400
        
    sale.status = new_status
    db.session.commit()
    return jsonify({'status': 'success', 'message': f'Status menjadi {new_status}'}), 200