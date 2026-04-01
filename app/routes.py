# URL

from flask import Flask, render_template
from app.models import db
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

# Konfigurasi SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '..', 'myfinance.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Membuat tabel database jika belum ada
with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/transaksi')
def transaksi():
    return render_template('transaksi.html') # 

@app.route('/akun')
def akun():
    return render_template('akun.html') # 

@app.route('/settings')
def settings():
    return render_template('settings.html') #