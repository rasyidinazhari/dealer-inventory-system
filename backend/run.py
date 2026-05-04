import os
from flask import send_from_directory # <--- Pastikan baris ini ada
from app import create_app

app = create_app()

# Tambahkan route ini sebelum app.run()
@app.route('/app/static/uploads/<path:filename>')
def serve_uploaded_file(filename):
    # Pastikan path ini benar menuju folder uploads kamu
    upload_path = os.path.join(app.root_path, 'static', 'uploads')
    return send_from_directory(upload_path, filename)

if __name__ == '__main__':
    app.run(port=5001, debug=True)