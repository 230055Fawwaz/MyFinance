# MyFinance - Personal Finance Tracker

Aplikasi pencatat keuangan pribadi berbasis web yang dikembangkan menggunakan **Python (Flask)** untuk backend, **SQLite** untuk database, serta **HTML**, **Vanilla CSS**, dan **Vanilla JS** untuk frontend. Aplikasi ini dilengkapi dengan visualisasi grafik menggunakan **Chart.js** dan algoritma **Machine Learning** sederhana untuk analisis keuangan yang lebih mendalam.

---

## 🚀 Fitur Utama

1. **Dashboard Dinamis**:
   - Visualisasi arus kas (pemasukan vs pengeluaran) harian dalam 30 hari terakhir.
   - Grafik alokasi pengeluaran berdasarkan kategori utama.
   - Grafik distribusi saldo di berbagai akun keuangan.

2. **Manajemen Transaksi**:
   - Pencatatan transaksi pemasukan dan pengeluaran secara terperinci.
   - Edit dan hapus transaksi dengan mekanisme *reversal saldo* otomatis (saldo akun disesuaikan kembali saat transaksi diubah/dihapus).

3. **Manajemen Akun & Transfer**:
   - Mendukung banyak akun keuangan (misalnya: Dompet, Rekening Bank, E-Wallet).
   - Fitur transfer saldo antar akun dengan opsi biaya admin (*transfer fee*).

4. **Kategori & Subkategori**:
   - Pengelompokan transaksi yang fleksibel menggunakan relasi satu-ke-banyak (Kategori utama ke Subkategori).

5. **Laporan & Export Data**:
   - Filter laporan berdasarkan rentang tanggal.
   - Export laporan keuangan teragregasi ke dalam format **CSV** dan **PDF** (menggunakan ReportLab).

6. **Analisis Keuangan Cerdas (DSS & Data Mining)**:
   - **DSS Rule-Based**: Evaluasi rasio menabung bulanan disertai status kesehatan keuangan ("SANGAT SEHAT", "AMAN", "WASPADA/BOROS") dan rekomendasi finansial.
   - **Deteksi Anomali**: Menggunakan algoritma **Isolation Forest** (scikit-learn) untuk mendeteksi transaksi pengeluaran yang tidak wajar (outlier).
   - **Prediksi Pengeluaran**: Menggunakan **Linear Regression** untuk memproyeksikan total pengeluaran pada bulan berikutnya berdasarkan tren historis.
   - **Analisis Pola Hubungan**: Menggunakan algoritma **Apriori** (mlxtend) untuk menemukan pola hubungan transaksi subkategori yang sering terjadi pada hari yang sama.

---

## 🛠️ Arsitektur & Struktur Proyek

```text
MyFinance/
├── app/
│   ├── routes/              # Controller / Endpoint Blueprint Flask
│   │   ├── akun.py          # Manajemen akun & saldo
│   │   ├── dropdown.py      # Kategori dan subkategori
│   │   ├── laporan.py       # Pembuatan laporan CSV & PDF
│   │   ├── main.py          # Halaman dashboard & halaman utama
│   │   └── transaksi.py     # Transaksi & transfer saldo
│   ├── static/              # Asset frontend (CSS & JS)
│   │   ├── css/             # Stylesheet vanilla CSS per halaman
│   │   └── js/              # Script logic vanilla JS per halaman
│   ├── templates/           # Layout HTML dengan template engine Jinja2
│   ├── utils/               # Logika pemrosesan data
│   │   ├── analisa.py       # DSS & algoritma data mining (sklearn, mlxtend)
│   │   └── dashgraph.py     # Penyiapan dataset grafik dashboard
│   ├── __init__.py          # Inisialisasi Flask, database SQLite, & Blueprint
│   └── backup.bat           # Script batch untuk backup database manual
├── backups/                 # Folder penyimpanan riwayat database backup
├── notes/                   # Laporan otomatis hasil pembersihan python/web
├── clean_python.bat         # Script otomatisasi linting/formatting Python
├── clean_web.bat            # Script otomatisasi linting/formatting Frontend
├── myfinance.db             # File database SQLite
├── requirements.txt         # Daftar dependensi Python
├── run.py                   # Entry point aplikasi Flask
└── run_server.bat           # Script otomatisasi penyalaan server & backup
```

---

## 💻 Tech Stack

- **Backend**: Python 3, Flask, Flask-SQLAlchemy (ORM)
- **Database**: SQLite
- **Frontend**: HTML5, Vanilla CSS, Vanilla JS, Jinja2
- **Data Analytics & ML**: Pandas, NumPy, Scikit-learn, Mlxtend
- **Reporting**: ReportLab (PDF Generator)
- **Visualisasi**: Chart.js (v2/v3)
- **Automation/DevOps**: Windows Batch (.bat), PowerShell

---

## 🏁 Cara Menjalankan Aplikasi

Aplikasi ini telah dioptimalkan untuk berjalan di lingkungan Windows menggunakan script batch otomatis (`run_server.bat`).

### Prasyarat
1. Pastikan **Python 3** sudah terinstal dan berada dalam sistem `PATH`.
2. Pastikan file database (`myfinance.db`) dan dependensi di `requirements.txt` sudah siap.

### Langkah-langkah:
1. Hubungkan terminal ke folder proyek dan buat virtual environment (jika belum ada):
   ```bash
   python -m venv .venv
   ```
2. Aktifkan virtual environment dan instal dependensi:
   ```bash
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Cukup jalankan file **`run_server.bat`** dengan melakukan klik dua kali (double click) atau via terminal:
   ```cmd
   run_server.bat
   ```

**Apa saja yang dilakukan `run_server.bat` secara otomatis?**
- Memeriksa apakah ada proses server Python yang sedang berjalan untuk menghindari konflik port.
- Melakukan **backup database otomatis** ke dalam folder `backups/` dengan format nama berdasarkan waktu presisi (`backup_YYYYMMDD_HHMin.db`).
- Menjalankan kebijakan **retensi backup** via PowerShell (menyimpan 10 backup terakhir dan menghapus backup yang lebih tua dari 30 hari).
- Menyalakan server Flask secara latar belakang (background process).
- Memeriksa kesiapan port server Flask menggunakan `curl`, lalu secara otomatis **membuka browser** ke alamat `http://127.0.0.1:5000`.

---

## 🧹 Script Otomatisasi Developer

Untuk menjaga kualitas dan kerapihan penulisan kode, disediakan dua batch file pembersih kode:

### 1. Pembersihan Kode Python (`clean_python.bat`)
Script ini mengotomatiskan proses penataan kode python menggunakan 4 alat analisis:
- **Vulture**: Mencari kode mati (*dead code*) yang tidak pernah terpanggil.
- **Black**: Melakukan formatting otomatis agar kode konsisten sesuai standar PEP 8.
- **Flake8**: Menganalisis *syntax error* dan pelanggaran gaya penulisan kode.
- **Pylint**: Menganalisis kualitas kode secara menyeluruh dan memberikan skor.

Hasil analisis dan log pembersihan akan disimpan secara otomatis di folder `notes/laporan_pembersihan_XXX.txt`.

### 2. Pembersihan Kode Frontend/Web (`clean_web.bat`)
Script ini merapikan file HTML (Jinja), JS, dan CSS menggunakan:
- **djLint**: Memformat dan memeriksa kebersihan struktur HTML yang berada di template Jinja.
- **Prettier & ESLint**: Merapikan dan menganalisis kualitas kode JavaScript (tanpa menyentuh pustaka vendor seperti `chart.min.js`).
- **Stylelint**: Memformat file CSS secara otomatis.

Hasil analisis dan log pembersihan web akan disimpan di `notes/web/laporan_pembersihan_XXX.txt`.