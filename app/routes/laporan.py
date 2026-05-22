# ==========================================
# Nama File: laporan.py
# Deskripsi: Rute khusus fitur-fitur halaman laporan
# Penulis:   Fawwaz Yaqzhan
# Tanggal:   20-05-2026
# Catatan:
#   - Hanya rute yang ada di halaman laporan
#   - Rute lain ada di file tersendiri
# ==========================================

from flask import render_template, request, Blueprint
from app.models import db, Category, Transaction, SubCategory
from datetime import datetime, timedelta
from sqlalchemy import func

laporan_bp = Blueprint('laporan', __name__)

@laporan_bp.route('/laporan_hasil')
def laporan_hasil():
    # 1. Ambil string dari filter HTML
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    # 2. KONVERSI WAJIB: Ubah string HTML menjadi objek datetime Python
    if start_date_str and end_date_str:
        # Ubah '2026-05-01' menjadi datetime(2026, 5, 1, 0, 0)
        start_date_obj = datetime.strptime(start_date_str, '%Y-%m-%d')
        # Ubah '2026-05-17' menjadi datetime(2026, 5, 17, 23, 59, 59)
        end_date_raw = datetime.strptime(end_date_str, '%Y-%m-%d')
        end_date_obj = end_date_raw.replace(hour=23, minute=59, second=59)
    else:
        # Default jika filter kosong (Sama persis dengan dashboard Anda: 30 hari terakhir)
        hari_ini = datetime.utcnow()
        start_date_obj = hari_ini - timedelta(days=30)
        end_date_obj = hari_ini
        
        # Siapkan string untuk ditampilkan kembali di form HTML
        start_date_str = start_date_obj.strftime('%Y-%m-%d')
        end_date_str = end_date_obj.strftime('%Y-%m-%d')

    # 3. Query Pengeluaran Kategori (Gunakan objek datetime, samakan dengan dashboard)
    expense_by_category = db.session.query(
        Category.nama.label('category_name'),
        func.sum(Transaction.amount).label('total')
    ).join(SubCategory, Transaction.subcategory_id == SubCategory.id)\
     .join(Category, SubCategory.category_id == Category.id)\
     .filter(Category.type == 'expense')\
     .filter(Transaction.date >= start_date_obj)\
     .filter(Transaction.date <= end_date_obj)\
     .group_by(Category.nama).all()

    # 4. Query Pengeluaran Subkategori
    expense_by_subcategory = db.session.query(
        Category.nama.label('category_name'),
        SubCategory.nama.label('subcategory_name'),
        func.sum(Transaction.amount).label('total')
    ).join(SubCategory, Transaction.subcategory_id == SubCategory.id)\
     .join(Category, SubCategory.category_id == Category.id)\
     .filter(Category.type == 'expense')\
     .filter(Transaction.date >= start_date_obj)\
     .filter(Transaction.date <= end_date_obj)\
     .group_by(Category.nama, SubCategory.nama)\
     .order_by(Category.nama, func.sum(Transaction.amount).desc()).all()

    return render_template(
        'laporan.html', 
        categories=expense_by_category, 
        subcategories=expense_by_subcategory,
        start_date=start_date_str,
        end_date=end_date_str
    )
