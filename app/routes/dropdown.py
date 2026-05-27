# ==========================================
# Nama File: dropdown.py
# Deskripsi: Rute khusus fitur-fitur halaman dropdown
# Penulis:   Fawwaz Yaqzhan
# Tanggal:   20-05-2026
# Catatan:
#   - Hanya rute yang ada di halaman dropdown
#   - Rute lain ada di file tersendiri
# ==========================================

from flask import request, redirect, url_for, Blueprint
from app.models import db, Category, SubCategory

kategori_bp = Blueprint("kategori", __name__)


@kategori_bp.route("/kategori/tambah", methods=["POST"])
def tambah_kategori():
    nama_kategori = request.form.get("nama")
    tipe_kategori = request.form.get("type")  # 'income' atau 'expense'

    kategori_baru = Category(nama=nama_kategori, type=tipe_kategori)
    db.session.add(kategori_baru)
    db.session.commit()

    return redirect(url_for("main.dropdown"))


@kategori_bp.route("/subkategori/tambah", methods=["POST"])
def tambah_subkategori():
    nama_subkategori = request.form.get("nama")
    kategori_induk_id = request.form.get("category_id")

    sub_baru = SubCategory(nama=nama_subkategori, category_id=kategori_induk_id)
    db.session.add(sub_baru)
    db.session.commit()

    return redirect(url_for("main.dropdown"))


@kategori_bp.route("/kategori/hapus/<int:kategori_id>", methods=["POST"])
def hapus_kategori(kategori_id):
    kategori = Category.query.get_or_404(kategori_id)

    # Catatan: Sama seperti akun, menghapus kategori yang masih memiliki sub-kategori
    # atau transaksi bisa menyebabkan error database (jika foreign key diaktifkan).
    db.session.delete(kategori)
    db.session.commit()

    return redirect(url_for("main.dropdown"))


@kategori_bp.route("/kategori/edit/<int:kategori_id>", methods=["POST"])
def edit_kategori(kategori_id):
    kategori = Category.query.get_or_404(kategori_id)

    kategori.nama = request.form.get("nama")
    kategori.type = request.form.get("type")

    db.session.commit()
    return redirect(url_for("main.dropdown"))


@kategori_bp.route("/subkategori/hapus/<int:subkategori_id>", methods=["POST"])
def hapus_subkategori(subkategori_id):
    subkategori = SubCategory.query.get_or_404(subkategori_id)

    db.session.delete(subkategori)
    db.session.commit()

    return redirect(url_for("main.dropdown"))


@kategori_bp.route("/subkategori/edit/<int:subkategori_id>", methods=["POST"])
def edit_subkategori(subkategori_id):
    subkategori = SubCategory.query.get_or_404(subkategori_id)

    subkategori.nama = request.form.get("nama")
    subkategori.category_id = request.form.get(
        "category_id"
    )  # Memungkinkan ganti induk kategori

    db.session.commit()
    return redirect(url_for("main.dropdown"))
