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
def hitung_kesehatan_keuangan(query_result):
    """
    DSS Rule-Based: Menghitung rasio keuangan bulan berjalan
    memanfaatkan Enum type ('income' / 'expense') dari Category.
    """
    now = datetime.now()
    total_pemasukan = 0
    total_pengeluaran = 0
    
    for t in query_result:
        # Filter transaksi bulan dan tahun berjalan
        if t.date.year == now.year and t.date.month == now.month:
            amount = float(t.amount)
            
            # Mengakses tipe kategori melalui relasi: Transaction -> SubCategory -> Category
            if t.subcategory and t.subcategory.category:
                tipe_transaksi = t.subcategory.category.type # nilainya 'income' atau 'expense'
                
                if tipe_transaksi == 'income':
                    total_pemasukan += amount
                elif tipe_transaksi == 'expense':
                    total_pengeluaran += abs(amount)

    # Jika tidak ada transaksi sama sekali bulan ini
    if total_pemasukan == 0 and total_pengeluaran == 0:
        return {
            "status": "Belum ada data",
            "rasio_menabung": 0,
            "skor": "N/A",
            "rekomendasi": "Belum ada transaksi yang tercatat untuk bulan ini.",
            "status_color": "neutral"
        }

    # Jika ada pengeluaran tapi tidak ada pemasukan tercatat
    if total_pemasukan == 0 and total_pengeluaran > 0:
        return {
            "total_pemasukan": 0,
            "total_pengeluaran": total_pengeluaran,
            "rasio_menabung": -100,
            "skor": "WASPADA / BOROS",
            "rekomendasi": "Kamu memiliki pengeluaran tanpa adanya pemasukan yang tercatat bulan ini! Segera input pemasukanmu.",
            "status_color": "danger"
        }

    # Hitung Rasio Menabung Normal
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
def deteksi_anomali_pengeluaran(query_result):
    """
    Data Mining: Mendeteksi anomali khusus pada transaksi bertipe 'expense'.
    """
    data = []
    for t in query_result:
        if t.subcategory and t.subcategory.category:
            if t.subcategory.category.type == 'expense':
                data.append({
                    'id': t.id,
                    'date': t.date,
                    'kategori': t.subcategory.nama, # Menggunakan t.subcategory.nama sesuai model baru
                    'amount': float(t.amount),
                    'note': t.note
                })
    
    if not data or len(data) < 5:
        return []
        
    df = pd.DataFrame(data)
    X = df['amount'].values.reshape(-1, 1)
    
    model = IsolationForest(contamination=0.05, random_state=42)
    df['is_anomali'] = model.fit_predict(X)
    
    anomali_df = df[df['is_anomali'] == -1]
    anomali_df = anomali_df.sort_values(by='date', ascending=False)
    anomali_df['date'] = anomali_df['date'].dt.strftime('%Y-%m-%d')
    
    return anomali_df.to_dict(orient='records')

# ==========================================
# 3. TEMPAT FUNGSI DATA MINING (PREDIKSI)
# ==========================================
def prediksi_pengeluaran_bulan_depan(query_result):
    """
    Data Mining: Memprediksi pengeluaran bulan depan menggunakan Linear Regression
    berdasarkan data historis bulanan bertipe 'expense'.
    """
    data = []
    for t in query_result:
        if t.subcategory and t.subcategory.category:
            if t.subcategory.category.type == 'expense':
                data.append({
                    'period': t.date.strftime('%Y-%m'),
                    'amount': float(t.amount)
                })
            
    if not data:
        return 0
        
    df = pd.DataFrame(data)
    df_bulanan = df.groupby('period')['amount'].sum().reset_index()
    df_bulanan = df_bulanan.sort_values(by='period').reset_index()
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
def analisis_hubungan_kategori(query_result):
    """
    Data Mining: Menggunakan algoritma Apriori untuk menemukan 
    subkategori pengeluaran yang sering muncul bersamaan berdasarkan tanggal transaksi.
    """
    data = []
    for t in query_result:
        if t.subcategory and t.subcategory.category:
            if t.subcategory.category.type == 'expense':
                data.append({
                    'tanggal': t.date.strftime('%Y-%m-%d'),
                    'sub_nama': t.subcategory.nama
                })
                
    if not data or len(data) < 5:
        return []
        
    df = pd.DataFrame(data)
    
    # Membuat matriks transaksi: Baris = Tanggal, Kolom = Nama Subkategori (1 jika dibeli di tanggal itu, 0 jika tidak)
    basket = (df.groupby(['tanggal', 'sub_nama'])['sub_nama']
              .count().unstack().reset_index().fillna(0)
              .set_index('tanggal'))
    
    # Ubah jumlah item menjadi boolean (True/False) sesuai syarat pustaka mlxtend
    basket_sets = basket.map(lambda x: True if x > 0 else False)
    
    try:
        # Cari kombinasi item yang sering muncul (min_support=0.1 artinya minimal muncul di 10% dari total hari transaksi)
        frequent_itemsets = apriori(basket_sets, min_support=0.1, use_colnames=True)
        
        if frequent_itemsets.empty:
            return []
            
        # Bentuk aturan asosiasi
        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)
        
        output = []
        for _, row in rules.head(3).iterrows(): # Ambil top 3 pola terkuat
            item_a = list(row['antecedents'])[0]
            item_b = list(row['consequents'])[0]
            keyakinan = round(row['confidence'] * 100, 1)
            
            output.append({
                "pola": f"Jika kamu mengeluarkan uang untuk '{item_a}', ada kemungkinan {keyakinan}% kamu juga akan mengeluarkan uang untuk '{item_b}' di hari yang sama."
            })
        return output
    except Exception:
        # Mengantisipasi jika variasi data di hari tersebut belum cukup untuk membentuk matriks asosiasi
        return []
    