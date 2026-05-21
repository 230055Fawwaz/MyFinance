# ==========================================
# Nama File: akun.py
# Deskripsi: Rute khusus fitur-fitur halaman akun
# Penulis:   Fawwaz Yaqzhan
# Tanggal:   20-05-2026
# Catatan:
#   - Hanya rute yang ada di halaman akun
#   - Rute lain ada di file tersendiri
# ==========================================

from decimal import Decimal 
from flask import render_template, request, redirect, url_for, Blueprint
from app.models import db, Category, Account, Transaction, SubCategory, Transfer
from app import app
from datetime import datetime, timedelta
from sqlalchemy import func

akun_bp = Blueprint('akun', __name__)

@akun_bp.route('/tambah', methods=['POST'])
def tambah_akun():
    nama_akun = request.form.get('nama')
    tipe_akun = request.form.get('type')
    saldo_awal = request.form.get('balance')

    akun_baru = Account(nama=nama_akun, type=tipe_akun, balance=saldo_awal)
    db.session.add(akun_baru)
    db.session.commit()

    return redirect(url_for('akun')) # Kembali ke halaman akun setelah simpan

@akun_bp.route('/hapus/<int:id>', methods=['POST'])
def hapus_akun(id):
    akun = Account.query.get_or_404(id)
    
    # PERHATIAN: Jika akun dihapus, transaksi yang menggunakan foreign key akun ini 
    # bisa menyebabkan error (IntegrityError) kecuali dikonfigurasi 'cascade delete'.
    # Pastikan akun yang dihapus sedang tidak memiliki transaksi, 
    # atau ubah kode ini jika ingin menghapus transaksi terkait juga.
    
    db.session.delete(akun)
    db.session.commit()
    
    return redirect(url_for('akun'))

@akun_bp.route('/edit/<int:id>', methods=['POST'])
def edit_akun(id):
    akun = Account.query.get_or_404(id)
    
    # Update data berdasarkan input dari form modal
    akun.nama = request.form.get('nama')
    akun.type = request.form.get('type')
    akun.balance = Decimal(request.form.get('balance'))
    
    db.session.commit()
    
    return redirect(url_for('akun'))
