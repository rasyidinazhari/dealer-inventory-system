from app import create_app
from backend.app.modelsbackup import db

app = create_app()
with app.app_context():
    db.drop_all()   # Menghapus semua tabel lama
    db.create_all() # Membuat ulang semua tabel dengan kolom image_url
    print("Database berhasil di-reset!")

exit()