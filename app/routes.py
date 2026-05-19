# ==========================================
# Nama File: routes.py
# Deskripsi: Rute (URL) yang dimiliki
# Penulis:   Fawwaz Yaqzhan
# Tanggal:   01-04-2026
# Catatan:
#   - Rute memakai app.route
# ==========================================

from decimal import Decimal 
from flask import render_template, request, redirect, url_for
from app.models import db, Category, Account, Transaction, SubCategory, Transfer
from app import app
from datetime import datetime, timedelta
from sqlalchemy import func

# ==========================================
# ROUTE UNTUK MENAMPILKAN HALAMAN WEB
# ==========================================

@app.route('/')
@app.route('/transaksi')
def transaksi():
    # Ambil semua transaksi, urutkan dari yang terbaru
    daftar_transaksi = Transaction.query.order_by(Transaction.date.desc()).all()
    
    # Ambil data akun dan kategori untuk dropdown di Modal Form
    daftar_akun = Account.query.all()
    daftar_kategori = Category.query.all()
    
    return render_template('transaksi.html', 
                           transactions=daftar_transaksi,
                           accounts=daftar_akun,
                           categories=daftar_kategori)

@app.route('/akun')
def akun():
    # Ambil semua data akun dari database
    daftar_akun = Account.query.all()
    # Kirim variabel 'accounts' ke akun.html
    return render_template('akun.html', accounts=daftar_akun)

@app.route('/laporan')
def laporan():
    return render_template('laporan.html')

@app.route('/dropdown')
def dropdown():
    kategori_induk = Category.query.all() 
    return render_template('dropdown.html', categories=kategori_induk)


# ==========================================
# ROUTE UNTUK MENERIMA DATA FORM (POST)
# ==========================================

# 1. Simpan Akun Baru
@app.route('/akun/tambah', methods=['POST'])
def tambah_akun():
    nama_akun = request.form.get('nama')
    tipe_akun = request.form.get('type')
    saldo_awal = request.form.get('balance')

    akun_baru = Account(nama=nama_akun, type=tipe_akun, balance=saldo_awal)
    db.session.add(akun_baru)
    db.session.commit()

    return redirect(url_for('akun')) # Kembali ke halaman akun setelah simpan


# 2. Simpan Kategori Baru
@app.route('/dropdown/kategori/tambah', methods=['POST'])
def tambah_kategori():
    nama_kategori = request.form.get('nama')
    tipe_kategori = request.form.get('type') # 'income' atau 'expense'

    kategori_baru = Category(nama=nama_kategori, type=tipe_kategori)
    db.session.add(kategori_baru)
    db.session.commit()

    return redirect(url_for('dropdown'))


# 3. Simpan Sub-Kategori Baru
@app.route('/dropdown/subkategori/tambah', methods=['POST'])
def tambah_subkategori():
    nama_subkategori = request.form.get('nama')
    kategori_induk_id = request.form.get('category_id')

    sub_baru = SubCategory(nama=nama_subkategori, category_id=kategori_induk_id)
    db.session.add(sub_baru)
    db.session.commit()

    return redirect(url_for('dropdown'))


# 4. Simpan Transaksi Baru & Update Saldo
@app.route('/transaksi/tambah', methods=['POST'])
def tambah_transaksi():
    account_id = request.form.get('account_id')
    subcategory_id = request.form.get('subcategory_id')
    amount = Decimal(request.form.get('amount'))
    note = request.form.get('note')
    
    # HTML <input type="date"> mengirim format string 'YYYY-MM-DD'
    # Kita harus ubah ke objek datetime Python
    tanggal_str = request.form.get('date') 
    date_obj = datetime.strptime(tanggal_str, '%Y-%m-%d')

    # Buat record transaksi baru
    trx_baru = Transaction(
        account_id=account_id,
        subcategory_id=subcategory_id,
        amount=amount,
        date=date_obj,
        note=note
    )
    db.session.add(trx_baru)

    # Lakukan update saldo pada akun terkait
    akun = Account.query.get(account_id)
    subkategori = SubCategory.query.get(subcategory_id)
    
    # Cek tipe dari kategori induknya (income / expense)
    if subkategori.category.type == 'expense':
        akun.balance -= amount
    elif subkategori.category.type == 'income':
        akun.balance += amount

    db.session.commit()

    return redirect(url_for('transaksi'))

# ==========================================
# ROUTE UNTUK HAPUS & EDIT TRANSAKSI
# ==========================================

@app.route('/transaksi/hapus/<int:id>', methods=['POST'])
def hapus_transaksi(id):
    # Cari transaksi berdasarkan ID, jika tidak ada kembalikan 404
    trx = Transaction.query.get_or_404(id)
    
    # Ambil data akun dan tipe kategori transaksi yang akan dihapus
    akun = trx.account
    kategori_tipe = trx.subcategory.category.type
    
    # LOGIKA REVERSAL SALDO
    # Jika transaksi aslinya pengeluaran, uangnya harus dikembalikan ke akun (+)
    # Jika transaksi aslinya pemasukan, uangnya harus ditarik dari akun (-)
    if kategori_tipe == 'expense':
        akun.balance += trx.amount
    elif kategori_tipe == 'income':
        akun.balance -= trx.amount
        
    # Hapus transaksi dari database
    db.session.delete(trx)
    db.session.commit()
    
    return redirect(url_for('transaksi'))


@app.route('/transaksi/edit/<int:id>', methods=['POST'])
def edit_transaksi(id):
    trx = Transaction.query.get_or_404(id)
    
    # ---------------------------------------------------------
    # FASE 1: REVERSAL SALDO LAMA
    # Batalkan efek dari transaksi lama sebelum data diperbarui
    # ---------------------------------------------------------
    tipe_lama = trx.subcategory.category.type
    akun_lama = trx.account
    
    if tipe_lama == 'expense':
        akun_lama.balance += trx.amount
    elif tipe_lama == 'income':
        akun_lama.balance -= trx.amount

    # ---------------------------------------------------------
    # FASE 2: UPDATE DATA TRANSAKSI
    # Masukkan data baru dari form modal
    # ---------------------------------------------------------
    trx.account_id = request.form.get('account_id')
    trx.subcategory_id = request.form.get('subcategory_id')
    trx.amount = Decimal(request.form.get('amount'))
    trx.note = request.form.get('note')
    trx.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d')
    
    # ---------------------------------------------------------
    # FASE 3: TERAPKAN SALDO BARU
    # Potong/tambah saldo akun berdasarkan data yang baru diedit
    # ---------------------------------------------------------
    akun_baru = Account.query.get(trx.account_id)
    subkategori_baru = SubCategory.query.get(trx.subcategory_id)
    tipe_baru = subkategori_baru.category.type
    
    if tipe_baru == 'expense':
        akun_baru.balance -= trx.amount
    elif tipe_baru == 'income':
        akun_baru.balance += trx.amount
        
    # Simpan semua perubahan (update transaksi & update saldo akun)
    db.session.commit()
    
    return redirect(url_for('transaksi'))

# ==========================================
# ROUTE UNTUK HAPUS & EDIT AKUN
# ==========================================

@app.route('/akun/hapus/<int:id>', methods=['POST'])
def hapus_akun(id):
    akun = Account.query.get_or_404(id)
    
    # PERHATIAN: Jika akun dihapus, transaksi yang menggunakan foreign key akun ini 
    # bisa menyebabkan error (IntegrityError) kecuali dikonfigurasi 'cascade delete'.
    # Pastikan akun yang dihapus sedang tidak memiliki transaksi, 
    # atau ubah kode ini jika ingin menghapus transaksi terkait juga.
    
    db.session.delete(akun)
    db.session.commit()
    
    return redirect(url_for('akun'))

@app.route('/akun/edit/<int:id>', methods=['POST'])
def edit_akun(id):
    akun = Account.query.get_or_404(id)
    
    # Update data berdasarkan input dari form modal
    akun.nama = request.form.get('nama')
    akun.type = request.form.get('type')
    akun.balance = Decimal(request.form.get('balance'))
    
    db.session.commit()
    
    return redirect(url_for('akun'))

# ==========================================
# ROUTE UNTUK TRANSFER ANTAR AKUN
# ==========================================

@app.route('/transfer', methods=['POST'])
def proses_transfer():
    from_account_id = request.form.get('from_account_id')
    to_account_id = request.form.get('to_account_id')
    
    amount = Decimal(request.form.get('amount', 0))
    fee = Decimal(request.form.get('fee', 0))
    note = request.form.get('note', '')

    # 1. Validasi Dasar: Jika akun sama atau jumlah <= 0, langsung kembali
    if from_account_id == to_account_id or amount <= 0:
        return redirect(url_for('akun'))

    from_account = Account.query.get(from_account_id)
    to_account = Account.query.get(to_account_id)

    if not from_account or not to_account:
        return redirect(url_for('akun'))

    # 2. Validasi Saldo: Jika saldo kurang, batalkan dan kembali ke akun
    total_deduction = amount + fee
    if from_account.balance < total_deduction:
        return redirect(url_for('akun'))

    # 3. Proses Eksekusi Database
    try:
        from_account.balance -= total_deduction
        to_account.balance += amount

        new_transfer = Transfer(
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            amount=amount,
            fee=fee,
            note=note
        )
        db.session.add(new_transfer)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        # Print error ke terminal untuk kebutuhan debugging kamu
        print(f"Error proses transfer: {e}") 

    # 4. Sukses: Kembali ke halaman akun
    return redirect(url_for('akun'))

# ==========================================
# ROUTE UNTUK HAPUS & EDIT KATEGORI
# ==========================================

@app.route('/dropdown/kategori/hapus/<int:id>', methods=['POST'])
def hapus_kategori(id):
    kategori = Category.query.get_or_404(id)
    
    # Catatan: Sama seperti akun, menghapus kategori yang masih memiliki sub-kategori
    # atau transaksi bisa menyebabkan error database (jika foreign key diaktifkan).
    db.session.delete(kategori)
    db.session.commit()
    
    return redirect(url_for('dropdown'))

@app.route('/dropdown/kategori/edit/<int:id>', methods=['POST'])
def edit_kategori(id):
    kategori = Category.query.get_or_404(id)
    
    kategori.nama = request.form.get('nama')
    kategori.type = request.form.get('type')
    
    db.session.commit()
    return redirect(url_for('dropdown'))

# ==========================================
# ROUTE UNTUK HAPUS & EDIT SUB-KATEGORI
# ==========================================

@app.route('/dropdown/subkategori/hapus/<int:id>', methods=['POST'])
def hapus_subkategori(id):
    subkategori = SubCategory.query.get_or_404(id)
    
    db.session.delete(subkategori)
    db.session.commit()
    
    return redirect(url_for('dropdown'))

@app.route('/dropdown/subkategori/edit/<int:id>', methods=['POST'])
def edit_subkategori(id):
    subkategori = SubCategory.query.get_or_404(id)
    
    subkategori.nama = request.form.get('nama')
    subkategori.category_id = request.form.get('category_id') # Memungkinkan ganti induk kategori
    
    db.session.commit()
    return redirect(url_for('dropdown'))

# ==========================================
# ROUTE HALAMAN DASHBOARD
# ==========================================

@app.route('/dashboard')
def dashboard():
    # Rentang waktu: 30 hari terakhir
    hari_ini = datetime.utcnow()
    tiga_puluh_hari_lalu = hari_ini - timedelta(days=30)

    # ====================================================
    # 1. DATA GRAFIK ARUS KAS (Pemasukan vs Pengeluaran)
    # ====================================================
    cash_flow_query = db.session.query(
        func.date(Transaction.date).label('tanggal'),
        Category.type.label('tipe'),
        func.sum(Transaction.amount).label('total')
    ).join(SubCategory, Transaction.subcategory_id == SubCategory.id)\
     .join(Category, SubCategory.category_id == Category.id)\
     .filter(Transaction.date >= tiga_puluh_hari_lalu)\
     .group_by(func.date(Transaction.date), Category.type)\
     .all()

    # Susun struktur data tanggal agar urut untuk Chart.js
    cf_labels = sorted(list(set([str(row.tanggal) for row in cash_flow_query])))
    
    # Buat template default nilai 0 untuk setiap tanggal yang ada
    income_dict = {tgl: 0 for tgl in cf_labels}
    expense_dict = {tgl: 0 for tgl in cf_labels}
    
    # Isi nilai dari database
    for row in cash_flow_query:
        tgl = str(row.tanggal)
        if row.tipe == 'income':
            income_dict[tgl] = float(row.total)
        elif row.tipe == 'expense':
            expense_dict[tgl] = float(row.total)

    cf_income_values = [income_dict[tgl] for tgl in cf_labels]
    cf_expense_values = [expense_dict[tgl] for tgl in cf_labels]


    # ====================================================
    # 2. DATA GRAFIK ALOKASI PENGELUARAN (Per Kategori Utama)
    # ====================================================
    expense_query = db.session.query(
        Category.nama, 
        func.sum(Transaction.amount)
    ).join(SubCategory, Transaction.subcategory_id == SubCategory.id)\
     .join(Category, SubCategory.category_id == Category.id)\
     .filter(Category.type == 'expense')\
     .filter(Transaction.date >= tiga_puluh_hari_lalu)\
     .group_by(Category.nama).all()

    exp_labels = [row[0] for row in expense_query]
    exp_values = [float(row[1]) for row in expense_query]


    # ====================================================
    # 3. DATA GRAFIK DISTRIBUSI SALDO AKUN
    # ====================================================
    account_query = db.session.query(Account.nama, Account.balance).all()

    acc_labels = [row[0] for row in account_query]
    acc_values = [float(row[1]) for row in account_query]


    # ====================================================
    # KIRIM SEMUA DATA KE TEMPLATE JINJA2
    # ====================================================
    return render_template(
        'dashboard.html',
        # Grafik 1: Arus Kas
        cf_labels=cf_labels,
        cf_income=cf_income_values,
        cf_expense=cf_expense_values,
        # Grafik 2: Alokasi Pengeluaran
        exp_labels=exp_labels,
        exp_values=exp_values,
        # Grafik 3: Saldo Akun
        acc_labels=acc_labels,
        acc_values=acc_values
    )

# ====================================================
# ROUTE HALAMAN LAPORAN
# ====================================================

@app.route('/laporan_hasil')
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
