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

import os
import logging
from flask import Flask
from dotenv import load_dotenv
from sqlalchemy import event
from sqlalchemy.engine import Engine
from app.models import db

# Memuat file .env
load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")

# Mengambil kunci dari .env. Jika tidak ditemukan, gunakan fallback default (hanya untuk development)
app.config["SECRET_KEY"] = os.environ.get(
    "FLASK_SECRET_KEY", "dev-key-fallback-jangan-pakai-di-production"
)

# Konfigurasi logging global
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],  # Agar log muncul di terminal/console
)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "..", "myfinance.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.close()


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

# noqa: E402 # pylint: disable=wrong-import-position
from app.routes.main import main_bp

# noqa: E402 # pylint: disable=wrong-import-position
from app.routes.transaksi import transaksi_bp

# noqa: E402 # pylint: disable=wrong-import-position
from app.routes.akun import akun_bp

# noqa: E402 # pylint: disable=wrong-import-position
from app.routes.dropdown import kategori_bp

# noqa: E402 # pylint: disable=wrong-import-position
from app.routes.laporan import laporan_bp

# Daftarkan ke aplikasi utama Anda
app.register_blueprint(main_bp, url_prefix="/")
app.register_blueprint(transaksi_bp, url_prefix="/transaksi")
app.register_blueprint(akun_bp, url_prefix="/akun")
app.register_blueprint(kategori_bp, url_prefix="/dropdown")
app.register_blueprint(laporan_bp, url_prefix="/laporan")
