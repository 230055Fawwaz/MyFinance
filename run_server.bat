@echo off
:: 1. Masuk ke direktori file .bat berada
cd /d %~dp0

:: 2. Aktifkan virtual environment
call venv\Scripts\activate

:: 3. Tunggu sebentar lalu buka browser ke localhost:5000
:: Perintah 'start' akan membuka browser default Anda
timeout /t 2 /nobreak >nul
start http://127.0.0.1:5000

:: 4. Jalankan server Flask
py run.py

pause
