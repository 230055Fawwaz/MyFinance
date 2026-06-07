REM ==========================================
REM Nama File: backup.bat
REM Deskripsi: Backup manual oleh user
REM Penulis:   Fawwaz Yaqzhan
REM Tanggal:   08-06-2026
REM Catatan:
REM   - User bisa backup database melalui klik tombol
REM ==========================================

:: ====================================================================
:: BACKUP SQLITE (Lokasi: /app/backup.bat)
:: ====================================================================
@echo off

:: Berpindah ke direktori tempat file .bat ini disimpan (/app)
cd /d "%~dp0"

echo Menjalankan backup database...

:: Mundur satu tingkat ke folder luar tempat database berada
set "DB_SOURCE=..\myfinance.db"
set "BACKUP_DIR=..\backups"

:: Buat folder backup di luar jika belum ada
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

:: Ambil tanggal dan waktu saat ini
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
    echo [INFO] Database asal tidak ditemukan di %cd%\%DB_SOURCE%. Backup dilewati.
)
echo --------------------------------------------------------------------
