# 💰 MyFinance

Aplikasi pencatatan keuangan pribadi berbasis web yang dirancang untuk memudahkan pelacakan arus kas, analisis pengeluaran, dan manajemen akun keuangan Anda. 

Berawal dari kesulitan mencatat uang keluar-masuk secara manual, MyFinance dibangun untuk menjadi solusi praktis, otomatis, dan dilengkapi dengan visualisasi data yang informatif.

---

## ✨ Fitur Utama

### 📊 Halaman & Fungsionalitas Web
* **Dashboard:** Visualisasi komprehensif berisi total saldo akun, pengeluaran per kategori, serta tren pemasukan dan pengeluaran dalam 30 hari terakhir menggunakan Chart.js.
* **Transaksi:** Pencatatan pemasukan dan pengeluaran yang cepat melalui antarmuka *form modal* responsif.
* **Akun:** Manajemen daftar akun keuangan beserta detail saldo terkini.
* **Laporan:** Pembuatan laporan keuangan dinamis (hari ini, 7 hari terakhir, bulan ini, atau tanggal kustom) dengan opsi ekspor ke format **CSV** dan **PDF**.
* **Dropdown Menu:** Pengaturan kategori dan subkategori yang fleksibel untuk digunakan pada form transaksi.
* **Analisa:** Terintegrasi dengan *Decision Support System* (DSS) dan *data mining* untuk memberikan *insight* cerdas mengenai kondisi kesehatan keuangan saat ini.
* **Backup Database:** Fitur pencadangan data sekali klik untuk keamanan informasi keuangan Anda.

### 🛠 Fitur Teknis & Performa
* **Integritas Data:** Menggunakan *Foreign Key Constraint* SQLite untuk mencegah data yatim (*orphan data*) akibat penghapusan akun atau kategori.
* **Performa Optimal:** Mengimplementasikan mode WAL (*Write-Ahead Logging*) pada SQLite untuk paralelisasi proses baca dan tulis yang lebih cepat.
* **UX Interaktif:** Dilengkapi dengan *Flash Messages* untuk notifikasi sukses atau peringatan *error*.
* **Otomatisasi Batch:** Menjalankan server Flask sangat mudah, cukup klik ganda pada *batch file* tanpa perlu repot mengetik perintah di terminal.

---

## 💻 Teknologi yang Digunakan

* **Backend:** Flask, Python (Vanilla)
* **Frontend:** HTML5, CSS3 (Vanilla), JavaScript (Vanilla), Chart.js
* **Database:** SQLite

---

## 🧹 Code Quality & Linting
Proyek ini sangat memperhatikan kebersihan, standar, dan konsistensi penulisan kode. Berbagai alat *linting* dan *formatter* digunakan dalam pengembangannya:

* **Python:** Vulture, Flake8, Black, Pylint
* **Frontend (Web):** Prettier, ESLint, Stylelint, djLint
* **Skrip Pembersih Otomatis:** Telah disediakan `clean_python.bat` dan `clean_web.bat` untuk menjalankan proses perapian kode secara instan.

---

## 🚀 Cara Menjalankan Proyek

1. *Clone* repositori ini ke komputer Anda.
2. Pastikan Python sudah terinstal di sistem Anda.
3. Instal semua dependensi yang dibutuhkan (jika Anda menggunakan `requirements.txt`, jalankan `pip install -r requirements.txt`).
4. Jalankan aplikasi dengan mengklik dua kali pada *batch file* yang tersedia. 
5. Buka *browser* dan akses *localhost* yang tertera pada terminal. Server Flask sudah menyala dan siap digunakan!
