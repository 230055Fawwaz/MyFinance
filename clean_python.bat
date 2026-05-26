REM ==========================================
REM Nama File: clean_python.bat
REM Deskripsi: Otomatisasi dalam membersihkan kode Python
REM Penulis:   Fawwaz Yaqzhan
REM Tanggal:   26-05-2026
REM Catatan:
REM   - Dilakukan dengan 4 library python; vulture; black; flake8; pylint
REM ==========================================

@echo off
cls
set REPORT_FILE=laporan_pembersihan.txt

echo =================================================== > %REPORT_FILE%
echo   LAPORAN PEMBERSIHAN KODE PYTHON - %DATE% %TIME%     >> %REPORT_FILE%
echo =================================================== >> %REPORT_FILE%
echo. >> %REPORT_FILE%

echo ===================================================
echo   MEMULAI PROSES PEMBERSIHAN KODE PYTHON (FLASK)   
echo ===================================================

echo.
echo [1/4] Menginstal/Memperbarui Tools PIP...
pip install --quiet vulture black flake8 pylint

echo.
echo [2/4] Menjalankan VULTURE (Mencari kode mati)...
echo --- HASIL VULTURE (KODE MATI) --- >> %REPORT_FILE%
vulture run.py app/ >> %REPORT_FILE% 2>&1
echo * Selesai. Hasil dicatat ke laporan.

echo.
echo [3/4] Menjalankan BLACK (Format kode otomatis)...
echo --- HASIL BLACK (FORMAT OTOMATIS) --- >> %REPORT_FILE%
black run.py app/ >> %REPORT_FILE% 2>&1
echo * Selesai. Kode Anda sudah dirapikan otomatis.

echo.
echo [4/4] Menjalankan FLAKE8 & PYLINT (Analisis Kode)...
echo. >> %REPORT_FILE%
echo --- HASIL FLAKE8 --- >> %REPORT_FILE%
flake8 run.py app/ --ignore=E501 >> %REPORT_FILE% 2>&1

echo. >> %REPORT_FILE%
echo --- HASIL PYLINT --- >> %REPORT_FILE%
pylint run.py app/ --disable=C0114,C0115,C0116 >> %REPORT_FILE% 2>&1
echo * Selesai. Analisis mendalam telah dicatat.

echo.
echo ===================================================
echo   PROSES SELESAI! 
echo   Silakan buka file: %REPORT_FILE%
echo ===================================================
pause
