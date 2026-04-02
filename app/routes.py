# URL

from decimal import Decimal # Tambahkan ini
from flask import Flask, render_template, request, redirect, url_for
from app.models import db, Category, Account, Transaction, SubCategory
from datetime import datetime
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


# ==========================================
# ROUTE UNTUK MENAMPILKAN HALAMAN WEB
# ==========================================

@app.route('/')
@app.route('/transaksi')
def transaksi():
    # Ambil semua transaksi, urutkan dari yang terbaru
    daftar_transaksi = Transaction.query.order_by(Transaction.date.desc()).all()
    
    # Ambil data akun dan kategori untuk dropdown di Modal Form
    daftar_akun = Account.query.all()
    daftar_kategori = Category.query.all()
    
    return render_template('transaksi.html', 
                           transactions=daftar_transaksi,
                           accounts=daftar_akun,
                           categories=daftar_kategori)

@app.route('/akun')
def akun():
    # Ambil semua data akun dari database
    daftar_akun = Account.query.all()
    # Kirim variabel 'accounts' ke akun.html
    return render_template('akun.html', accounts=daftar_akun) 

@app.route('/settings')
def settings():
    kategori_induk = Category.query.all() 
    return render_template('settings.html', categories=kategori_induk)


# ==========================================
# ROUTE UNTUK MENERIMA DATA FORM (POST)
# ==========================================

# 1. Simpan Akun Baru
@app.route('/akun/tambah', methods=['POST'])
def tambah_akun():
    nama_akun = request.form.get('nama')
    tipe_akun = request.form.get('type')
    saldo_awal = request.form.get('balance')

    akun_baru = Account(nama=nama_akun, type=tipe_akun, balance=saldo_awal)
    db.session.add(akun_baru)
    db.session.commit()

    return redirect(url_for('akun')) # Kembali ke halaman akun setelah simpan


# 2. Simpan Kategori Baru
@app.route('/settings/kategori/tambah', methods=['POST'])
def tambah_kategori():
    nama_kategori = request.form.get('nama')
    tipe_kategori = request.form.get('type') # 'income' atau 'expense'

    kategori_baru = Category(nama=nama_kategori, type=tipe_kategori)
    db.session.add(kategori_baru)
    db.session.commit()

    return redirect(url_for('settings'))


# 3. Simpan Sub-Kategori Baru
@app.route('/settings/subkategori/tambah', methods=['POST'])
def tambah_subkategori():
    nama_subkategori = request.form.get('nama')
    kategori_induk_id = request.form.get('category_id')

    sub_baru = SubCategory(nama=nama_subkategori, category_id=kategori_induk_id)
    db.session.add(sub_baru)
    db.session.commit()

    return redirect(url_for('settings'))


# 4. Simpan Transaksi Baru & Update Saldo
@app.route('/transaksi/tambah', methods=['POST'])
def tambah_transaksi():
    account_id = request.form.get('account_id')
    subcategory_id = request.form.get('subcategory_id')
    amount = Decimal(request.form.get('amount'))
    note = request.form.get('note')
    
    # HTML <input type="date"> mengirim format string 'YYYY-MM-DD'
    # Kita harus ubah ke objek datetime Python
    tanggal_str = request.form.get('date') 
    date_obj = datetime.strptime(tanggal_str, '%Y-%m-%d')

    # Buat record transaksi baru
    trx_baru = Transaction(
        account_id=account_id,
        subcategory_id=subcategory_id,
        amount=amount,
        date=date_obj,
        note=note
    )
    db.session.add(trx_baru)

    # Lakukan update saldo pada akun terkait
    akun = Account.query.get(account_id)
    subkategori = SubCategory.query.get(subcategory_id)
    
    # Cek tipe dari kategori induknya (income / expense)
    if subkategori.category.type == 'expense':
        akun.balance -= amount
    elif subkategori.category.type == 'income':
        akun.balance += amount

    db.session.commit()

    return redirect(url_for('transaksi'))