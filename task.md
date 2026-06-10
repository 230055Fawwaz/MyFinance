# Daftar Tugas Optimasi Startup Server

- [x] Optimasi Python Backend (Lazy Loading)
  - [x] Pindahkan impor di `app/utils/analisa.py` ke dalam fungsi masing-masing
  - [x] Pindahkan impor pandas di `app/routes/main.py` ke dalam route `/analisa`
  - [x] Pindahkan impor reportlab di `app/routes/laporan.py` ke dalam route `/laporan/download/pdf`
- [x] Optimasi Batch Script (`run_server.bat`)
  - [x] Ubah urutan jalannya Flask server agar di-start di awal secara paralel
  - [x] Optimasi parsing tanggal/waktu tanpa menggunakan `wmic` yang lambat
  - [x] Jalankan pengecekan `curl` pertama kali sebelum menunggu (polling)
- [x] Verifikasi Hasil Perubahan
  - [x] Jalankan server Flask dan uji apakah startup lebih cepat
  - [x] Verifikasi halaman `/dashboard` dan `/analisa` serta unduhan PDF tetap berfungsi normal
