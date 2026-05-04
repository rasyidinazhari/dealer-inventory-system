from datetime import datetime, timedelta

from werkzeug.security import generate_password_hash

from backend.app.__init__ import create_app
from app.models import (
    Article,
    Banner,
    Branch,
    Brand,
    Category,
    Customer,
    Motorcycle,
    MotorcycleGallery,
    Sale,
    User,
    VehicleModel,
    Wishlist,
    db,
)

app = create_app()


def run_seed():
    with app.app_context():
        print("Starting database reset and seed...")
        db.drop_all()
        db.create_all()

        # 1. Master data
        branches = [
            Branch(
                name="Abu Motor Pusat (Solo)",
                address="Jl. Slamet Riyadi No. 1",
                phone="0271-111111",
            ),
            Branch(
                name="Abu Motor Sukoharjo",
                address="Jl. Jend. Sudirman No. 10",
                phone="0271-222222",
            ),
        ]
        db.session.add_all(branches)

        brands = [
            Brand(name="Honda"),
            Brand(name="Yamaha"),
            Brand(name="Kawasaki"),
            Brand(name="Vespa"),
        ]
        db.session.add_all(brands)

        categories = [
            Category(name="Matic"),
            Category(name="Sport"),
            Category(name="Bebek"),
        ]
        db.session.add_all(categories)
        db.session.flush()

        vehicle_models = [
            VehicleModel(name="Beat CBS 2023", brand_id=brands[0].id),
            VehicleModel(name="Vario 160", brand_id=brands[0].id),
            VehicleModel(name="NMAX 155 Connected", brand_id=brands[1].id),
            VehicleModel(name="Aerox 155", brand_id=brands[1].id),
            VehicleModel(name="Ninja 250 FI", brand_id=brands[2].id),
            VehicleModel(name="Sprint 150 I-Get", brand_id=brands[3].id),
        ]
        db.session.add_all(vehicle_models)

        # 2. Users
        pusat = branches[0]
        sukoharjo = branches[1]

        users = {
            "owner": User(
                username="owner",
                password_hash=generate_password_hash("password123"),
                role="super_admin",
                full_name="Mas Abu",
                phone_number="08111",
                branch_id=None,
            ),
            "admin_skh": User(
                username="admin_skh",
                password_hash=generate_password_hash("password123"),
                role="admin_cabang",
                full_name="Budi Admin",
                phone_number="08222",
                branch_id=sukoharjo.id,
            ),
            "cs_nina": User(
                username="cs_nina",
                password_hash=generate_password_hash("password123"),
                role="cs",
                full_name="Nina CS",
                phone_number="08333",
                branch_id=pusat.id,
            ),
            "finance_doni": User(
                username="finance_doni",
                password_hash=generate_password_hash("password123"),
                role="finance",
                full_name="Doni Finance",
                phone_number="08444",
                branch_id=pusat.id,
            ),
            "seller_joko": User(
                username="seller_joko",
                password_hash=generate_password_hash("password123"),
                role="seller",
                full_name="Joko Susilo",
                phone_number="08555",
                branch_id=pusat.id,
            ),
        }
        db.session.add_all(users.values())
        db.session.flush()

        # 3. Customers
        customers = {
            "ahmad": Customer(
                nik="337200001",
                full_name="Ahmad Pembeli",
                phone_number="0899",
                address="Solo",
                branch_id=pusat.id,
            ),
            "sari": Customer(
                nik="337200002",
                full_name="Sari Kredit",
                phone_number="0888",
                address="Sukoharjo",
                branch_id=sukoharjo.id,
            ),
        }
        db.session.add_all(customers.values())
        db.session.flush()

        # 4. Inventory
        motorcycles = {
            "beat": Motorcycle(
                sku_code="INT-BEAT-01",
                branch_id=pusat.id,
                vehicle_type="Motor",
                condition="Bekas",
                brand_id=brands[0].id,
                category_id=categories[0].id,
                model_name="Beat CBS 2023",
                color="Hitam",
                transmission="Otomatis",
                year=2023,
                mileage="8.500 km",
                engine_capacity="110cc",
                documents="STNK, BPKB",
                incoming_date=datetime.utcnow().date() - timedelta(days=15),
                capital_price=15000000,
                repair_cost=500000,
                price=18000000,
                stock=2,
                description="Unit harian, irit, siap pakai.",
                approval_status="approved",
                is_active=True,
                image_url="/static/uploads/main_seed_beat.jpg",
            ),
            "nmax": Motorcycle(
                sku_code="INT-NMAX-02",
                branch_id=pusat.id,
                vehicle_type="Motor",
                condition="Bekas",
                brand_id=brands[1].id,
                category_id=categories[0].id,
                model_name="NMAX 155 Connected",
                color="Biru",
                transmission="Otomatis",
                year=2022,
                mileage="12.000 km",
                engine_capacity="155cc",
                documents="STNK, BPKB",
                incoming_date=datetime.utcnow().date() - timedelta(days=75),
                capital_price=28000000,
                repair_cost=1000000,
                price=32000000,
                stock=1,
                description="Kondisi terawat, pajak hidup.",
                approval_status="approved",
                is_active=True,
                image_url="/static/uploads/main_seed_nmax.jpg",
            ),
            "ninja_external": Motorcycle(
                sku_code="EXT-JOKO-01",
                branch_id=pusat.id,
                vehicle_type="Motor",
                condition="Bekas",
                brand_id=brands[2].id,
                category_id=categories[1].id,
                model_name="Ninja 250 FI",
                color="Hijau",
                transmission="Manual",
                year=2021,
                mileage="9.200 km",
                engine_capacity="250cc",
                documents="STNK, BPKB",
                incoming_date=datetime.utcnow().date() - timedelta(days=10),
                capital_price=0,
                repair_cost=0,
                base_price=50000000,
                dealer_fee=5000000,
                price=55000000,
                stock=1,
                description="Motor titipan seller, siap jual.",
                seller_id=users["seller_joko"].id,
                approval_status="approved",
                is_active=True,
                image_url="/static/uploads/main_seed_ninja.jpg",
            ),
            "aerox_pending": Motorcycle(
                sku_code="SELL-PENDING-01",
                branch_id=pusat.id,
                vehicle_type="Motor",
                condition="Bekas",
                brand_id=brands[1].id,
                category_id=categories[0].id,
                model_name="Aerox 155",
                color="Merah",
                transmission="Otomatis",
                year=2020,
                mileage="15.000 km",
                engine_capacity="155cc",
                documents="STNK",
                incoming_date=datetime.utcnow().date() - timedelta(days=3),
                capital_price=0,
                repair_cost=0,
                base_price=24000000,
                price=0,
                stock=1,
                description="Pengajuan seller yang masih menunggu approval.",
                seller_id=users["seller_joko"].id,
                approval_status="pending",
                is_active=False,
                image_url="/static/uploads/main_seed_aerox.jpg",
            ),
        }
        db.session.add_all(motorcycles.values())
        db.session.flush()

        galleries = [
            MotorcycleGallery(
                motorcycle_id=motorcycles["beat"].id,
                image_url="/static/uploads/gal_seed_beat_1.jpg",
            ),
            MotorcycleGallery(
                motorcycle_id=motorcycles["beat"].id,
                image_url="/static/uploads/gal_seed_beat_2.jpg",
            ),
            MotorcycleGallery(
                motorcycle_id=motorcycles["ninja_external"].id,
                image_url="/static/uploads/gal_seed_ninja_1.jpg",
            ),
            MotorcycleGallery(
                motorcycle_id=motorcycles["aerox_pending"].id,
                image_url="/static/uploads/gal_seed_aerox_1.jpg",
            ),
        ]
        db.session.add_all(galleries)

        # 5. Sales
        sales = [
            Sale(
                invoice_number="INV-SEED-001",
                branch_id=pusat.id,
                motorcycle_id=motorcycles["beat"].id,
                customer_id=customers["ahmad"].id,
                user_id=users["cs_nina"].id,
                payment_type="Cash",
                status="Selesai",
                is_deal_price=False,
                total_price=18000000,
                sale_date=datetime.utcnow() - timedelta(days=7),
            ),
            Sale(
                invoice_number="INV-SEED-002",
                branch_id=pusat.id,
                motorcycle_id=motorcycles["ninja_external"].id,
                customer_id=customers["ahmad"].id,
                user_id=users["cs_nina"].id,
                payment_type="Kredit",
                status="Disetujui",
                is_deal_price=True,
                deal_price=54500000,
                total_price=54500000,
                dp_amount=10000000,
                tenor=24,
                installment_amount=2100000,
                ktp_url="/static/uploads/documents/ktp_seed.jpg",
                kk_url="/static/uploads/documents/kk_seed.jpg",
                sale_date=datetime.utcnow() - timedelta(days=2),
            ),
        ]
        db.session.add_all(sales)

        # Reflect sold units in stock
        motorcycles["beat"].stock = 1
        motorcycles["ninja_external"].stock = 0

        # 6. Wishlist
        wishlist_entries = [
            Wishlist(
                user_id=users["seller_joko"].id,
                motorcycle_id=motorcycles["nmax"].id,
            ),
            Wishlist(
                user_id=users["seller_joko"].id,
                motorcycle_id=motorcycles["beat"].id,
            ),
        ]
        db.session.add_all(wishlist_entries)

        # 7. Articles
        articles = [
            Article(
                title="Tips Memilih Motor Bekas untuk Harian",
                slug="tips-memilih-motor-bekas-untuk-harian",
                content="Periksa surat, rangka, mesin, dan riwayat servis sebelum membeli motor bekas.",
                image_url="/static/uploads/blog_seed_tips.jpg",
                author_id=users["owner"].id,
                is_published=True,
            ),
            Article(
                title="Cara Menjual Motor Titipan Lebih Cepat",
                slug="cara-menjual-motor-titipan-lebih-cepat",
                content="Foto yang rapi, harga realistis, dan data unit lengkap mempercepat penjualan.",
                image_url="/static/uploads/blog_seed_seller.jpg",
                author_id=users["cs_nina"].id,
                is_published=False,
            ),
        ]
        db.session.add_all(articles)

        # 8. Banners
        banners = [
            Banner(
                title="Promo Motor Harian",
                image_url="/static/uploads/banners/banner_seed_1.jpg",
                link_url="/inventory",
                order=1,
                is_active=True,
            ),
            Banner(
                title="Titip Jual Abu Motor",
                image_url="/static/uploads/banners/banner_seed_2.jpg",
                link_url="/seller/dashboard",
                order=2,
                is_active=True,
            ),
        ]
        db.session.add_all(banners)

        db.session.commit()
        print("Seed completed.")
        print("Login seed user: owner / password123")


if __name__ == "__main__":
    run_seed()
