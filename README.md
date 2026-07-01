# 📊 MyFinance - Personal Finance Tracker

<p align="center">
  <img src="assets/banner.png" alt="MyFinance Banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.1.3-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Code%20Style-Black-000000?style=for-the-badge" alt="Code Style">
  <img src="https://img.shields.io/badge/License-ISC-blue?style=for-the-badge" alt="License">
</p>

Aplikasi pencatat keuangan pribadi berbasis web yang membantu pengguna melacak, menganalisis, dan mengelola arus keuangan mereka secara mandiri, aman, dan terstruktur.

---

## 📌 Daftar Isi

- [📝 Latar Belakang Proyek](#-latar-belakang-proyek)
- [🖥️ Halaman Web & Fitur Utama](#️-halaman-web--fitur-utama)
- [📂 Struktur Proyek](#-struktur-proyek)
- [💻 Tech Stack & Kualitas Kode](#-tech-stack--kualitas-kode)
- [🛡️ Fitur Sistem & Keamanan Database](#️-fitur-sistem--keamanan-database)
- [⚙️ Skrip Otomatisasi (Batch Files)](#-skrip-otomatisasi-batch-files)
- [🚀 Cara Memulai](#-cara-memulai)
- [📸 Galeri Screenshot](#-galeri-screenshot)
- [📄 Lisensi](#-lisensi)

---

## 📝 Latar Belakang Proyek

Pencatatan keuangan secara manual sering kali merepotkan dan tidak terstruktur. Proyek **MyFinance** lahir dari:
- **Kesulitan mencatat keuangan keluar masuk** secara konsisten dan terperinci secara manual.
- Keinginan untuk **membangun sebuah program mandiri** yang praktis, cepat, dan memiliki analisis keuangan cerdas guna memberikan gambaran kesehatan finansial pribadi secara langsung (lokal).

---

## 🖥️ Halaman Web & Fitur Utama

Aplikasi MyFinance terdiri dari beberapa halaman utama dengan fungsi spesifik:

1. **Dashboard (Visualisasi Keuangan)**
   - Ringkasan total saldo dari seluruh akun yang dimiliki.
   - Grafik distribusi saldo antar akun keuangan (rekening, e-wallet, dompet fisik).
   - Grafik pengeluaran berdasarkan kategori utama.
   - Grafik tren harian perbandingan pemasukan vs pengeluaran dalam 30 hari terakhir.

2. **Transaksi (Pencatatan Finansial)**
   - Pencatatan transaksi pemasukan dan pengeluaran.
   - **Modal Form**: Pengisian data transaksi dilakukan menggunakan form modal interaktif tanpa perlu berpindah halaman.
   - Fitur edit dan hapus transaksi dengan kalkulasi *reversal* saldo akun otomatis.

3. **Akun (Manajemen Dompet)**
   - Daftar akun keuangan yang terdaftar beserta rincian saldonya.
   - Pencatatan transfer saldo antar akun dengan opsi biaya admin (*transfer fee*).

4. **Laporan (Ekspor Data)**
   - Filter waktu yang fleksibel: **Hari Ini**, **7 Hari Terakhir**, **Bulan Ini**, serta rentang tanggal **Custom**.
   - Ekspor laporan transaksi langsung ke dalam format **CSV** dan **PDF**.

5. **Dropdown Menu (Pengaturan Kategori)**
   - Mengatur opsi kategori dan subkategori untuk drop-down transaksi.
   - Kustomisasi struktur pengeluaran dan pemasukan sesuai kebutuhan pribadi.

6. **Analisa (Decision Support System & Data Mining)**
   - **DSS Rule-Based**: Penilaian terhadap rasio tabungan bulanan (Finansial Sehat/Aman/Boros) serta rekomendasi langkah keuangan.
   - **Deteksi Anomali**: Menggunakan algoritma *Isolation Forest* untuk mendeteksi transaksi dengan nominal tidak wajar (outliers).
   - **Prediksi Tren**: Menggunakan *Linear Regression* untuk memproyeksikan pengeluaran di bulan berikutnya.
   - **Pola Pembelian (Association Rules)**: Menggunakan algoritma *Apriori* untuk menemukan hubungan subkategori transaksi yang sering dibeli bersamaan pada hari yang sama.

7. **Backup Database**
   - Fasilitas untuk memicu backup database SQLite secara manual langsung dari aplikasi.

---

## 📂 Struktur Proyek

Berikut adalah pohon direktori utama proyek MyFinance untuk memudahkan navigasi kode:

```text
MyFinance/
├── .env.example          # Template konfigurasi environment variables
├── .gitignore            # File & folder yang diabaikan oleh Git
├── README.md             # Dokumentasi utama proyek
├── requirements.txt      # Daftar dependensi Python
├── package.json          # Konfigurasi dependensi Node.js (Linting web)
├── run.py                # Entry point utama untuk menjalankan server Flask
├── run_server.bat        # Batch script untuk backup db & menjalankan server
├── clean_python.bat      # Batch script untuk linter Python (pylint, black, etc.)
├── clean_web.bat         # Batch script untuk linter Web (eslint, prettier, etc.)
├── assets/               # Aset gambar pendukung dokumentasi
│   └── banner.png        # Banner utama README
├── app/                  # Folder kode utama aplikasi (Flask)
│   ├── __init__.py       # Inisialisasi Flask, SQLAlchemy, & Blueprint
│   ├── models.py         # Model database SQLAlchemy (SQLite)
│   ├── backup.bat        # Script backup SQLite internal
│   ├── routes/           # Blueprint rute/kontroller
│   │   ├── akun.py       # Manajemen akun dompet
│   │   ├── dropdown.py   # Manajemen kategori & subkategori
│   │   ├── laporan.py    # Ekspor laporan (CSV & PDF)
│   │   ├── main.py       # Rute dashboard & analisa utama
│   │   └── transaksi.py  # CRUD transaksi keuangan
│   ├── utils/            # Fungsi utilitas penunjang
│   │   ├── analisa.py    # Algoritma DSS, Isolation Forest, Regresi, & Apriori
│   │   └── dashgraph.py  # Pembuatan grafik/chart dashboard
│   ├── static/           # Aset statis frontend (CSS, JS)
│   └── templates/        # Template halaman HTML (Jinja2)
└── notes/                # Laporan/log hasil linting kode (terbuat otomatis)
```

---

## 💻 Tech Stack & Kualitas Kode

### Teknologi Utama
- **Backend**: Python (Flask & Flask-SQLAlchemy)
- **Database**: SQLite (Integritas data & optimasi konkurensi)
- **Frontend**: HTML5, Vanilla CSS, Vanilla JS
- **Visualisasi**: Chart.js (Grafik interaktif)
- **Data Science**: Pandas, NumPy, Scikit-learn, Mlxtend
- **Reporting**: ReportLab (Ekspor PDF)
- **Otomatisasi**: Windows Batch File (`.bat`) & PowerShell

### Pengontrol Kualitas Kode (Linting & Formatting)
Proyek ini mengadopsi standar penulisan kode bersih (*clean code*) dengan integrasi perkakas berikut:

| Stack | Alat (Tool) | Fungsi / Deskripsi |
| :--- | :--- | :--- |
| **Python** | `Black` | Melakukan pemformatan kode (*code formatting*) secara otomatis agar seragam. |
| | `Flake8` | Memeriksa kepatuhan terhadap standar gaya penulisan PEP 8. |
| | `Pylint` | Menganalisis bug potensial, kualitas kode, dan memberikan skor kualitas. |
| | `Vulture` | Mendeteksi kode mati (*dead code*) yang tidak digunakan. |
| **Web Frontend** | `Prettier` | Melakukan pemformatan otomatis pada file JavaScript dan CSS. |
| | `ESLint` | Melakukan analisis statis untuk mendeteksi pola bermasalah pada JavaScript. |
| | `Stylelint` | Memeriksa kesalahan dan merapikan file stylesheet CSS. |
| | `djLint` | Memformat dan melakukan linting pada template HTML (Jinja2). |

---

## 🛡️ Fitur Sistem & Keamanan Database

- **SQLite Foreign Key Constraint**: Mencegah data transaksi yatim-piatu (*orphan data*) yang diakibatkan oleh penghapusan akun keuangan, kategori, atau subkategori secara tidak sengaja.
- **Write-Ahead Logging (WAL) SQLite**: Mode WAL diaktifkan untuk mendukung paralelisasi proses membaca (read) dan menulis (write) pada database, meminimalkan resiko database terkunci (*locked database*) saat diakses secara bersamaan.
- **Flash Message**: Memberikan umpan balik instan berupa pesan sukses (hijau) atau pesan peringatan (merah/kuning) pada bagian atas halaman setelah melakukan operasi CRUD database.

---

## ⚙️ Skrip Otomatisasi (Batch Files)

Dua file batch disediakan untuk mempermudah operasional harian tanpa perlu mengetik command terminal yang rumit:

### 1. Jalankan Server (`run_server.bat`)
Dengan melakukan **double-click** pada file ini, proses berikut berjalan otomatis:
- Memeriksa apakah port server Flask (`5000`) sudah digunakan (mencegah konflik port).
- Melakukan **backup database otomatis** sebelum server menyala, disimpan ke folder `backups/` dengan nama berformat timestamp presisi (`backup_YYYYMMDD_HHMin.db`).
- Mengelola retensi database (menyimpan maksimal 10 file backup terakhir dan menghapus backup yang berumur lebih dari 30 hari).
- Menjalankan virtual environment (`.venv`) dan menyalakan server Flask di latar belakang.
- **Membuka browser default** secara otomatis mengarah ke alamat `http://127.0.0.1:5000` ketika server siap menerima request.

### 2. Pembersihan Kode & Linting Otomatis
- **`clean_python.bat`**: Menjalankan *Black, Flake8, Pylint, dan Vulture* pada seluruh file Python. Hasil analisanya disimpan secara otomatis ke dalam folder `notes/`.
- **`clean_web.bat`**: Menjalankan *djLint, Prettier, ESLint, dan Stylelint* pada file HTML/Jinja, JavaScript, dan CSS. Hasil analisanya disimpan di folder `notes/web/`.

---

## 🚀 Cara Memulai

### Prasyarat:
- [Python 3.x](https://www.python.org/downloads/) terinstal di komputer Anda.
- *(Opsional)* [Node.js](https://nodejs.org/) terinstal jika Anda ingin menggunakan linter web frontend.

### Langkah-Langkah Instalasi:

1. Kloning atau unduh repositori ini ke komputer lokal Anda.
2. Buka terminal di direktori proyek dan buat virtual environment:
   ```powershell
   python -m venv .venv
   ```
3. Aktifkan virtual environment:
   - **Windows PowerShell**:
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - **Windows CMD**:
     ```cmd
     .venv\Scripts\activate.bat
     ```
4. Instal seluruh dependensi yang dibutuhkan:
   ```powershell
   pip install -r requirements.txt
   ```
5. Konfigurasikan Environment Variables:
   - Salin file `.env.example` dan ubah namanya menjadi `.env`
   - Buka file `.env` baru tersebut, lalu isi nilai variabel berikut:
     ```env
     FLASK_SECRET_KEY=<tambahkan kunci rahasia anda di sini>
     ```
6. Jalankan aplikasi dengan melakukan **double-click** pada file **`run_server.bat`**, atau jalankan lewat terminal:
   ```powershell
   .\run_server.bat
   ```
7. Aplikasi akan terbuka secara otomatis di browser Anda di alamat `http://127.0.0.1:5000`.

---

## 📸 Galeri Screenshot

Untuk memberikan gambaran antarmuka aplikasi, Anda dapat menambahkan screenshot di bawah ini:

### 📊 Dashboard
<tambahkan screenshot dashboard di sini>

### 💸 Form Transaksi (Modal)
<tambahkan screenshot form transaksi di sini>

### 🧠 Analisa Finansial (Data Mining & DSS)
<tambahkan screenshot halaman analisa di sini>

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah lisensi ISC.

```text
Copyright (c) 2026 <tambahkan nama Anda di sini>

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
```