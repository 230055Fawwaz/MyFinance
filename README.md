# MyFinance - Personal Finance Tracker

Aplikasi pencatat keuangan pribadi berbasis web yang membantu pengguna melacak, menganalisis, dan mengelola arus keuangan mereka secara mandiri dan terstruktur.

---

## 📝 Latar Belakang Proyek

Pencatatan keuangan secara manual sering kali merepotkan dan tidak terstruktur. Proyek **MyFinance** lahir dari:
- **Kesulitan mencatat keuangan keluar masuk** secara konsisten dan terperinci secara manual.
- Keinginan untuk **membangun sebuah program mandiri** yang praktis, cepat, dan memiliki analisis keuangan cerdas guna memberikan gambaran kesehatan finansial pribadi.

---

## 💻 Tech Stack

Aplikasi ini menggunakan teknologi yang ringan namun tangguh untuk menjamin performa lokal yang maksimal:

- **Backend**: [Python](https://www.python.org/) & [Flask](https://flask.palletsprojects.com/) (Vanilla Python / Flask-SQLAlchemy)
- **Database**: [SQLite](https://www.sqlite.org/) (dilengkapi constraint integritas data dan optimasi konkurensi)
- **Frontend**: HTML5, Vanilla CSS, Vanilla JS
- **Visualisasi**: [Chart.js](https://www.chartjs.org/) (untuk representasi grafis interaktif)
- **Analisis & Data Mining**: Pandas, NumPy, Scikit-learn, Mlxtend
- **Reporting**: ReportLab (untuk dokumen PDF)
- **Otomatisasi**: Windows Batch File (`.bat`) & PowerShell

---

## 🔍 Pembersih Kode dan Linting (Code Quality & Style Guides)

Untuk menjaga konsistensi gaya penulisan dan kualitas kode (clean code), proyek ini didukung oleh berbagai tools linting dan formatting:

### Python Stack:
- **Vulture**: Mendeteksi kode mati (*dead code*) yang tidak digunakan.
- **Flake8**: Memeriksa kepatuhan terhadap standar gaya penulisan PEP 8.
- **Black**: Melakukan pemformatan kode (*code formatting*) secara otomatis agar seragam.
- **Pylint**: Menganalisis bug potensial, kualitas kode, dan memberikan skor kualitas.

### Web Frontend Stack:
- **djLint**: Memformat dan melakukan linting pada template HTML (Jinja2).
- **Prettier**: Melakukan pemformatan otomatis pada file JavaScript dan CSS.
- **ESLint**: Melakukan analisis statis untuk mendeteksi pola bermasalah pada JavaScript.
- **Stylelint**: Memeriksa kesalahan dan merapikan file stylesheet CSS.

---

## 🖥️ Halaman Web & Fitur Aplikasi

Aplikasi MyFinance terdiri dari beberapa halaman utama dengan fungsi spesifik:

1. **Dashboard (Visualisasi Keuangan)**
   - Menampilkan ringkasan saldo total dari seluruh akun.
   - Grafik distribusi saldo antar akun yang dimiliki.
   - Grafik pengeluaran berdasarkan kategori utama.
   - Grafik tren harian untuk membandingkan total pemasukan dan pengeluaran dalam 30 hari terakhir.

2. **Transaksi (Pencatatan Finansial)**
   - Pencatatan transaksi pemasukan dan pengeluaran.
   - **Modal Form**: Pengisian data transaksi dilakukan menggunakan form modal yang interaktif tanpa perlu berpindah halaman.
   - Fitur edit dan hapus transaksi dengan kalkulasi *reversal* saldo akun otomatis.

3. **Akun (Manajemen Dompet)**
   - Menampilkan daftar akun keuangan yang terdaftar (misalnya: Rekening Bank, Dompet Fisik, E-Wallet) beserta rincian jumlah uang di dalamnya.
   - Mendukung pencatatan transfer saldo antar akun dengan opsi biaya admin (*transfer fee*).

4. **Laporan (Eksport Data)**
   - Menyediakan filter waktu yang fleksibel untuk melihat riwayat transaksi: **Hari Ini**, **7 Hari Terakhir**, **Bulan Ini**, serta rentang tanggal **Custom**.
   - Fitur ekspor laporan transaksi langsung ke dalam format **CSV** dan **PDF**.

5. **Dropdown Menu (Pengaturan Kategori)**
   - Halaman khusus untuk mengatur opsi kategori dan subkategori yang akan digunakan dalam dropdown form modal transaksi.
   - Mempermudah kustomisasi struktur pengeluaran dan pemasukan sesuai kebutuhan pribadi.

6. **Analisa (Decision Support System & Data Mining)**
   - **DSS Rule-Based**: Memberikan penilaian terhadap rasio tabungan bulanan (Finansial Sehat/Aman/Boros) serta rekomendasi langkah keuangan.
   - **Deteksi Anomali**: Menggunakan algoritma *Isolation Forest* untuk mendeteksi transaksi dengan nominal tidak wajar (outliers).
   - **Prediksi Tren**: Menggunakan *Linear Regression* untuk memproyeksikan total pengeluaran di bulan berikutnya.
   - **Pola Pembelian (Association Rules)**: Menggunakan algoritma *Apriori* untuk menemukan hubungan subkategori transaksi yang sering dibeli bersamaan pada hari yang sama.

7. **Backup Database**
   - Fasilitas untuk memicu backup database SQLite secara manual demi keamanan data.

---

## 🛡️ Fitur Sistem & Keamanan Database

- **SQLite Foreign Key Constraint**: Secara ketat mencegah adanya data transaksi yatim-piatu (*orphan data*) yang diakibatkan oleh penghapusan akun keuangan, kategori, atau subkategori secara tidak sengaja.
- **Write-Ahead Logging (WAL) SQLite**: Mode WAL diaktifkan untuk mendukung paralelisasi proses membaca (read) dan menulis (write) pada database, meminimalkan resiko database terkunci (*locked database*) saat diakses bersamaan.
- **Flash Message**: Memberikan umpan balik instan berupa pesan sukses (hijau) atau pesan peringatan (merah/kuning) pada bagian atas halaman setelah melakukan operasi CRUD database.

---

## ⚙️ Fungsi Batch File (`.bat`)

Dua file batch disediakan untuk mempermudah operasional harian tanpa perlu mengetik command terminal yang rumit:

### 1. Mempermudah Menjalankan Server (`run_server.bat`)
Dengan cukup melakukan **klik dua kali (double click)** pada file ini, proses berikut berjalan otomatis:
- Memeriksa apakah server Flask sudah menyala di port terkait (mencegah konflik port).
- Melakukan **backup database otomatis** sebelum server menyala, disimpan ke folder `backups/` dengan nama berformat timestamp presisi (`backup_YYYYMMDD_HHMin.db`).
- Mengelola kebijakan retensi database (menyimpan maksimal 10 file backup terakhir dan menghapus backup yang berumur lebih dari 30 hari).
- Menjalankan virtual environment (`.venv`) dan menyalakan server Flask di latar belakang.
- Secara otomatis **membuka browser default** mengarah ke alamat `http://127.0.0.1:5000` ketika server siap menerima request.

### 2. Pembersihan Kode & Linting Otomatis
- **`clean_python.bat`**: Menjalankan *Black, Flake8, Pylint, dan Vulture* pada seluruh file Python. Hasil analisanya disimpan secara otomatis ke dalam folder `notes/`.
- **`clean_web.bat`**: Menjalankan *djLint, Prettier, ESLint, dan Stylelint* pada file HTML/Jinja, JavaScript, dan CSS. Hasil analisanya disimpan di folder `notes/web/`.

---

## 🚀 Cara Memulai

### Prasyarat:
- [Python 3.x](https://www.python.org/downloads/) terinstal di komputer Anda.

### Cara Menjalankan:
1. Kloning atau unduh repositori ini ke komputer lokal Anda.
2. Buka terminal di direktori proyek dan buat virtual environment:
   ```powershell
   python -m venv .venv
   ```
3. Aktifkan virtual environment:
   ```powershell
   # Windows PowerShell
   .venv\Scripts\Activate.ps1
   
   # Windows CMD
   .venv\Scripts\activate.bat
   ```
4. Instal seluruh dependensi yang dibutuhkan:
   ```powershell
   pip install -r requirements.txt
   ```
5. Jalankan aplikasi dengan melakukan **double click** pada file **`run_server.bat`**, atau jalankan lewat terminal:
   ```powershell
   .\run_server.bat
   ```
6. Aplikasi akan terbuka secara otomatis di browser Anda di alamat `http://127.0.0.1:5000`.