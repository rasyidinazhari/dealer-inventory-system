import random
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from app import create_app 
from app.models import (
    db, Branch, Brand, VehicleModel, Category, User, Customer, 
    Motorcycle, MotorcycleGallery, Sale, Wishlist, Article, Banner
)

app = create_app()

def run_seed():
    with app.app_context():
        print("🚀 Memulai proses reset & seeding database Abu Motor...")
        db.drop_all()
        db.create_all()

        # 1. SEED MASTER DATA
        branches = [Branch(name="Abu Motor Pusat (Solo)", address="Jl. Slamet Riyadi No. 1"), Branch(name="Abu Motor Sukoharjo", address="Jl. Jend. Sudirman No. 10")]
        db.session.add_all(branches)
        db.session.commit()

        # Merek
        brands = [Brand(name="Honda"), Brand(name="Yamaha"), Brand(name="Kawasaki"), Brand(name="Vespa")]
        db.session.add_all(brands)
        db.session.commit()

        # Model Kendaraan Berdasarkan Merek
        vehicle_models = [
            VehicleModel(name="Beat CBS 2023", brand_id=brands[0].id),
            VehicleModel(name="Vario 160", brand_id=brands[0].id),
            VehicleModel(name="NMAX 155 Connected", brand_id=brands[1].id),
            VehicleModel(name="Aerox 155", brand_id=brands[1].id),
            VehicleModel(name="Ninja 250 FI", brand_id=brands[2].id),
            VehicleModel(name="Sprint 150 I-Get", brand_id=brands[3].id),
        ]
        db.session.add_all(vehicle_models)

        # Kategori
        categories = [Category(name="Matic"), Category(name="Sport"), Category(name="Bebek")]
        db.session.add_all(categories)
        db.session.commit()

        # 2. SEED USERS
        pusat_id = branches[0].id
        skh_id = branches[1].id
        users_data = [
            {'username': 'owner', 'role': 'super_admin', 'full_name': 'Mas Abu', 'phone': '08111', 'branch_id': None},
            {'username': 'admin_skh', 'role': 'admin_cabang', 'full_name': 'Budi Admin', 'phone': '08222', 'branch_id': skh_id},
            {'username': 'cs_nina', 'role': 'cs', 'full_name': 'Nina CS', 'phone': '08333', 'branch_id': pusat_id},
            {'username': 'finance_doni', 'role': 'finance', 'full_name': 'Doni Finance', 'phone': '08444', 'branch_id': pusat_id},
            {'username': 'seller_joko', 'role': 'seller', 'full_name': 'Joko Susilo', 'phone': '08555', 'branch_id': pusat_id},
        ]
        created_users = {}
        for u in users_data:
            user = User(username=u['username'], password_hash=generate_password_hash('password123'), role=u['role'], full_name=u['full_name'], phone_number=u['phone'], branch_id=u['branch_id'])
            db.session.add(user)
            db.session.commit()
            created_users[u['username']] = user

        # 3. SEED CUSTOMER
        customer = Customer(nik='337200001', full_name='Ahmad Pembeli', phone_number='0899', address='Solo', branch_id=pusat_id)
        db.session.add(customer)
        db.session.commit()

        # 4. SEED KENDARAAN
        seller_id = created_users['seller_joko'].id
        motors_data = [
            {'sku': 'INT-BEAT-01', 'brand_id': brands[0].id, 'cat_id': categories[0].id, 'model': 'Beat CBS 2023', 'color': 'Hitam', 'price': 18000000, 'capital': 15000000, 'stock': 3, 'seller_id': None, 'status': 'approved'},
            {'sku': 'INT-NMAX-02', 'brand_id': brands[1].id, 'cat_id': categories[0].id, 'model': 'NMAX 155 Connected', 'color': 'Biru', 'price': 32000000, 'capital': 28000000, 'stock': 2, 'seller_id': None, 'status': 'approved'},
            {'sku': f'EXT-{seller_id}-1', 'brand_id': brands[2].id, 'cat_id': categories[1].id, 'model': 'Ninja 250 FI', 'color': 'Hijau', 'price': 55000000, 'capital': 0, 'stock': 1, 'seller_id': seller_id, 'status': 'approved'},
        ]

        for m in motors_data:
            motor = Motorcycle(
                sku_code=m['sku'], branch_id=pusat_id, vehicle_type='Motor', condition='Bekas',
                brand_id=m['brand_id'], category_id=m['cat_id'], model_name=m['model'], color=m['color'],
                capital_price=m['capital'], price=m['price'], stock=m['stock'], seller_id=m['seller_id'],
                approval_status=m['status'], is_active=True
            )
            db.session.add(motor)
        db.session.commit()

        print("🎉 SEEDING SELESAI! Struktur Merek & Model sudah berhasil dimasukkan!")

if __name__ == '__main__':
    run_seed()