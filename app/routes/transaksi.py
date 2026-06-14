# ==========================================
# Nama File: transaksi.py
# Deskripsi: Rute khusus fitur-fitur halaman transaksi dengan proteksi data
# Penulis:   Fawwaz Yaqzhan
# Tanggal:   14-06-2026
# ==========================================

import logging
from datetime import datetime
from decimal import Decimal, InvalidOperation
from sqlalchemy.exc import SQLAlchemyError
from flask import request, redirect, url_for, Blueprint, flash
from app.models import db, Account, Transaction, SubCategory, Transfer

transaksi_bp = Blueprint("transaksi", __name__)
logger = logging.getLogger(__name__)


@transaksi_bp.route("/tambah", methods=["POST"])
def tambah_transaksi():
    account_id = request.form.get("account_id")
    subcategory_id = request.form.get("subcategory_id")
    amount_str = request.form.get("amount")
    note = request.form.get("note")
    tanggal_str = request.form.get("date")

    # Validasi Input Kosong
    if not account_id or not subcategory_id or not amount_str or not tanggal_str:
        flash("Semua field transaksi wajib diisi!", "danger")
        return redirect(url_for("main.transaksi"))

    # Validasi Keberadaan Akun & Subkategori
    akun = Account.query.get(account_id)
    subkategori = SubCategory.query.get(subcategory_id)

    if not akun:
        flash("Akun tidak ditemukan!", "danger")
        return redirect(url_for("main.transaksi"))
    if not subkategori:
        flash("Subkategori tidak ditemukan!", "danger")
        return redirect(url_for("main.transaksi"))

    # Validasi Nominal
    try:
        amount = Decimal(amount_str)
        if amount <= 0:
            raise ValueError("Nominal transaksi harus lebih besar dari nol.")
    except (InvalidOperation, ValueError):
        flash("Nominal transaksi harus berupa angka positif yang valid!", "danger")
        return redirect(url_for("main.transaksi"))

    # Validasi Tanggal
    try:
        date_obj = datetime.strptime(tanggal_str, "%Y-%m-%d")
    except ValueError:
        flash("Format tanggal tidak valid!", "danger")
        return redirect(url_for("main.transaksi"))

    # Proses Eksekusi Database
    try:
        # Terapkan perubahan saldo pada akun terkait
        tipe_kategori = subkategori.category.type
        if tipe_kategori == "expense":
            akun.balance -= amount
        elif tipe_kategori == "income":
            akun.balance += amount
        else:
            raise ValueError("Tipe kategori tidak dikenal.")

        # Buat transaksi baru
        trx_baru = Transaction(
            account_id=account_id,
            subcategory_id=subcategory_id,
            amount=amount,
            date=date_obj,
            note=note,
        )
        db.session.add(trx_baru)
        db.session.commit()
        flash(
            f"Transaksi sebesar Rp {amount:,.0f} berhasil dicatat ke akun '{akun.nama}'!",
            "success",
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error("Database error saat tambah transaksi: %s", e)
        flash("Terjadi kesalahan database saat menyimpan transaksi.", "danger")
    except Exception as e:
        db.session.rollback()
        logger.error("Terjadi error tak terduga saat tambah transaksi: %s", e)
        flash("Gagal menambahkan transaksi akibat kesalahan sistem.", "danger")

    return redirect(url_for("main.transaksi"))


@transaksi_bp.route("/hapus/<int:transaksi_id>", methods=["POST"])
def hapus_transaksi(transaksi_id):
    trx = Transaction.query.get_or_404(transaksi_id)

    try:
        akun = trx.account
        kategori_tipe = trx.subcategory.category.type

        # Reversal Saldo
        if kategori_tipe == "expense":
            akun.balance += trx.amount
        elif kategori_tipe == "income":
            akun.balance -= trx.amount

        # Hapus transaksi
        db.session.delete(trx)
        db.session.commit()
        flash(
            "Transaksi berhasil dihapus dan saldo akun disesuaikan kembali!", "success"
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error("Database error saat hapus transaksi: %s", e)
        flash("Gagal menghapus transaksi karena kesalahan database.", "danger")
    except Exception as e:
        db.session.rollback()
        logger.error("Error tak terduga saat hapus transaksi: %s", e)
        flash("Gagal menghapus transaksi akibat kesalahan sistem.", "danger")

    return redirect(url_for("main.transaksi"))


@transaksi_bp.route("/edit/<int:transaksi_id>", methods=["POST"])
def edit_transaksi(transaksi_id):
    trx = Transaction.query.get_or_404(transaksi_id)

    # Ambil masukan dari form
    new_account_id = request.form.get("account_id")
    new_subcategory_id = request.form.get("subcategory_id")
    new_amount_str = request.form.get("amount")
    note = request.form.get("note")
    tanggal_str = request.form.get("date")

    # Validasi Input Kosong
    if (
        not new_account_id
        or not new_subcategory_id
        or not new_amount_str
        or not tanggal_str
    ):
        flash("Semua field transaksi wajib diisi!", "danger")
        return redirect(url_for("main.transaksi"))

    # Validasi Keberadaan Akun & Subkategori Baru
    new_akun = Account.query.get(new_account_id)
    new_subkategori = SubCategory.query.get(new_subcategory_id)

    if not new_akun:
        flash("Akun yang dipilih tidak ditemukan!", "danger")
        return redirect(url_for("main.transaksi"))
    if not new_subkategori:
        flash("Subkategori yang dipilih tidak ditemukan!", "danger")
        return redirect(url_for("main.transaksi"))

    # Validasi Nominal Baru
    try:
        new_amount = Decimal(new_amount_str)
        if new_amount <= 0:
            raise ValueError("Nominal transaksi harus lebih besar dari nol.")
    except (InvalidOperation, ValueError):
        flash("Nominal transaksi harus berupa angka positif yang valid!", "danger")
        return redirect(url_for("main.transaksi"))

    # Validasi Tanggal Baru
    try:
        new_date_obj = datetime.strptime(tanggal_str, "%Y-%m-%d")
    except ValueError:
        flash("Format tanggal tidak valid!", "danger")
        return redirect(url_for("main.transaksi"))

    try:
        # ---------------------------------------------------------
        # FASE 1: REVERSAL SALDO LAMA
        # ---------------------------------------------------------
        old_tipe = trx.subcategory.category.type
        old_akun = trx.account

        if old_tipe == "expense":
            old_akun.balance += trx.amount
        elif old_tipe == "income":
            old_akun.balance -= trx.amount

        # ---------------------------------------------------------
        # FASE 2: UPDATE DATA TRANSAKSI
        # ---------------------------------------------------------
        trx.account_id = new_account_id
        trx.subcategory_id = new_subcategory_id
        trx.amount = new_amount
        trx.note = note
        trx.date = new_date_obj

        # ---------------------------------------------------------
        # FASE 3: TERAPKAN SALDO BARU
        # ---------------------------------------------------------
        new_tipe = new_subkategori.category.type
        if new_tipe == "expense":
            new_akun.balance -= new_amount
        elif new_tipe == "income":
            new_akun.balance += new_amount

        db.session.commit()
        flash("Perubahan transaksi berhasil disimpan!", "success")
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error("Database error saat edit transaksi ID %s: %s", transaksi_id, e)
        flash(
            "Gagal menyimpan perubahan transaksi akibat kesalahan database.", "danger"
        )
    except Exception as e:
        db.session.rollback()
        logger.error("Error tak terduga saat edit transaksi ID %s: %s", transaksi_id, e)
        flash("Gagal memperbarui transaksi akibat kesalahan sistem.", "danger")

    return redirect(url_for("main.transaksi"))


@transaksi_bp.route("/transfer", methods=["POST"])
def proses_transfer():
    from_account_id = request.form.get("from_account_id")
    to_account_id = request.form.get("to_account_id")
    amount_str = request.form.get("amount", "0")
    fee_str = request.form.get("fee", "0")
    note = request.form.get("note", "")

    # Validasi Dasar
    if not from_account_id or not to_account_id:
        flash("Akun asal dan akun tujuan wajib dipilih!", "danger")
        return redirect(url_for("main.akun"))

    if from_account_id == to_account_id:
        flash("Akun asal dan tujuan transfer tidak boleh sama!", "danger")
        return redirect(url_for("main.akun"))

    try:
        amount = Decimal(amount_str)
        fee = Decimal(fee_str) if fee_str else Decimal("0.00")
        if amount <= 0:
            raise ValueError("Jumlah transfer harus lebih besar dari nol.")
        if fee < 0:
            raise ValueError("Biaya transfer tidak boleh negatif.")
    except (InvalidOperation, ValueError):
        flash(
            "Jumlah dan biaya transfer harus berupa angka positif yang valid!", "danger"
        )
        return redirect(url_for("main.akun"))

    from_account = Account.query.get(from_account_id)
    to_account = Account.query.get(to_account_id)

    if not from_account or not to_account:
        flash("Akun asal atau akun tujuan transfer tidak ditemukan!", "danger")
        return redirect(url_for("main.akun"))

    total_deduction = amount + fee
    if from_account.balance < total_deduction:
        flash(
            f"Saldo akun '{from_account.nama}' tidak mencukupi untuk transfer! (Dibutuhkan: Rp {total_deduction:,.0f}, Saldo aktif: Rp {from_account.balance:,.0f})",
            "danger",
        )
        return redirect(url_for("main.akun"))

    # Proses Eksekusi Database
    try:
        from_account.balance -= total_deduction
        to_account.balance += amount

        new_transfer = Transfer(
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            amount=amount,
            fee=fee,
            note=note,
        )
        db.session.add(new_transfer)
        db.session.commit()
        flash(
            f"Transfer sebesar Rp {amount:,.0f} dari '{from_account.nama}' ke '{to_account.nama}' berhasil!",
            "success",
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error("Database error saat transfer: %s", e)
        flash("Terjadi kesalahan database saat memproses transfer.", "danger")
    except Exception as e:
        db.session.rollback()
        logger.error("Unexpected error saat transfer: %s", e)
        flash("Gagal melakukan transfer karena kesalahan sistem.", "danger")

    return redirect(url_for("main.akun"))
