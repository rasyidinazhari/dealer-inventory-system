from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Sale, User, Motorcycle
from datetime import datetime
import calendar

finance_bp = Blueprint('finance', __name__, url_prefix='/api/finance')

@finance_bp.route('/', methods=['GET']) # Sesuaikan rute agar sinkron dengan Vue
@jwt_required()
def get_financial_report():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.role not in ['super_admin', 'finance', 'admin_cabang']:
        return jsonify({'message': 'Akses ditolak.'}), 403

    month = request.args.get('month')
    year = request.args.get('year', datetime.now().year)
    filter_branch_id = request.args.get('branch_id')

    query = db.session.query(Sale).filter(Sale.status.in_(['Selesai', 'Disetujui']))

    # Filter Cabang
    if user.role in ['finance', 'admin_cabang']: # <--- UBAH BARIS INI
        query = query.filter(Sale.branch_id == user.branch_id)
    elif user.role == 'super_admin' and filter_branch_id:
        query = query.filter(Sale.branch_id == filter_branch_id)

    # Filter Bulan & Tahun (Sesuai Dashboard Vue)
    if month and month != "":
        last_day = calendar.monthrange(int(year), int(month))[1]
        start_date = datetime(int(year), int(month), 1).date()
        end_date = datetime(int(year), int(month), last_day).date()
        query = query.filter(Sale.sale_date >= start_date, Sale.sale_date <= end_date)
    else:
        # Jika bulan kosong, ambil sepanjang tahun tersebut
        query = query.filter(db.extract('year', Sale.sale_date) == int(year))

    sales_data = query.order_by(Sale.sale_date.desc()).all()

    # Inisialisasi summary
    summary = {
        'gross_revenue': 0,
        'total_costs': 0,
        'net_profit': 0,
        'total_sales_count': len(sales_data)
    }
    
    report_details = []

    for sale in sales_data:
        motor = sale.motorcycle_sold
        price = float(sale.total_price)
        
        # Ambil nilai modal & perbaikan dari database
        capital = float(motor.capital_price or 0)
        repair = float(motor.repair_cost or 0)
        
        # PERBAIKAN LOGIKA: Pastikan benar-benar motor titipan dengan mengecek base_price
        base_price = float(motor.base_price or 0)
        
        if motor.seller_id is not None and base_price > 0:
            hpp = base_price  # HPP Titip Jual adalah uang yang disetor ke Seller
            profit = price - hpp
        else:
            hpp = capital + repair  # HPP Internal adalah Modal + Servis
            profit = price - hpp

        summary['gross_revenue'] += price
        summary['total_costs'] += hpp
        summary['net_profit'] += profit

        report_details.append({
            'id': sale.id,
            'invoice_number': sale.invoice_number,
            'sale_date': sale.sale_date.strftime("%Y-%m-%d"),
            'motor_name': motor.model_name,
            'branch_name': sale.branch.name if sale.branch else 'Pusat',
            'status': sale.status,
            'capital_price': capital,
            'repair_cost': repair,
            'total_price': price,
            'net_profit': profit,
            'payment_type': sale.payment_type,
            'is_deal_price': getattr(sale, 'is_deal_price', False)
        })

    return jsonify({
        'status': 'success',
        'summary': summary,
        'data': report_details
    }), 200