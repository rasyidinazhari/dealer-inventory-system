import re
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ==========================================
# MASTER DATA & ARSITEKTUR MULTI-CABANG
# ==========================================
class Branch(db.Model):
    __tablename__ = 'branches'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) 
    address = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    users = db.relationship('User', backref='branch', lazy=True)
    customers = db.relationship('Customer', backref='branch', lazy=True)
    motorcycles = db.relationship('Motorcycle', backref='branch', lazy=True)
    sales = db.relationship('Sale', backref='branch', lazy=True)

class Brand(db.Model):
    __tablename__ = 'brands'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    # Relasi ke model kendaraan
    models = db.relationship('VehicleModel', backref='brand', lazy=True, cascade="all, delete-orphan")

# INI YANG BARU DITAMBAHKAN
class VehicleModel(db.Model):
    __tablename__ = 'vehicle_models'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=False)

# PASTIKAN CLASS INI TIDAK TERHAPUS
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


# ==========================================
# PENGGUNA & PELANGGAN
# ==========================================
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=True) 
    phone_number = db.Column(db.String(20), nullable=True)
    
    # Role nambah: 'admin_cabang'
    role = db.Column(db.String(50), nullable=False) 
    
    # Superadmin/Owner mungkin tidak terikat cabang (nullable=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=True) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    motorcycles = db.relationship('Motorcycle', backref='seller_user', lazy=True)
    wishlists = db.relationship('Wishlist', back_populates='user', cascade="all, delete-orphan")

    # wishlists = db.relationship('Wishlist', back_populates='user', cascade="all, delete-orphan")

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    nik = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False) # Terikat cabang
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sales = db.relationship('Sale', backref='customer', lazy=True)

# Catatan: Tabel Affiliate (Mitra) dihapus sesuai revisi


# ==========================================
# INVENTORY KENDARAAN
# ==========================================
class Motorcycle(db.Model):
    __tablename__ = 'motorcycles'
    id = db.Column(db.Integer, primary_key=True)
    sku_code = db.Column(db.String(50), unique=True, nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    
    vehicle_type = db.Column(db.String(20), default='Motor') 
    condition = db.Column(db.String(20), default='Bekas')    
    
    # Ubah menjadi Relasi ke tabel Merek dan Kategori
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    # Menyimpan nama model (contoh: "Vario 160", "Civic Turbo")
    model_name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(50))
    
    transmission = db.Column(db.String(50), default='Otomatis')
    year = db.Column(db.Integer)
    mileage = db.Column(db.String(50), default='0 (Baru)')
    body_type = db.Column(db.String(50))
    engine_capacity = db.Column(db.String(50))
    features = db.Column(db.Text)
    documents = db.Column(db.String(255))
    
    # KOMPONEN KEUANGAN & MONITORING
    incoming_date = db.Column(db.Date, nullable=False, default=datetime.utcnow) # Untuk alert 2 bulan
    capital_price = db.Column(db.Numeric(15, 2), default=0) # Modal beli
    repair_cost = db.Column(db.Numeric(15, 2), default=0)   # Biaya Perbaikan (Net Profit = Harga Jual - (Modal + Perbaikan))
    price = db.Column(db.Numeric(15, 2), nullable=False)    # Harga Jual Normal
    
    # SISTEM SELLER EKSTERNAL
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # Jika null, berarti milik Abu Motor
    approval_status = db.Column(db.String(20), default='approved')
    rejection_reason = db.Column(db.Text, nullable=True)
    base_price = db.Column(db.Numeric(15, 2), nullable=True) # Harga titipan seller
    dealer_fee = db.Column(db.Numeric(15, 2), default=0)

    stock = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    
    # FOTO KENDARAAN (1 Utama, 9 Tambahan di tabel terpisah)
    image_url = db.Column(db.String(255)) # Foto Utama
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sales = db.relationship('Sale', backref='motorcycle_sold', lazy=True)
    galleries = db.relationship('MotorcycleGallery', backref='motorcycle', cascade="all, delete-orphan")
    wishlisted_by = db.relationship('Wishlist', back_populates='motorcycle', cascade="all, delete-orphan")


    # Relasi ke tabel master untuk mempermudah akses (motorcycle.brand_rel.name)
    brand_rel = db.relationship('Brand', backref='motorcycles')
    category_rel = db.relationship('Category', backref='motorcycles')
    

class MotorcycleGallery(db.Model):
    """Menyimpan hingga 9 foto tambahan per kendaraan"""
    __tablename__ = 'motorcycle_galleries'
    id = db.Column(db.Integer, primary_key=True)
    motorcycle_id = db.Column(db.Integer, db.ForeignKey('motorcycles.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ==========================================
# PENJUALAN (POS) & KREDIT
# ==========================================
class Sale(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    motorcycle_id = db.Column(db.Integer, db.ForeignKey('motorcycles.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Kasir/Sales
    
    payment_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='Selesai') 
    
    # HARGA DEAL NEGOSIASI
    is_deal_price = db.Column(db.Boolean, default=False) 
    deal_price = db.Column(db.Numeric(15, 2), nullable=True) 
    
    # DATA KREDIT
    dp_amount = db.Column(db.Numeric(15, 2), default=0)
    tenor = db.Column(db.Integer, default=0)
    installment_amount = db.Column(db.Numeric(15, 2), default=0)
    ktp_image_url = db.Column(db.String(255), nullable=True) # Upload KTP untuk kredit
    kk_image_url = db.Column(db.String(255), nullable=True)  # Upload KK untuk kredit
    ktp_url = db.Column(db.String(255), nullable=True)
    kk_url = db.Column(db.String(255), nullable=True)
    
    total_price = db.Column(db.Numeric(15, 2), nullable=False) # Harga akhir yang dipakai
    sale_date = db.Column(db.DateTime, default=datetime.utcnow)


# ==========================================
# WISHLIST SELLER (KENDARAAN DISUKAI)
# ==========================================
class Wishlist(db.Model):
    __tablename__ = 'wishlists'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    motorcycle_id = db.Column(db.Integer, db.ForeignKey('motorcycles.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relasi agar mudah memanggil data motor dan user
    user = db.relationship('User', back_populates='wishlists')
    motorcycle = db.relationship('Motorcycle', back_populates='wishlisted_by')


# ==========================================
# BLOG & BANNER
# ==========================================
class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.relationship('User', backref='articles', lazy=True)

    @staticmethod
    def generate_slug(title):
        slug = title.lower()
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        slug = slug.strip('-')
        return slug
    
class Banner(db.Model):
    __tablename__ = 'banners'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    image_url = db.Column(db.String(255), nullable=False)
    link_url = db.Column(db.String(255), nullable=True)
    order = db.Column(db.Integer, default=0) 
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)