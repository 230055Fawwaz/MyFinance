# ==========================================
# Nama File: __init__.py
# Deskripsi: Inisialisasi Flask dan SQLite
# Penulis:   Fawwaz Yaqzhan
# Tanggal:   01-04-2026
# Catatan:
#   - Konrigurasi SQLite dan membuatnya jika belum ada
#   - Cacha busting agar browser selalu menampilkan versi terbaru
#   - Rute di-impor agar menghindari circular import
# ==========================================

from flask import Flask
from app.models import db
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '..', 'myfinance.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

# ====================================================
# PROSES REGISTRASI BLUEPRINT BARU DI SINI
# ====================================================
# Jalankan import di paling bawah untuk menghindari circular import
from app.routes.main import main_bp

# Daftarkan ke aplikasi utama Anda
app.register_blueprint(main_bp, url_prefix='/')
