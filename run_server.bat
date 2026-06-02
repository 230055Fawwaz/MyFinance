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

:: 1. Cek apakah sudah ada instance Flask yang berjalan (hindari duplikasi)
tasklist /FI "IMAGENAME eq python.exe" 2>nul | find /I "python.exe" >nul
if not errorlevel 1 (
    echo [PERINGATAN] Python sudah berjalan. Pastikan tidak ada Flask yang aktif sebelumnya.
    echo Lanjutkan tetap buka browser saja? [Y/N]
    set /p konfirmasi=Pilihan: 
    if /i "%konfirmasi%"=="Y" goto buka_browser
    goto akhir
)

:: 2. Validasi virtual environment
if not exist .venv\Scripts\activate (
    echo [ERROR] Virtual Environment .venv tidak ditemukan!
    pause
    exit /b 1
)

:: 3. Aktifkan venv
call .venv\Scripts\activate

:: 4. Jalankan Flask di window terpisah yang BISA DITUTUP MANUAL
::    /MIN  = minimized agar tidak mengganggu
::    Menutup jendela CMD itu = mematikan Flask sepenuhnya
echo Menyalakan server Flask...
start "Flask Server - Tutup jendela ini untuk mematikan server" /MIN cmd /k "python run.py"

:: 5. Tunggu Flask siap dengan polling (lebih andal dari timeout tetap)
echo Menunggu Flask siap...
:tunggu
timeout /t 1 /nobreak >nul
curl -s http://127.0.0.1:5000 >nul 2>&1
if errorlevel 1 goto tunggu

:: 6. Buka browser
:buka_browser
echo Membuka browser...
start http://127.0.0.1:5000

:akhir
exit
