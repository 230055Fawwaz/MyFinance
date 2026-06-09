REM ==========================================
REM Nama File: run_server.bat
REM Deskripsi: Otomatisasi dalam menyalakan server flask
REM Penulis:   Fawwaz Yaqzhan
REM Tanggal:   02-04-2026
REM Catatan:
REM   - Menjalankan server Flask
REM   - Membuka browser
REM   - Error handling untuk mengecek environment virtual
REM   - Backup database setiap kali flask berjalan
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

:: ====================================================================
:: TAMBAHAN: OTOMATISASI BACKUP SQLITE
:: ====================================================================
echo Menjalankan backup database...

:: Tentukan folder penyimpanan backup (sesuaikan jika letak DB kamu berbeda)
set "DB_SOURCE=myfinance.db"
set "BACKUP_DIR=backups"

:: Buat folder backup jika belum ada
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

:: Ambil tanggal dan waktu saat ini (Format independen regional setting)
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set "dt=%%I"
set "YYYY=%dt:~0,4%"
set "MM=%dt:~4,2%"
set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%"
set "Min=%dt:~10,2%"

set "BACKUP_FILE=%BACKUP_DIR%\backup_%YYYY%%MM%%DD%_%HH%%Min%.db"

:: Eksekusi penyalinan file DB jika file sumber ditemukan
if exist "%DB_SOURCE%" (
    copy "%DB_SOURCE%" "%BACKUP_FILE%" >nul
    echo [SUKSES] Backup disimpan ke: %BACKUP_FILE%
) else (
    echo [INFO] Database asal belum terbentuk. Backup dilewati untuk sesi ini.
)
echo --------------------------------------------------------------------

:: ====================================================================
:: PEMBERSIHAN OTOMATIS (RETENSI DATA)
:: ====================================================================
echo Memeriksa retensi file backup...

:: Memanggil PowerShell SATU KALI untuk mengurutkan, melewati 10 terbaru, dan menghapus yang >30 hari
powershell -NoProfile -Command "$limitDate = (Get-Date).AddDays(-30); Get-ChildItem -Path '%BACKUP_DIR%' -Filter '*.db' -File | Sort-Object LastWriteTime -Descending | Select-Object -Skip 10 | Where-Object { $_.LastWriteTime -lt $limitDate } | ForEach-Object { Remove-Item -LiteralPath $_.FullName -Force; Write-Host ('Menghapus backup lama: ' + $_.Name) }"

echo --------------------------------------------------------------------
:: ====================================================================

:: 4. Jalankan Flask di window terpisah yang BISA DITUTUP MANUAL
echo Menyalakan server Flask...
start "Flask Server - Tutup jendela ini untuk mematikan server" /MIN cmd /k "python run.py"

:: 5. Tunggu Flask siap dengan polling
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
