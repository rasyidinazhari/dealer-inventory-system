from fileinput import filename
import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv # <-- Import ini
from .models import db

# Load variabel dari file .env
load_dotenv()


def create_app():
    app = Flask(__name__)
    CORS(app)

    # File akan disimpan di backend/app/static/uploads
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True) # Buat folder otomatis jika belum ada
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    # Ganti dengan username, password, dan port PostgreSQL kamu
    # Contoh di bawah menggunakan default postgres:
    DB_USER = os.getenv('DB_USERNAME')
    DB_PASS = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

    # Konfigurasi koneksi PostgreSQL
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Konfigurasi JWT Secret Key
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    db.init_app(app)

    # --- INISIALISASI JWT WAJIB DI SINI ---
    jwt = JWTManager(app) 
    # -------------------------------------

    with app.app_context():
        # Karena kita pindah ke database baru, ini akan otomatis
        # membuat semua tabel dari awal di PostgreSQL
        db.create_all() 

    # Registrasi Blueprints
    from .routes.inventory import inventory_bp
    from .routes.sales import sales_bp 
    from .routes.finance import finance_bp
    from .routes.auth import auth_bp
    from .routes.master import master_bp
    from .routes.users import users_bp, seller_bp
    from .routes.articles import articles_bp
    from .routes.banners import banners_bp
    from app.routes.wishlist import wishlist_bp

    app.register_blueprint(banners_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(sales_bp)   
    app.register_blueprint(finance_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(master_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(seller_bp)
    app.register_blueprint(articles_bp)
    app.register_blueprint(wishlist_bp)

    
    return app