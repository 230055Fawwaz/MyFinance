REM ==========================================
REM Nama File: run_server.bat
REM Deskripsi: Otomatisasi dalam menyalakan server flask
REM Penulis:   Fawwaz Yaqzhan
REM Tanggal:   02-04-2026
REM Catatan:
REM   - Menjalankan server Flask
REM   - Membuka browser
REM   - Error handling untuk mengecek environment virtual
REM ==========================================

@echo off
cd /d %~dp0

:: 1. Validasi cek apakah virtual environment ada
if not exist .venv\Scripts\activate (
    echo [ERROR] Virtual Environment .venv tidak ditemukan!
    goto error
)

:: 2. Aktifkan venv
call .venv\Scripts\activate

:: 3. Jalankan server Flask di latar belakang (background) menggunakan 'start'
:: Ini membuat Flask menyala, dan CMD utama bisa lanjut mengeksekusi perintah berikutnya
echo Menyalakan server Flask...
start "" python run.py

:: 4. Beri jeda 3 detik agar Flask benar-benar siap
timeout /t 3 /nobreak >nul

:: 5. Buka browser setelah server dipastikan naik
echo Membuka browser...
start http://127.0.0.1:5000
exit

:error
pause
