# ==========================================
# Nama File: main.py
# Deskripsi: Rute halaman web awal
# Penulis:   Fawwaz Yaqzhan
# Tanggal:   20-05-2026
# Catatan:
#   - Rute hanya menampilkan halaman saja beserta data di dalamnya
# ==========================================

import os
import subprocess
from datetime import datetime, timedelta, timezone
from flask import render_template, Blueprint, jsonify, current_app
from app.models import db, Category, SubCategory, Account, Transaction
from sqlalchemy import func
from decimal import Decimal
from app.utils.analisa import (
    deteksi_anomali_pengeluaran,
    hitung_kesehatan_keuangan,
    prediksi_pengeluaran_bulan_depan,
    analisis_hubungan_kategori,
)
from app.utils.dashgraph import (
    get_cash_flow_data,
    get_expense_allocation,
    get_account_distribution,
)

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@main_bp.route("/dashboard")
def dashboard():
    # Rentang waktu: 30 hari terakhir
    hari_ini = datetime.now(timezone.utc).replace(tzinfo=None)
    tiga_puluh_hari_lalu = hari_ini - timedelta(days=30)

    cf_labels, cf_income, cf_expense = get_cash_flow_data(tiga_puluh_hari_lalu)
    exp_labels, exp_values = get_expense_allocation(tiga_puluh_hari_lalu)
    acc_labels, acc_values = get_account_distribution()

    # --- PERBAIKAN DI SINI (Menggunakan Decimal) ---
    # 1. Hitung Uang Siap Pakai (Operasional)
    uang_panas = db.session.query(func.sum(Account.balance)).filter(
        Account.kategori_dana == 'operasional'
    ).scalar() or Decimal('0.00')

    # 2. Hitung Uang Dingin (Tabungan)
    uang_dingin = db.session.query(func.sum(Account.balance)).filter(
        Account.kategori_dana == 'tabungan'
    ).scalar() or Decimal('0.00')

    # Sekarang keduanya bertipe Decimal, sehingga aman untuk dijumlahkan
    total_saldo_riil = uang_panas + uang_dingin

    return render_template(
        "dashboard.html",
        cf_labels=cf_labels,
        cf_income=cf_income,
        cf_expense=cf_expense,
        exp_labels=exp_labels,
        exp_values=exp_values,
        acc_labels=acc_labels,
        acc_values=acc_values,
        uang_panas=uang_panas,
        uang_dingin=uang_dingin,
        total_saldo_riil=total_saldo_riil
    )


@main_bp.route("/transaksi")
def transaksi():
    # Ambil semua transaksi, urutkan dari yang terbaru
    daftar_transaksi = Transaction.query.order_by(Transaction.date.desc()).all()

    # Ambil data akun dan kategori untuk dropdown di Modal Form
    daftar_akun = Account.query.all()
    daftar_kategori = Category.query.all()

    return render_template(
        "transaksi.html",
        transactions=daftar_transaksi,
        accounts=daftar_akun,
        categories=daftar_kategori,
    )


@main_bp.route("/akun")
def akun():
    # Ambil semua data akun dari database
    daftar_akun = Account.query.all()
    # Kirim variabel 'accounts' ke akun.html
    return render_template("akun.html", accounts=daftar_akun)


@main_bp.route("/laporan")
def laporan():
    return render_template("laporan.html")


@main_bp.route("/dropdown")
def dropdown():
    kategori_induk = Category.query.all()
    return render_template("dropdown.html", categories=kategori_induk)


@main_bp.route("/run-backup", methods=["POST"])
def run_backup():
    # Karena .bat sudah di dalam /app, langsung gabungkan saja
    path_to_bat = os.path.join(current_app.root_path, "backup.bat")

    if os.path.exists(path_to_bat):
        try:
            # Jalankan skrip dengan 'cwd' di dalam folder /app tempat skrip itu berada
            subprocess.run(
                [path_to_bat],
                shell=True,
                check=True,
                cwd=current_app.root_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            return (
                jsonify(
                    {"status": "success", "message": "Database berhasil dibackup!"}
                ),
                200,
            )
        except subprocess.CalledProcessError as e:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": f"Skrip gagal dieksekusi: {e.stderr}",
                    }
                ),
                500,
            )
    else:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"Skrip tidak ditemukan di: {path_to_bat}",
                }
            ),
            404,
        )


@main_bp.route("/analisa")
def halaman_analisa():
    # 1. Buat Query SQL JOIN menggunakan SQLAlchemy Statement
    stmt = (
        db.session.query(
            Transaction.id,
            Transaction.date,
            Transaction.amount,
            Transaction.note,
            SubCategory.nama.label("sub_nama"),
            Category.type.label("cat_type"),
        )
        .select_from(Transaction)
        .join(SubCategory)
        .join(Category)
        .statement
    )

    # 2. Masukkan langsung ke Pandas DataFrame
    import pandas as pd

    df = pd.read_sql(stmt, con=db.engine)

    # 3. Konversi kolom date menjadi tipe datetime agar bisa diolah Pandas
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])

    # 4. Oper DataFrame ke fungsi analisa (Bukan lagi objek semua_transaksi)
    return render_template(
        "analisa.html",
        data_anomali=deteksi_anomali_pengeluaran(df),
        dss=hitung_kesehatan_keuangan(df),
        prediksi=prediksi_pengeluaran_bulan_depan(df),
        pola_hubungan=analisis_hubungan_kategori(df),
    )
