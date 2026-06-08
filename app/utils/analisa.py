# ==========================================
# Nama File: analisis.py
# Deskripsi: Logika analisis DSS dan Data Mining
# Penulis:   Fawwaz Yaqzhan
# Tanggal:   08-06-2026
# Catatan:
#   - Fungsi deteksi anomali (Z-score)
#   - Forecasting/Prediksi tren sederhana
#   - Forecasting/Prediksi time series
#   - Analisis hubungan kategori
# ==========================================

import os
import sqlite3
import pandas as pd
import numpy as np

# Impor untuk Data Mining & DSS
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA
from mlxtend.frequent_patterns import apriori, association_rules

# Hasilnya: /root/database.db
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, 'myfinance.db')

def get_transaction_data():
    """Mengambil data transaksi dari SQLite dan mengubahnya menjadi Pandas DataFrame"""
    conn = sqlite3.connect(DATABASE_PATH)
    
    query = """
        SELECT 
            t.id, 
            t.date, 
            s.nama AS kategori, 
            t.amount, 
            t.note
        FROM transactions t
        JOIN subcategories s ON t.subcategory_id = s.id
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if not df.empty:
        # Menyelaraskan tipe data
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
    return df

# ==========================================
# 1. TEMPAT FUNGSI DSS (RULE-BASED / RASIO)
# ==========================================
def hitung_kesehatan_keuangan():
    df = get_transaction_data()
    # Logika DSS kamu akan ditulis di sini
    return {}

# ==========================================
# 2. TEMPAT FUNGSI DATA MINING (ANOMALI)
# ==========================================
def deteksi_anomali_pengeluaran(query_result):
    """
    Menerima data transaksi hasil query Flask-SQLAlchemy,
    mengubahnya menjadi DataFrame, dan mendeteksi anomali.
    """
    # Mengubah list of object SQLAlchemy menjadi list of dictionary
    data = []
    for t in query_result:
        data.append({
            'id': t.id,
            'date': t.date,
            'kategori': t.subcategory.nama if t.subcategory else '-',
            'amount': float(t.amount),
            'note': t.note
        })
    
    df = pd.DataFrame(data)
    
    # Jika data pengeluaran kurang dari 5, batalkan deteksi
    if df.empty or len(df) < 5:
        return []
    
    # Deteksi menggunakan Isolation Forest
    X = df['amount'].values.reshape(-1, 1)
    model = IsolationForest(contamination=0.05, random_state=42)
    df['is_anomali'] = model.fit_predict(X)
    
    # Filter data yang dianggap anomali (-1)
    anomali_df = df[df['is_anomali'] == -1]
    anomali_df = anomali_df.sort_values(by='date', ascending=False)
    
    # Format tanggal ke string agar rapi di frontend
    anomali_df['date'] = anomali_df['date'].dt.strftime('%Y-%m-%d')
    
    return anomali_df.to_dict(orient='records')

# ==========================================
# 3. TEMPAT FUNGSI DATA MINING (PREDIKSI)
# ==========================================
def prediksi_pengeluaran_depan():
    df = get_transaction_data()
    # Logika ARIMA / Regression akan ditulis di sini
    return {}

