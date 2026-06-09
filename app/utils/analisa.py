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

import pandas as pd
from datetime import datetime

# Impor untuk Data Mining & DSS
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression
from mlxtend.frequent_patterns import apriori, association_rules

# ==========================================
# 1. TEMPAT FUNGSI DSS (RULE-BASED / RASIO)
# ==========================================
def hitung_kesehatan_keuangan(df):
    """
    DSS Rule-Based: Menghitung rasio keuangan bulan berjalan menggunakan Pandas DataFrame.
    """
    if df.empty:
        return {
            "status": "Belum ada data",
            "rasio_menabung": 0,
            "skor": "N/A",
            "rekomendasi": "Belum ada transaksi yang tercatat untuk bulan ini.",
            "status_color": "neutral"
        }

    now = datetime.now()
    
    # Filter transaksi bulan dan tahun berjalan menggunakan properti .dt Pandas
    df_bulan_ini = df[(df['date'].dt.year == now.year) & (df['date'].dt.month == now.month)]
    
    # Hitung total pemasukan dan pengeluaran tanpa loop
    total_pemasukan = df_bulan_ini[df_bulan_ini['cat_type'] == 'income']['amount'].astype(float).sum()
    total_pengeluaran = df_bulan_ini[df_bulan_ini['cat_type'] == 'expense']['amount'].astype(float).abs().sum()

    if total_pemasukan == 0 and total_pengeluaran == 0:
        return {
            "status": "Belum ada data",
            "rasio_menabung": 0,
            "skor": "N/A",
            "rekomendasi": "Belum ada transaksi yang tercatat untuk bulan ini.",
            "status_color": "neutral"
        }

    if total_pemasukan == 0 and total_pengeluaran > 0:
        return {
            "total_pemasukan": 0,
            "total_pengeluaran": total_pengeluaran,
            "rasio_menabung": -100,
            "skor": "WASPADA / BOROS",
            "rekomendasi": "Kamu memiliki pengeluaran tanpa adanya pemasukan yang tercatat bulan ini! Segera input pemasukanmu.",
            "status_color": "danger"
        }

    uang_tersisa = total_pemasukan - total_pengeluaran
    rasio_menabung = (uang_tersisa / total_pemasukan) * 100
    
    if rasio_menabung >= 30:
        skor = "SANGAT SEHAT"
        rekomendasi = "Luar biasa! Alokasi tabunganmu di atas 30%. Kamu punya ruang aman untuk investasi atau dana darurat."
        status_color = "success"
    elif 10 <= rasio_menabung < 30:
        skor = "AMAN"
        rekomendasi = "Kondisi keuangan stabil. Usahakan untuk menekan sedikit pengeluaran impulsif agar rasio menabung menyentuh angka ideal."
        status_color = "warning"
    else:
        skor = "WASPADA / BOROS"
        rekomendasi = "Pengeluaranmu hampir habis atau melebihi pemasukan bulan ini! Segera tinjau ulang histori transaksimu."
        status_color = "danger"

    return {
        "total_pemasukan": total_pemasukan,
        "total_pengeluaran": total_pengeluaran,
        "rasio_menabung": round(rasio_menabung, 1),
        "skor": skor,
        "rekomendasi": rekomendasi,
        "status_color": status_color
    }

# ==========================================
# 2. TEMPAT FUNGSI DATA MINING (ANOMALI)
# ==========================================
def deteksi_anomali_pengeluaran(df):
    """
    Data Mining: Mendeteksi anomali khusus pada transaksi bertipe 'expense'.
    """
    if df.empty:
        return []
        
    # Filter khusus expense
    df_expense = df[df['cat_type'] == 'expense'].copy()
    
    if len(df_expense) < 5:
        return []
        
    X = df_expense['amount'].astype(float).values.reshape(-1, 1)
    
    model = IsolationForest(contamination=0.05, random_state=42)
    df_expense['is_anomali'] = model.fit_predict(X)
    
    anomali_df = df_expense[df_expense['is_anomali'] == -1].copy()
    anomali_df = anomali_df.sort_values(by='date', ascending=False)
    anomali_df['date'] = anomali_df['date'].dt.strftime('%Y-%m-%d')
    
    # Rename kolom sub_nama kembali menjadi 'kategori' agar sesuai dengan struktur HTML/Template
    anomali_df = anomali_df.rename(columns={'sub_nama': 'kategori'})
    
    return anomali_df[['id', 'date', 'kategori', 'amount', 'note']].to_dict(orient='records')

# ==========================================
# 3. TEMPAT FUNGSI DATA MINING (PREDIKSI)
# ==========================================
def prediksi_pengeluaran_bulan_depan(df):
    """
    Data Mining: Memprediksi pengeluaran bulan depan menggunakan Linear Regression.
    """
    if df.empty:
        return 0
        
    df_expense = df[df['cat_type'] == 'expense'].copy()
    if df_expense.empty:
        return 0
        
    df_expense['period'] = df_expense['date'].dt.strftime('%Y-%m')
    df_expense['amount'] = df_expense['amount'].astype(float)
    
    df_bulanan = df_expense.groupby('period')['amount'].sum().reset_index()
    df_bulanan = df_bulanan.sort_values(by='period').reset_index(drop=True)
    df_bulanan['bulan_ke'] = df_bulanan.index
    
    if len(df_bulanan) < 2:
        return round(df_bulanan['amount'].iloc[0], 2) if not df_bulanan.empty else 0
        
    X = df_bulanan['bulan_ke'].values.reshape(-1, 1)
    y = df_bulanan['amount'].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    indeks_bulan_depan = len(df_bulanan)
    prediksi_y = model.predict([[indeks_bulan_depan]])
    
    return round(max(0, prediksi_y[0]), 0)

# ==========================================
# 4. Analisis Hubungan Kategori
# ==========================================
def analisis_hubungan_kategori(df):
    """
    Data Mining: Menggunakan algoritma Apriori untuk pola hubungan subkategori.
    """
    if df.empty:
        return []
        
    df_expense = df[df['cat_type'] == 'expense'].copy()
    if len(df_expense) < 5:
        return []
        
    df_expense['tanggal'] = df_expense['date'].dt.strftime('%Y-%m-%d')
    
    # Membuat matriks transaksi
    basket = (df_expense.groupby(['tanggal', 'sub_nama'])['sub_nama']
              .count().unstack().reset_index().fillna(0)
              .set_index('tanggal'))
    
    basket_sets = basket.map(lambda x: True if x > 0 else False)
    
    try:
        frequent_itemsets = apriori(basket_sets, min_support=0.1, use_colnames=True)
        
        if frequent_itemsets.empty:
            return []
            
        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)
        
        output = []
        for _, row in rules.head(3).iterrows():
            item_a = list(row['antecedents'])[0]
            item_b = list(row['consequents'])[0]
            keyakinan = round(row['confidence'] * 100, 1)
            
            output.append({
                "pola": f"Jika kamu mengeluarkan uang untuk '{item_a}', ada kemungkinan {keyakinan}% kamu juga akan mengeluarkan uang untuk '{item_b}' di hari yang sama."
            })
        return output
    except Exception:
        return []
    