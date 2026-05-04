import os
import time
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Article, User

articles_bp = Blueprint('articles', __name__, url_prefix='/api/articles')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'webp'}

# 1. GET ALL (Untuk Admin)
@articles_bp.route('/admin', methods=['GET'])
@jwt_required()
def get_admin_articles():
    articles = Article.query.order_by(Article.created_at.desc()).all()
    result = []
    for a in articles:
        result.append({
            'id': a.id,
            'title': a.title,
            'slug': a.slug,
            'content': a.content, # <-- TAMBAHKAN INI AGAR BISA DI-EDIT
            'author_name': a.author.full_name if a.author else 'Admin',
            'is_published': a.is_published,
            'created_at': a.created_at.strftime("%d %b %Y"),
            'image_url': a.image_url
        })
    return jsonify({'status': 'success', 'data': result}), 200

# 2. GET PUBLIC (Untuk Homepage - Hanya yang published)
@articles_bp.route('/public', methods=['GET'], strict_slashes=False)
def get_public_articles():
    # Ambil 3 artikel terbaru untuk homepage
    limit = request.args.get('limit', 3, type=int)
    articles = Article.query.filter_by(is_published=True).order_by(Article.created_at.desc()).limit(limit).all()
    
    result = []
    for a in articles:
        result.append({
            'id': a.id,
            'title': a.title,
            'slug': a.slug,
            'content': a.content[:150] + '...', # Potong konten untuk preview
            'author_name': a.author.full_name if a.author else 'Admin',
            'created_at': a.created_at.strftime("%d %b %Y"),
            'image_url': a.image_url
        })
    return jsonify({'status': 'success', 'data': result}), 200

# 3. CREATE (Admin Tambah Artikel)
@articles_bp.route('/', methods=['POST'])
@jwt_required()
def create_article():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    
    if user.role not in ['super_admin', 'cs']:
        return jsonify({'message': 'Akses ditolak.'}), 403

    data = request.form
    title = data.get('title')
    
    # Generate slug dan pastikan unik
    base_slug = Article.generate_slug(title)
    slug = base_slug
    counter = 1
    while Article.query.filter_by(slug=slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1

    image_file = request.files.get('image')
    image_url = None

    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        unique_filename = f"blog_{int(time.time())}_{filename}"
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, unique_filename)
        image_file.save(filepath)
        image_url = f"/static/uploads/{unique_filename}"

    new_article = Article(
        title=title,
        slug=slug,
        content=data.get('content'),
        author_id=user.id,
        is_published=str(data.get('is_published', 'true')).lower() == 'true',
        image_url=image_url
    )
    
    db.session.add(new_article)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Artikel berhasil diterbitkan!'}), 201

# 4. DELETE (Admin Hapus Artikel)
@articles_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_article(id):
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    if user.role not in ['super_admin']:
        return jsonify({'message': 'Akses ditolak. Hanya Super Admin yang bisa menghapus.'}), 403

    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Artikel berhasil dihapus.'}), 200

# 2.5. GET SINGLE PUBLIC ARTICLE (Untuk halaman Baca Artikel)
@articles_bp.route('/public/<slug>', methods=['GET'])
def get_single_article(slug):
    # Cari artikel berdasarkan slug dan pastikan statusnya published
    article = Article.query.filter_by(slug=slug, is_published=True).first()
    
    if not article:
        return jsonify({'status': 'error', 'message': 'Artikel tidak ditemukan'}), 404
        
    return jsonify({
        'status': 'success', 
        'data': {
            'id': article.id,
            'title': article.title,
            'slug': article.slug,
            'content': article.content, # Kirim konten utuh
            'author_name': article.author.full_name if article.author else 'Admin',
            'created_at': article.created_at.strftime("%d %b %Y"),
            'image_url': article.image_url
        }
    }), 200

# 5. UPDATE (Admin Edit Artikel)
@articles_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_article(id):
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    
    if user.role not in ['super_admin', 'cs']:
        return jsonify({'message': 'Akses ditolak.'}), 403

    article = Article.query.get_or_404(id)
    data = request.form

    # Update Judul & Slug
    title = data.get('title')
    if title and title != article.title:
        article.title = title
        base_slug = Article.generate_slug(title)
        slug = base_slug
        counter = 1
        while Article.query.filter(Article.slug == slug, Article.id != article.id).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        article.slug = slug

    # Update Konten & Status
    if 'content' in data:
        article.content = data.get('content')
    if 'is_published' in data:
        article.is_published = str(data.get('is_published')).lower() == 'true'

    # Update Gambar (Hanya jika upload gambar baru)
    image_file = request.files.get('image')
    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        unique_filename = f"blog_{int(time.time())}_{filename}"
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, unique_filename)
        image_file.save(filepath)
        article.image_url = f"/static/uploads/{unique_filename}"

    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Artikel berhasil diperbarui!'}), 200