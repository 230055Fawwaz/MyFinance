# ==========================================
# Nama File: akun.py
# Deskripsi: Rute khusus fitur-fitur halaman akun dengan proteksi data
# Penulis:   Fawwaz Yaqzhan
# Tanggal:   14-06-2026
# ==========================================

import logging
from decimal import Decimal, InvalidOperation
from sqlalchemy.exc import SQLAlchemyError
from flask import request, redirect, url_for, Blueprint, flash
from app.models import db, Account, Transaction, Transfer

akun_bp = Blueprint("akun", __name__)
logger = logging.getLogger(__name__)


@akun_bp.route("/tambah", methods=["POST"])
def tambah_akun():
    nama_akun = request.form.get("nama")
    tipe_akun = request.form.get("type")
    saldo_awal_str = request.form.get("balance")

    # Validasi Input Kosong
    if not nama_akun or not nama_akun.strip():
        flash("Nama akun tidak boleh kosong!", "danger")
        return redirect(url_for("main.akun"))
    if not tipe_akun or not tipe_akun.strip():
        flash("Tipe akun tidak boleh kosong!", "danger")
        return redirect(url_for("main.akun"))

    # Validasi Saldo
    try:
        saldo_awal = Decimal(saldo_awal_str) if saldo_awal_str else Decimal("0.00")
        if saldo_awal < 0:
            raise ValueError("Saldo awal tidak boleh negatif.")
    except (InvalidOperation, ValueError):
        flash("Saldo awal harus berupa angka positif yang valid!", "danger")
        return redirect(url_for("main.akun"))

    # Simpan ke Database
    try:
        akun_baru = Account(
            nama=nama_akun.strip(), type=tipe_akun.strip(), balance=saldo_awal
        )
        db.session.add(akun_baru)
        db.session.commit()
        flash(f"Akun '{akun_baru.nama}' berhasil ditambahkan!", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error("Gagal menambahkan akun ke database: %s", e)
        flash("Terjadi kesalahan pada database saat menyimpan akun baru.", "danger")

    return redirect(url_for("main.akun"))


@akun_bp.route("/hapus/<int:akun_id>", methods=["POST"])
def hapus_akun(akun_id):
    akun = Account.query.get_or_404(akun_id)

    # Validasi Hubungan Kunci Asing sebelum Hapus (menghindari orphan/IntegrityError)
    has_transactions = (
        Transaction.query.filter_by(account_id=akun_id).first() is not None
    )
    has_transfers = (
        Transfer.query.filter(
            (Transfer.from_account_id == akun_id) | (Transfer.to_account_id == akun_id)
        ).first()
        is not None
    )

    if has_transactions or has_transfers:
        flash(
            f"Akun '{akun.nama}' tidak dapat dihapus karena masih memiliki histori transaksi atau transfer aktif!",
            "danger",
        )
        return redirect(url_for("main.akun"))

    try:
        db.session.delete(akun)
        db.session.commit()
        flash(f"Akun '{akun.nama}' berhasil dihapus!", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error("Gagal menghapus akun ID %s: %s", akun_id, e)
        flash("Gagal menghapus akun akibat kesalahan sistem database.", "danger")

    return redirect(url_for("main.akun"))


@akun_bp.route("/edit/<int:akun_id>", methods=["POST"])
def edit_akun(akun_id):
    akun = Account.query.get_or_404(akun_id)

    nama_akun = request.form.get("nama")
    tipe_akun = request.form.get("type")
    saldo_str = request.form.get("balance")

    # Validasi Input Kosong
    if not nama_akun or not nama_akun.strip():
        flash("Nama akun tidak boleh kosong!", "danger")
        return redirect(url_for("main.akun"))
    if not tipe_akun or not tipe_akun.strip():
        flash("Tipe akun tidak boleh kosong!", "danger")
        return redirect(url_for("main.akun"))

    # Validasi Saldo
    try:
        saldo = Decimal(saldo_str) if saldo_str else Decimal("0.00")
        if saldo < 0:
            raise ValueError("Saldo tidak boleh negatif.")
    except (InvalidOperation, ValueError):
        flash("Saldo harus berupa angka positif yang valid!", "danger")
        return redirect(url_for("main.akun"))

    try:
        akun.nama = nama_akun.strip()
        akun.type = tipe_akun.strip()
        akun.balance = saldo
        db.session.commit()
        flash(f"Perubahan pada akun '{akun.nama}' berhasil disimpan!", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error("Gagal mengedit akun ID %s: %s", akun_id, e)
        flash("Gagal menyimpan perubahan akun akibat kesalahan database.", "danger")

    return redirect(url_for("main.akun"))
