# ==========================================
# Nama File: main.py
# Deskripsi: Rute halaman web awal
# Penulis:   Fawwaz Yaqzhan
# Tanggal:   20-05-2026
# Catatan:
#   - Rute hanya menampilkan halaman saja beserta data di dalamnya
# ==========================================

from datetime import datetime, timedelta
from sqlalchemy import func
from flask import render_template, Blueprint
from app.models import db, Category, Account, Transaction, SubCategory

main_bp = Blueprint("main", __name__)


# ==========================================
# ROUTE UNTUK MENAMPILKAN HALAMAN WEB
# ==========================================


def _get_cash_flow_data(start_date):
    """Mengambil dan memproses data grafik arus kas (Pemasukan vs Pengeluaran)."""
    cash_flow_query = (
        db.session.query(
            func.date(Transaction.date).label("tanggal"),
            Category.type.label("tipe"),
            func.sum(Transaction.amount).label("total"),
        )
        .join(SubCategory, Transaction.subcategory_id == SubCategory.id)
        .join(Category, SubCategory.category_id == Category.id)
        .filter(Transaction.date >= start_date)
        .group_by(func.date(Transaction.date), Category.type)
        .all()
    )

    cf_labels = sorted({str(row.tanggal) for row in cash_flow_query})
    income_dict = {tgl: 0 for tgl in cf_labels}
    expense_dict = {tgl: 0 for tgl in cf_labels}

    for row in cash_flow_query:
        tgl = str(row.tanggal)
        if row.tipe == "income":
            income_dict[tgl] = float(row.total)
        elif row.tipe == "expense":
            expense_dict[tgl] = float(row.total)

    cf_income_values = [income_dict[tgl] for tgl in cf_labels]
    cf_expense_values = [expense_dict[tgl] for tgl in cf_labels]

    return cf_labels, cf_income_values, cf_expense_values


def _get_expense_allocation(start_date):
    """Mengambil data grafik alokasi pengeluaran per kategori utama."""
    expense_query = (
        db.session.query(Category.nama, func.sum(Transaction.amount))
        .join(SubCategory, Transaction.subcategory_id == SubCategory.id)
        .join(Category, SubCategory.category_id == Category.id)
        .filter(Category.type == "expense")
        .filter(Transaction.date >= start_date)
        .group_by(Category.nama)
        .all()
    )

    exp_labels = [row[0] for row in expense_query]
    exp_values = [float(row[1]) for row in expense_query]

    return exp_labels, exp_values


def _get_account_distribution():
    """Mengambil data grafik distribusi saldo akun."""
    account_query = db.session.query(Account.nama, Account.balance).all()

    acc_labels = [row[0] for row in account_query]
    acc_values = [float(row[1]) for row in account_query]

    return acc_labels, acc_values


@main_bp.route("/")
@main_bp.route("/dashboard")
# (Asumsi ada decorator @main_bp.route di sini)
def dashboard():
    # Rentang waktu: 30 hari terakhir
    hari_ini = datetime.utcnow()
    tiga_puluh_hari_lalu = hari_ini - timedelta(days=30)

    # Memanggil fungsi bantuan untuk masing-masing data
    cf_labels, cf_income, cf_expense = _get_cash_flow_data(tiga_puluh_hari_lalu)
    exp_labels, exp_values = _get_expense_allocation(tiga_puluh_hari_lalu)
    acc_labels, acc_values = _get_account_distribution()

    return render_template(
        "dashboard.html",
        cf_labels=cf_labels,
        cf_income=cf_income,
        cf_expense=cf_expense,
        exp_labels=exp_labels,
        exp_values=exp_values,
        acc_labels=acc_labels,
        acc_values=acc_values,
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
