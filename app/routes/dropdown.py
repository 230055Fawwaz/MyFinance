# ==========================================
# Nama File: dropdown.py
# Deskripsi: Rute khusus fitur-fitur halaman dropdown dengan proteksi data
# Penulis:   Fawwaz Yaqzhan
# Tanggal:   14-06-2026
# ==========================================

import logging
from sqlalchemy.exc import SQLAlchemyError
from flask import request, redirect, url_for, Blueprint, flash
from app.models import db, Category, SubCategory, Transaction

kategori_bp = Blueprint("kategori", __name__)
logger = logging.getLogger(__name__)


@kategori_bp.route("/kategori/tambah", methods=["POST"])
def tambah_kategori():
    nama_kategori = request.form.get("nama")
    tipe_kategori = request.form.get("type")  # 'income' atau 'expense'

    # Validasi Input Kosong
    if not nama_kategori or not nama_kategori.strip():
        flash("Nama kategori tidak boleh kosong!", "danger")
        return redirect(url_for("main.dropdown"))
    
    if tipe_kategori not in ["income", "expense"]:
        flash("Tipe kategori tidak valid!", "danger")
        return redirect(url_for("main.dropdown"))

    try:
        kategori_baru = Category(nama=nama_kategori.strip(), type=tipe_kategori)
        db.session.add(kategori_baru)
        db.session.commit()
        flash(f"Kategori '{kategori_baru.nama}' berhasil ditambahkan!", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error("Gagal menambahkan kategori ke database: %s", e)
        flash("Terjadi kesalahan database saat menambahkan kategori.", "danger")

    return redirect(url_for("main.dropdown"))


@kategori_bp.route("/subkategori/tambah", methods=["POST"])
def tambah_subkategori():
    nama_subkategori = request.form.get("nama")
    kategori_induk_id = request.form.get("category_id")

    # Validasi Input Kosong
    if not nama_subkategori or not nama_subkategori.strip():
        flash("Nama subkategori tidak boleh kosong!", "danger")
        return redirect(url_for("main.dropdown"))

    if not kategori_induk_id:
        flash("Kategori induk harus dipilih!", "danger")
        return redirect(url_for("main.dropdown"))

    kategori_induk = Category.query.get(kategori_induk_id)
    if not kategori_induk:
        flash("Kategori induk tidak ditemukan!", "danger")
        return redirect(url_for("main.dropdown"))

    try:
        sub_baru = SubCategory(
            nama=nama_subkategori.strip(), 
            category_id=kategori_induk_id
        )
        db.session.add(sub_baru)
        db.session.commit()
        flash(f"Subkategori '{sub_baru.nama}' berhasil ditambahkan ke kategori '{kategori_induk.nama}'!", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error("Gagal menambahkan subkategori ke database: %s", e)
        flash("Terjadi kesalahan database saat menambahkan subkategori.", "danger")

    return redirect(url_for("main.dropdown"))


@kategori_bp.route("/kategori/hapus/<int:kategori_id>", methods=["POST"])
def hapus_kategori(kategori_id):
    kategori = Category.query.get_or_404(kategori_id)

    # Validasi: Apakah ada subkategori dari kategori ini yang terhubung ke transaksi aktif?
    subkategori_ids = [sub.id for sub in kategori.subcategories]
    has_transactions = False
    if subkategori_ids:
        has_transactions = Transaction.query.filter(Transaction.subcategory_id.in_(subkategori_ids)).first() is not None

    if has_transactions:
        flash(f"Kategori '{kategori.nama}' tidak dapat dihapus karena salah satu subkategorinya masih digunakan dalam transaksi aktif!", "danger")
        return redirect(url_for("main.dropdown"))

    try:
        # Hapus semua subkategori terlebih dahulu secara eksplisit
        for sub in kategori.subcategories:
            db.session.delete(sub)
        
        db.session.delete(kategori)
        db.session.commit()
        flash(f"Kategori '{kategori.nama}' beserta seluruh subkategorinya berhasil dihapus!", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error("Gagal menghapus kategori ID %s: %s", kategori_id, e)
        flash("Gagal menghapus kategori akibat kesalahan database.", "danger")

    return redirect(url_for("main.dropdown"))


@kategori_bp.route("/kategori/edit/<int:kategori_id>", methods=["POST"])
def edit_kategori(kategori_id):
    kategori = Category.query.get_or_404(kategori_id)

    nama_kategori = request.form.get("nama")
    tipe_kategori = request.form.get("type")

    # Validasi Input Kosong
    if not nama_kategori or not nama_kategori.strip():
        flash("Nama kategori tidak boleh kosong!", "danger")
        return redirect(url_for("main.dropdown"))
    
    if tipe_kategori not in ["income", "expense"]:
        flash("Tipe kategori tidak valid!", "danger")
        return redirect(url_for("main.dropdown"))

    try:
        kategori.nama = nama_kategori.strip()
        kategori.type = tipe_kategori
        db.session.commit()
        flash(f"Perubahan kategori '{kategori.nama}' berhasil disimpan!", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error("Gagal mengubah kategori ID %s: %s", kategori_id, e)
        flash("Gagal menyimpan perubahan kategori akibat kesalahan database.", "danger")

    return redirect(url_for("main.dropdown"))


@kategori_bp.route("/subkategori/hapus/<int:subkategori_id>", methods=["POST"])
def hapus_subkategori(subkategori_id):
    subkategori = SubCategory.query.get_or_404(subkategori_id)

    # Validasi: Apakah subkategori ini digunakan dalam transaksi aktif?
    has_transactions = Transaction.query.filter_by(subcategory_id=subkategori_id).first() is not None
    if has_transactions:
        flash(f"Subkategori '{subkategori.nama}' tidak dapat dihapus karena masih digunakan dalam transaksi aktif!", "danger")
        return redirect(url_for("main.dropdown"))

    try:
        db.session.delete(subkategori)
        db.session.commit()
        flash(f"Subkategori '{subkategori.nama}' berhasil dihapus!", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error("Gagal menghapus subkategori ID %s: %s", subkategori_id, e)
        flash("Gagal menghapus subkategori akibat kesalahan database.", "danger")

    return redirect(url_for("main.dropdown"))


@kategori_bp.route("/subkategori/edit/<int:subkategori_id>", methods=["POST"])
def edit_subkategori(subkategori_id):
    subkategori = SubCategory.query.get_or_404(subkategori_id)

    nama_subkategori = request.form.get("nama")
    kategori_induk_id = request.form.get("category_id")

    # Validasi Input Kosong
    if not nama_subkategori or not nama_subkategori.strip():
        flash("Nama subkategori tidak boleh kosong!", "danger")
        return redirect(url_for("main.dropdown"))

    if not kategori_induk_id:
        flash("Kategori induk harus dipilih!", "danger")
        return redirect(url_for("main.dropdown"))

    kategori_induk = Category.query.get(kategori_induk_id)
    if not kategori_induk:
        flash("Kategori induk tidak ditemukan!", "danger")
        return redirect(url_for("main.dropdown"))

    try:
        subkategori.nama = nama_subkategori.strip()
        subkategori.category_id = kategori_induk_id
        db.session.commit()
        flash(f"Perubahan subkategori '{subkategori.nama}' berhasil disimpan!", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error("Gagal mengubah subkategori ID %s: %s", subkategori_id, e)
        flash("Gagal menyimpan perubahan subkategori akibat kesalahan database.", "danger")

    return redirect(url_for("main.dropdown"))
