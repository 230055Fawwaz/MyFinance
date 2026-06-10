# Rencana Optimasi Kecepatan Startup Server Flask

Dokumen ini menjelaskan analisis masalah performa startup dan rencana perbaikan untuk mempercepat waktu server terbuka saat dijalankan menggunakan `run_server.bat`.

## Sumber Masalah (Identifikasi)

Setelah meneliti kode aplikasi, ditemukan beberapa penyebab utama lambatnya startup server:

1. **Impor Modul Berat di Awal (Top-Level Imports)**:
   - Di [analisa.py](file:///d:/Projek%20Pribadi/Vibe%20Coding/MyFinance/app/utils/analisa.py), library besar seperti `pandas`, `sklearn` (scikit-learn), dan `mlxtend` diimpor di level atas. Modul ini selalu diimpor ketika Flask melakukan inisialisasi route di [main.py](file:///d:/Projek%20Pribadi/Vibe%20Coding/MyFinance/app/routes/main.py), meskipun halaman analisis tidak dibuka. Ini memakan waktu 1.5 - 2.5 detik.
   - Di [laporan.py](file:///d:/Projek%20Pribadi/Vibe%20Coding/MyFinance/app/routes/laporan.py), modul `reportlab` diimpor di level atas, padahal hanya digunakan saat mengunduh PDF.
   - Di [main.py](file:///d:/Projek%20Pribadi/Vibe%20Coding/MyFinance/app/routes/main.py), `pandas` diimpor di level atas.

2. **Inisialisasi Batch Script yang Lambat & Sinkron**:
   - Di [run_server.bat](file:///d:/Projek%20Pribadi/Vibe%20Coding/MyFinance/run_server.bat), perintah `wmic` dan `powershell` dijalankan secara sinkron sebelum server Flask dinyalakan. Memanggil PowerShell dari Batch memakan waktu ~1.5 - 2 detik.
   - Server Flask baru dinyalakan *setelah* seluruh proses backup dan pembersihan selesai.

3. **Polling Siap Pakai dengan Delay Wajib**:
   - Skrip `run_server.bat` melakukan `timeout /t 1` *sebelum* memeriksa apakah Flask siap dengan `curl`. Ini menambahkan delay minimal 1 detik yang tidak perlu jika server sudah menyala cepat.

---

## Solusi yang Diusulkan

### 1. Lazy Loading (Impor Tertunda) pada Python
Memindahkan impor library berat ke dalam fungsi/rute yang membutuhkannya, sehingga tidak memperlambat startup awal Flask:
- Pindahkan impor `pandas`, `sklearn`, dan `mlxtend` ke dalam masing-masing fungsi analisis di [analisa.py](file:///d:/Projek%20Pribadi/Vibe%20Coding/MyFinance/app/utils/analisa.py).
- Pindahkan impor `pandas` ke dalam fungsi `halaman_analisa` di [main.py](file:///d:/Projek%20Pribadi/Vibe%20Coding/MyFinance/app/routes/main.py).
- Pindahkan impor `reportlab` ke dalam fungsi `download_pdf` di [laporan.py](file:///d:/Projek%20Pribadi/Vibe%20Coding/MyFinance/app/routes/laporan.py).

### 2. Optimasi Alur Kerja `run_server.bat`
- **Paralelisasi**: Jalankan perintah `start "Flask Server" ...` terlebih dahulu agar server Flask mulai inisialisasi di background. Sementara Flask sedang menyala, jalankan proses backup database dan retensi file.
- **Optimasi Tanggal**: Gunakan variabel bawaan CMD `%date%` dan `%time%` dengan fallback cerdas daripada memanggil `wmic` yang lambat dan deprecated.
- **Optimasi Polling**: Lakukan pengecekan `curl` pertama kali tanpa menunggu, dan hanya lakukan `timeout` jika server memang belum siap.

---

## Proposed Changes

### App Backend (Python)

#### [MODIFY] [analisa.py](file:///d:/Projek%20Pribadi/Vibe Coding/MyFinance/app/utils/analisa.py)
- Pindahkan impor `pandas` ke dalam fungsi yang membutuhkannya.
- Pindahkan `from sklearn.ensemble import IsolationForest` ke dalam `deteksi_anomali_pengeluaran`.
- Pindahkan `from sklearn.linear_model import LinearRegression` ke dalam `prediksi_pengeluaran_bulan_depan`.
- Pindahkan `from mlxtend.frequent_patterns import apriori, association_rules` ke dalam `analisis_hubungan_kategori`.

#### [MODIFY] [main.py](file:///d:/Projek%20Pribadi/Vibe Coding/MyFinance/app/routes/main.py)
- Pindahkan `import pandas as pd` ke dalam fungsi `halaman_analisa`.

#### [MODIFY] [laporan.py](file:///d:/Projek%20Pribadi/Vibe Coding/MyFinance/app/routes/laporan.py)
- Pindahkan impor `reportlab` ke dalam fungsi `download_pdf`.

### Automation (Batch)

#### [MODIFY] [run_server.bat](file:///d:/Projek%20Pribadi/Vibe Coding/MyFinance/run_server.bat)
- Ubah urutan eksekusi: jalankan Flask server terlebih dahulu di background (`start`).
- Lakukan proses backup database dan retensi backup *setelah* Flask dijalankan secara paralel.
- Gunakan cara pemrosesan string tanggal/waktu yang cepat atau jalankan pembersihan di background.
- Ubah logika loop `:tunggu` agar memeriksa terlebih dahulu dengan `curl` sebelum melakukan timeout.

---

## Verification Plan

### Automated Tests
- Menjalankan server Flask dan mengukur waktu impor sebelum dan sesudah perubahan.
- Membuka halaman `/dashboard` dan `/analisa` untuk memastikan fungsionalitas berjalan normal.

### Manual Verification
- Menjalankan `run_server.bat` secara manual dan mengukur waktu dari klik bat hingga browser terbuka secara otomatis.
- Memastikan file backup berhasil dibuat di direktori `backups/` dan retensi 10 file tetap terjaga.
