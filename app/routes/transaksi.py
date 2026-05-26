# ==========================================
# Nama File: transaksi.py
# Deskripsi: Rute khusus fitur-fitur halaman transaksi
# Penulis:   Fawwaz Yaqzhan
# Tanggal:   20-05-2026
# Catatan:
#   - Hanya rute yang ada di halaman transaksi
#   - Rute lain ada di file tersendiri
# ==========================================

from decimal import Decimal
from flask import request, redirect, url_for, Blueprint
from app.models import db, Account, Transaction, SubCategory, Transfer
from datetime import datetime

transaksi_bp = Blueprint("transaksi", __name__)


@transaksi_bp.route("/tambah", methods=["POST"])
def tambah_transaksi():
    account_id = request.form.get("account_id")
    subcategory_id = request.form.get("subcategory_id")
    amount = Decimal(request.form.get("amount"))
    note = request.form.get("note")

    # HTML <input type="date"> mengirim format string 'YYYY-MM-DD'
    # Kita harus ubah ke objek datetime Python
    tanggal_str = request.form.get("date")
    date_obj = datetime.strptime(tanggal_str, "%Y-%m-%d")

    # Buat record transaksi baru
    trx_baru = Transaction(
        account_id=account_id,
        subcategory_id=subcategory_id,
        amount=amount,
        date=date_obj,
        note=note,
    )
    db.session.add(trx_baru)

    # Lakukan update saldo pada akun terkait
    akun = Account.query.get(account_id)
    subkategori = SubCategory.query.get(subcategory_id)

    # Cek tipe dari kategori induknya (income / expense)
    if subkategori.category.type == "expense":
        akun.balance -= amount
    elif subkategori.category.type == "income":
        akun.balance += amount

    db.session.commit()

    return redirect(url_for("main.transaksi"))


@transaksi_bp.route("/hapus/<int:id>", methods=["POST"])
def hapus_transaksi(id):
    # Cari transaksi berdasarkan ID, jika tidak ada kembalikan 404
    trx = Transaction.query.get_or_404(id)

    # Ambil data akun dan tipe kategori transaksi yang akan dihapus
    akun = trx.account
    kategori_tipe = trx.subcategory.category.type

    # LOGIKA REVERSAL SALDO
    # Jika transaksi aslinya pengeluaran, uangnya harus dikembalikan ke akun (+)
    # Jika transaksi aslinya pemasukan, uangnya harus ditarik dari akun (-)
    if kategori_tipe == "expense":
        akun.balance += trx.amount
    elif kategori_tipe == "income":
        akun.balance -= trx.amount

    # Hapus transaksi dari database
    db.session.delete(trx)
    db.session.commit()

    return redirect(url_for("main.transaksi"))


@transaksi_bp.route("/edit/<int:id>", methods=["POST"])
def edit_transaksi(id):
    trx = Transaction.query.get_or_404(id)

    # ---------------------------------------------------------
    # FASE 1: REVERSAL SALDO LAMA
    # Batalkan efek dari transaksi lama sebelum data diperbarui
    # ---------------------------------------------------------
    tipe_lama = trx.subcategory.category.type
    akun_lama = trx.account

    if tipe_lama == "expense":
        akun_lama.balance += trx.amount
    elif tipe_lama == "income":
        akun_lama.balance -= trx.amount

    # ---------------------------------------------------------
    # FASE 2: UPDATE DATA TRANSAKSI
    # Masukkan data baru dari form modal
    # ---------------------------------------------------------
    trx.account_id = request.form.get("account_id")
    trx.subcategory_id = request.form.get("subcategory_id")
    trx.amount = Decimal(request.form.get("amount"))
    trx.note = request.form.get("note")
    trx.date = datetime.strptime(request.form.get("date"), "%Y-%m-%d")

    # ---------------------------------------------------------
    # FASE 3: TERAPKAN SALDO BARU
    # Potong/tambah saldo akun berdasarkan data yang baru diedit
    # ---------------------------------------------------------
    akun_baru = Account.query.get(trx.account_id)
    subkategori_baru = SubCategory.query.get(trx.subcategory_id)
    tipe_baru = subkategori_baru.category.type

    if tipe_baru == "expense":
        akun_baru.balance -= trx.amount
    elif tipe_baru == "income":
        akun_baru.balance += trx.amount

    # Simpan semua perubahan (update transaksi & update saldo akun)
    db.session.commit()

    return redirect(url_for("main.transaksi"))


# Menggunakan rute absolut agar tetap bisa diakses di url '/transfer'
@transaksi_bp.route("/transfer", methods=["POST"])
def proses_transfer():
    from_account_id = request.form.get("from_account_id")
    to_account_id = request.form.get("to_account_id")

    amount = Decimal(request.form.get("amount", 0))
    fee = Decimal(request.form.get("fee", 0))
    note = request.form.get("note", "")

    # 1. Validasi Dasar: Jika akun sama atau jumlah <= 0, langsung kembali
    if from_account_id == to_account_id or amount <= 0:
        return redirect(url_for("main.akun"))

    from_account = Account.query.get(from_account_id)
    to_account = Account.query.get(to_account_id)

    if not from_account or not to_account:
        return redirect(url_for("main.akun"))

    # 2. Validasi Saldo: Jika saldo kurang, batalkan dan kembali ke akun
    total_deduction = amount + fee
    if from_account.balance < total_deduction:
        return redirect(url_for("main.akun"))

    # 3. Proses Eksekusi Database
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

    except Exception as e:
        db.session.rollback()
        # Print error ke terminal untuk kebutuhan debugging kamu
        print(f"Error proses transfer: {e}")

    # 4. Sukses: Kembali ke halaman akun
    return redirect(url_for("main.akun"))
