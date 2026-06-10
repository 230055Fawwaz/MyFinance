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

:: 4. Jalankan Flask di window terpisah secara langsung!
echo Menyalakan server Flask...
start "Flask Server - Tutup jendela ini untuk mematikan server" /MIN cmd /k "python run.py"

:: 5. Jalankan backup database dan pembersihan retensi di background (paralel)
echo Menjalankan backup database di background...
start /b powershell -Command "$db = 'myfinance.db'; $dir = 'backups'; if (-not (Test-Path $dir)) { New-Item -ItemType Directory $dir | Out-Null }; if (Test-Path $db) { $dt = (Get-Date).ToString('yyyyMMdd_HHmm'); Copy-Item $db -Destination \"$dir\backup_$dt.db\" -Force }; $files = Get-ChildItem \"$dir\*.db\" | Sort-Object LastWriteTime -Descending; if ($files.Count -gt 10) { $files | Select-Object -Skip 10 | Where-Object { (Get-Date) - $_.LastWriteTime -gt (New-TimeSpan -Days 30) } | Remove-Item -Force }" >nul 2>&1

:: 6. Tunggu Flask siap dengan polling cepat (tanpa delay di awal)
echo Menunggu Flask siap...
:tunggu
curl -s http://127.0.0.1:5000 >nul 2>&1
if errorlevel 1 (
    timeout /t 1 /nobreak >nul
    goto tunggu
)

:: 7. Buka browser
:buka_browser
echo Membuka browser...
start http://127.0.0.1:5000

:akhir
exit
