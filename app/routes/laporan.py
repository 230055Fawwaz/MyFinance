# ==========================================
# Nama File: laporan.py
# Deskripsi: Rute khusus fitur-fitur halaman laporan
# Penulis:   Fawwaz Yaqzhan
# Tanggal:   20-05-2026
# Catatan:
#   - Hanya rute yang ada di halaman laporan
#   - Rute lain ada di file tersendiri
# ==========================================

from io import StringIO, BytesIO
import csv
from datetime import datetime, timedelta
from sqlalchemy import func

from flask import render_template, request, Blueprint, Response
from app.models import db, Category, Transaction, SubCategory

laporan_bp = Blueprint("laporan", __name__)


@laporan_bp.route("/laporan_hasil")
def laporan_hasil():
    # 1. Ambil string dari filter HTML
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")

    # 2. KONVERSI WAJIB: Ubah string HTML menjadi objek datetime Python
    if start_date_str and end_date_str:
        # Ubah '2026-05-01' menjadi datetime(2026, 5, 1, 0, 0)
        start_date_obj = datetime.strptime(start_date_str, "%Y-%m-%d")
        # Ubah '2026-05-17' menjadi datetime(2026, 5, 17, 23, 59, 59)
        end_date_raw = datetime.strptime(end_date_str, "%Y-%m-%d")
        end_date_obj = end_date_raw.replace(hour=23, minute=59, second=59)
    else:
        # Default jika filter kosong (Sama persis dengan dashboard Anda: 30 hari terakhir)
        hari_ini = datetime.utcnow()
        start_date_obj = hari_ini - timedelta(days=30)
        end_date_obj = hari_ini

        # Siapkan string untuk ditampilkan kembali di form HTML
        start_date_str = start_date_obj.strftime("%Y-%m-%d")
        end_date_str = end_date_obj.strftime("%Y-%m-%d")

    # 3. Query Pengeluaran Kategori (Gunakan objek datetime, samakan dengan dashboard)
    expense_by_category = (
        db.session.query(
            Category.nama.label("category_name"),
            func.sum(Transaction.amount).label("total"),
        )
        .join(SubCategory, Transaction.subcategory_id == SubCategory.id)
        .join(Category, SubCategory.category_id == Category.id)
        .filter(Category.type == "expense")
        .filter(Transaction.date >= start_date_obj)
        .filter(Transaction.date <= end_date_obj)
        .group_by(Category.nama)
        .all()
    )

    # 4. Query Pengeluaran Subkategori
    expense_by_subcategory = (
        db.session.query(
            Category.nama.label("category_name"),
            SubCategory.nama.label("subcategory_name"),
            func.sum(Transaction.amount).label("total"),
        )
        .join(SubCategory, Transaction.subcategory_id == SubCategory.id)
        .join(Category, SubCategory.category_id == Category.id)
        .filter(Category.type == "expense")
        .filter(Transaction.date >= start_date_obj)
        .filter(Transaction.date <= end_date_obj)
        .group_by(Category.nama, SubCategory.nama)
        .order_by(Category.nama, func.sum(Transaction.amount).desc())
        .all()
    )

    return render_template(
        "laporan.html",
        categories=expense_by_category,
        subcategories=expense_by_subcategory,
        start_date=start_date_str,
        end_date=end_date_str,
    )


def ambil_data_agregasi(start_date_str, end_date_str):
    """Fungsi pembantu untuk memfilter dan mengagregasi total pengeluaran"""

    # Query 1: Total berdasarkan Kategori Utama
    query = (
        db.session.query(
            Category.nama.label("category_name"),
            func.sum(Transaction.amount).label("total"),
        )
        .join(SubCategory, Transaction.subcategory_id == SubCategory.id)
        .join(Category, SubCategory.category_id == Category.id)
    )

    # Query 2: Total berdasarkan Subkategori
    query_sub = (
        db.session.query(
            Category.nama.label("category_name"),
            SubCategory.nama.label("subcategory_name"),
            func.sum(Transaction.amount).label("total"),
        )
        .join(SubCategory, Transaction.subcategory_id == SubCategory.id)
        .join(Category, SubCategory.category_id == Category.id)
    )

    # Terapkan filter tanggal jika dikirim oleh frontend
    if start_date_str:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        query = query.filter(Transaction.date >= start_date)
        query_sub = query_sub.filter(Transaction.date >= start_date)
    if end_date_str:
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        query = query.filter(Transaction.date <= end_date)
        query_sub = query_sub.filter(Transaction.date <= end_date)

    # Eksekusi query dengan pengelompokan yang tepat
    categories = query.group_by(Category.id, Category.nama).all()
    subcategories = query_sub.group_by(
        Category.id, Category.nama, SubCategory.id, SubCategory.nama
    ).all()

    return categories, subcategories


@laporan_bp.route("/laporan/download/csv")
def download_csv():
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")

    categories, subcategories = ambil_data_agregasi(start_date, end_date)

    si = StringIO()
    cw = csv.writer(si)

    # Menulis header CSV
    cw.writerow(["Kategori / Subkategori", "Jenis", "Total Pengeluaran"])

    for cat in categories:
        cw.writerow([cat.category_name, "Kategori Utama", cat.total])
        for sub in subcategories:
            if sub.category_name == cat.category_name:
                cw.writerow([sub.subcategory_name, "Subkategori", sub.total])

    response = Response(si.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = (
        f"attachment; filename=laporan_pengeluaran_{start_date}_to_{end_date}.csv"
    )
    return response


@laporan_bp.route("/laporan/download/pdf")
def download_pdf():
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")

    # Defer reportlab imports
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors

    categories, subcategories = ambil_data_agregasi(start_date, end_date)

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )
    story = []

    styles = getSampleStyleSheet()
    story.append(Paragraph("<b>Laporan Analisis Pengeluaran</b>", styles["Title"]))
    if start_date and end_date:
        story.append(
            Paragraph(
                f"<font color='grey'>Periode: {start_date} s/d {end_date}</font>",
                styles["Normal"],
            )
        )
    story.append(Spacer(1, 20))

    # Struktur matriks tabel PDF mengikuti logika hierarki HTML Anda
    table_data = [["Kategori / Subkategori", "Total Pengeluaran"]]

    # Variabel penampung styling baris dinamis (untuk membedakan warna subkategori)
    table_styles = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#343a40")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dee2e6")),
    ]

    row_idx = 1
    for cat in categories:
        table_data.append([cat.category_name, f"Rp {cat.total:,.2f}"])
        table_styles.append(("fontname", (0, row_idx), (-1, row_idx), "Helvetica-Bold"))
        table_styles.append(
            ("BACKGROUND", (0, row_idx), (-1, row_idx), colors.HexColor("#f8f9fa"))
        )
        row_idx += 1

        for sub in subcategories:
            if sub.category_name == cat.category_name:
                table_data.append(
                    [f"  • {sub.subcategory_name}", f"Rp {sub.total:,.2f}"]
                )
                table_styles.append(
                    (
                        "TEXTCOLOR",
                        (0, row_idx),
                        (-1, row_idx),
                        colors.HexColor("#6c757d"),
                    )
                )
                row_idx += 1

    t_table = Table(table_data, colWidths=[350, 180])
    t_table.setStyle(TableStyle(table_styles))

    story.append(t_table)
    doc.build(story)

    buffer.seek(0)
    response = Response(buffer.getvalue(), mimetype="application/pdf")
    response.headers["Content-Disposition"] = (
        f"attachment; filename=laporan_pengeluaran_{start_date}_to_{end_date}.pdf"
    )
    return response
