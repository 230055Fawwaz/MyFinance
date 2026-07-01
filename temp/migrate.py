# ==========================================
# Nama File: migrate.py
# Deskripsi: Migrasi SQLite
# Penulis:   Fawwaz Yaqzhan
# Tanggal:   30-06-2026
# Catatan:
#   - Dijalankan jika app/models.py mengalami perubahan
#   - File ini hanya digunakan sementara
#   - Jalankan di folder root dengan command "python -m temp.migrate"
# ==========================================

import os
import logging
from flask import Flask
from dotenv import load_dotenv
from sqlalchemy import event, text  # Tambahkan text untuk eksekusi SQL mentah
from sqlalchemy.engine import Engine
from app.models import db

# Memuat file .env
load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")

# Mengambil kunci dari .env
app.config["SECRET_KEY"] = os.environ.get(
    "FLASK_SECRET_KEY", "dev-key-fallback-jangan-pakai-di-production"
)

# Konfigurasi logging global
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
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


@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


def run_migration():
    print("Menghubungkan ke database lewat Flask-SQLAlchemy...")
    
    # Bungkus dalam blok app_context agar db.session bisa mendeteksi aplikasi Flask
    with app.app_context():
        try:
            print("Memulai migrasi kolom kategori_dana...")
            
            # Menggunakan db.session.execute() dengan fungsi text() dari SQLAlchemy
            query = text("ALTER TABLE accounts ADD COLUMN kategori_dana TEXT NOT NULL DEFAULT 'operasional';")
            db.session.execute(query)
            db.session.commit()
            
            print("✅ Migrasi sukses! Kolom 'kategori_dana' berhasil ditambahkan.")
            
        except Exception as e:
            db.session.rollback()
            # Menangani jika kolom ternyata sudah ada
            if "duplicate column name" in str(e).lower():
                print("⚠️ Kolom 'kategori_dana' sebenarnya sudah ada.")
            else:
                print(f"❌ Terjadi kesalahan: {e}")


if __name__ == "__main__":
    run_migration()
