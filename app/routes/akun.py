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
from flask import request, redirect, url_for, Blueprint
from app.models import db, Account

akun_bp = Blueprint("akun", __name__)


@akun_bp.route("/tambah", methods=["POST"])
def tambah_akun():
    nama_akun = request.form.get("nama")
    tipe_akun = request.form.get("type")
    saldo_awal = request.form.get("balance")

    akun_baru = Account(nama=nama_akun, type=tipe_akun, balance=saldo_awal)
    db.session.add(akun_baru)
    db.session.commit()

    return redirect(url_for("main.akun"))  # Kembali ke halaman akun setelah simpan


@akun_bp.route("/hapus/<int:akun_id>", methods=["POST"])
def hapus_akun(akun_id):
    akun = Account.query.get_or_404(akun_id)

    # PERHATIAN: Jika akun dihapus, transaksi yang menggunakan foreign key akun ini
    # bisa menyebabkan error (IntegrityError) kecuali dikonfigurasi 'cascade delete'.
    # Pastikan akun yang dihapus sedang tidak memiliki transaksi,
    # atau ubah kode ini jika ingin menghapus transaksi terkait juga.

    db.session.delete(akun)
    db.session.commit()

    return redirect(url_for("main.akun"))


@akun_bp.route("/edit/<int:akun_id>", methods=["POST"])
def edit_akun(akun_id):
    akun = Account.query.get_or_404(akun_id)

    # Update data berdasarkan input dari form modal
    akun.nama = request.form.get("nama")
    akun.type = request.form.get("type")
    akun.balance = Decimal(request.form.get("balance"))

    db.session.commit()

    return redirect(url_for("main.akun"))
