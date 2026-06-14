# ==========================================
# Nama File: dashgraph.py
# Deskripsi: Logika grafik dashboard
# Penulis:   Fawwaz Yaqzhan
# Tanggal:   08-06-2026
# Catatan:
#   - Arus kas (Cash flow)
#   - Alokasi dana
#   - Distribusi dana di berbagai akun
# ==========================================

from sqlalchemy import func
from app.models import db, Category, Account, Transaction, SubCategory


def get_cash_flow_data(start_date):
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


def get_expense_allocation(start_date):
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


def get_account_distribution():
    """Mengambil data grafik distribusi saldo akun."""
    account_query = db.session.query(Account.nama, Account.balance).all()

    acc_labels = [row[0] for row in account_query]
    acc_values = [float(row[1]) for row in account_query]

    return acc_labels, acc_values
