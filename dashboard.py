import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Dashboard Analisis 20 Soal", layout="wide")
st.title("📊 DASHBOARD ANALISIS 20 SOAL")
st.markdown("### Tugas Mata Kuliah Fisika Komputasi")
st.markdown("---")

# Baca data bersih
data = pd.read_excel('data_bersih.xlsx')
st.success(f"✅ Data siap! {len(data)} responden, {len(data.columns)} soal")

with st.expander("📋 LIHAT DATA (50 Responden x 20 Soal)"):
    st.dataframe(data, use_container_width=True)

st.divider()

# ==========================================================
# 1️⃣ STATISTIK DESKRIPTIF
# ==========================================================
st.header("1️⃣ STATISTIK DESKRIPTIF")

mean_scores = data.mean()
median_scores = data.median()
std_scores = data.std()

# Buat tabel statistik
stats_df = pd.DataFrame({
    'Soal': [f'Soal {i+1}' for i in range(20)],
    'Rata-rata': mean_scores.values.round(2),
    'Median': median_scores.values.round(2),
    'Std Dev': std_scores.values.round(2)
})

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Tabel Statistik")
    st.dataframe(stats_df, use_container_width=True, height=450)

with col2:
    st.subheader("📈 Grafik Rata-rata")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(range(1, 21), mean_scores.values, color='steelblue')
    ax.set_xlabel('Nomor Soal')
    ax.set_ylabel('Rata-rata Skor')
    ax.set_ylim(0, 4)
    ax.set_xticks(range(1, 21))
    ax.axhline(y=mean_scores.mean(), color='red', linestyle='--', 
               label=f'Total: {mean_scores.mean():.2f}')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    for bar, val in zip(bars, mean_scores.values):
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.1,
                f'{val:.2f}', ha='center', va='bottom', fontsize=8)
    
    st.pyplot(fig)

st.divider()

# ==========================================================
# 2️⃣ ANALISIS PER SOAL
# ==========================================================
st.header("2️⃣ ANALISIS PER SOAL")

soal_list = [f'Soal {i+1}' for i in range(20)]
pilihan = st.selectbox("Pilih Soal:", soal_list)
nomor = int(pilihan.split()[1]) - 1
kolom = data.iloc[:, nomor]

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Distribusi Skor")
    
    # Hitung frekuensi
    freq = {1:0, 2:0, 3:0, 4:0}
    for val in kolom:
        skor = int(round(val))
        if skor in freq:
            freq[skor] += 1
    
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(freq.keys(), freq.values(), 
                  color=['red', 'orange', 'lightblue', 'green'])
    ax.set_xlabel('Skor')
    ax.set_ylabel('Jumlah')
    ax.set_xticks([1, 2, 3, 4])
    
    for bar, (skor, jml) in zip(bars, freq.items()):
        ax.text(bar.get_x() + bar.get_width()/2, jml + 1,
                str(jml), ha='center', va='bottom')
    
    st.pyplot(fig)

with col2:
    st.subheader("Statistik")
    st.write(f"**Rata-rata:** {kolom.mean():.2f}")
    st.write(f"**Median:** {kolom.median():.2f}")
    st.write(f"**Std Deviasi:** {kolom.std():.2f}")
    st.write(f"**Minimum:** {kolom.min():.1f}")
    st.write(f"**Maximum:** {kolom.max():.1f}")

st.divider()

# ==========================================================
# 3️⃣ SOAL TERBAIK & TERBURUK
# ==========================================================
st.header("3️⃣ SOAL TERBAIK & TERBURUK")

# Urutkan nilai
nilai = mean_scores.values
indices = list(range(20))
pairs = list(zip(nilai, indices))
pairs.sort(reverse=True)

# Ambil 5 terbaik
top5_val = [pairs[i][0] for i in range(5)]
top5_idx = [pairs[i][1] for i in range(5)]
top5_nama = [f'Soal {idx+1}' for idx in top5_idx]

# Ambil 5 terburuk
bottom5_val = [pairs[-(i+1)][0] for i in range(5)]
bottom5_idx = [pairs[-(i+1)][1] for i in range(5)]
bottom5_nama = [f'Soal {idx+1}' for idx in bottom5_idx]

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 5 Soal Terbaik")
    
    fig, ax = plt.subplots(figsize=(8, 4))
    y_pos = range(5)
    bars = ax.barh(y_pos, top5_val, color='green')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(top5_nama)
    ax.set_xlabel('Rata-rata')
    ax.set_xlim(0, 4)
    
    for bar, val in zip(bars, top5_val):
        ax.text(val + 0.1, bar.get_y() + bar.get_height()/2,
                f'{val:.2f}', va='center')
    
    st.pyplot(fig)

with col2:
    st.subheader("📉 5 Soal Terburuk")
    
    fig, ax = plt.subplots(figsize=(8, 4))
    y_pos = range(5)
    bars = ax.barh(y_pos, bottom5_val, color='red')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(bottom5_nama)
    ax.set_xlabel('Rata-rata')
    ax.set_xlim(0, 4)
    
    for bar, val in zip(bars, bottom5_val):
        ax.text(val + 0.1, bar.get_y() + bar.get_height()/2,
                f'{val:.2f}', va='center')
    
    st.pyplot(fig)

st.divider()

# ==========================================================
# 4️⃣ ANALISIS GAP
# ==========================================================
st.header("4️⃣ ANALISIS GAP")

gap = [4 - v for v in nilai]

# Buat dataframe gap
gap_data = []
for i in range(20):
    gap_data.append({
        'Soal': f'Soal {i+1}',
        'Gap': round(gap[i], 2)
    })
gap_df = pd.DataFrame(gap_data)
gap_df = gap_df.sort_values('Gap', ascending=False)

col1, col2 = st.columns([2, 1])

with col1:
    fig, ax = plt.subplots(figsize=(12, 5))
    
    # Warna berdasarkan nilai gap
    colors = []
    for g in gap:
        if g > 1.5:
            colors.append('red')
        elif g > 1:
            colors.append('orange')
        else:
            colors.append('green')
    
    ax.bar(range(1, 21), gap, color=colors)
    ax.set_xlabel('Nomor Soal')
    ax.set_ylabel('Gap (4 - rata-rata)')
    ax.set_xticks(range(1, 21))
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)

with col2:
    st.subheader("🎯 Prioritas")
    st.dataframe(gap_df.head(5))
    st.warning(f"**Fokus:** {gap_df.iloc[0]['Soal']}")

st.divider()

# ==========================================================
# 5️⃣ SEGMENTASI SISWA
# ==========================================================
st.header("5️⃣ SEGMENTASI SISWA")

n_clusters = st.slider("Jumlah Kelompok:", 2, 4, 3)

# Standardisasi
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# K-Means
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
clusters = kmeans.fit_predict(data_scaled)

# Tambah cluster
data_cluster = data.copy()
data_cluster['Cluster'] = clusters

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Profil per Kelompok")
    profile = data_cluster.groupby('Cluster').mean()
    # Ganti nama kolom
    new_cols = [f'Soal {i+1}' for i in range(20)]
    profile.columns = new_cols
    st.dataframe(profile.round(2))

with col2:
    st.subheader("📈 Distribusi")
    jumlah = data_cluster['Cluster'].value_counts().sort_index()
    
    labels = [f'Kelompok {i+1}' for i in range(len(jumlah))]
    
    fig, ax = plt.subplots()
    ax.pie(jumlah.values, labels=labels, autopct='%1.1f%%')
    st.pyplot(fig)

st.divider()

# ==========================================================
# 6️⃣ KESIMPULAN
# ==========================================================
st.header("6️⃣ KESIMPULAN")

col1, col2, col3 = st.columns(3)

with col1:
    st.success(f"**Soal Terbaik:** {top5_nama[0]} ({top5_val[0]:.2f})")

with col2:
    st.error(f"**Soal Terburuk:** {bottom5_nama[0]} ({bottom5_val[0]:.2f})")

with col3:
    st.info(f"**Rata-rata Total:** {mean_scores.mean():.2f}/4.00")

st.markdown("---")
st.subheader("📋 REKOMENDASI:")

for i in range(3):
    st.write(f"{i+1}. **{bottom5_nama[i]}** (rata-rata: {bottom5_val[i]:.2f}) - Perlu ditingkatkan")

st.success("✅ ANALISIS SELESAI!")
