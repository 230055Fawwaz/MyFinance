@echo off
:: 1. Masuk ke direktori folder proyek Anda
cd /d %~dp0

:: 2. Aktifkan virtual environment
call .venv\Scripts\activate

:: 3. Tunggu sebentar lalu buka browser ke localhost:5000
timeout /t 2 /nobreak >nul
start http://127.0.0.1:5000

:: 4. Jalankan server Flask
python run.py

pause