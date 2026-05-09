from flask import Flask
from app.models import db
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

# 1. Konfigurasi SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '..', 'myfinance.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# 2. Membuat tabel database jika belum ada
with app.app_context():
    db.create_all()

# 3. Cache busting untuk development (Ditaruh di sini)
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

# 4. CRITICAL: Impor routes WAJIB di paling bawah untuk mencegah circular import
from app import routes
