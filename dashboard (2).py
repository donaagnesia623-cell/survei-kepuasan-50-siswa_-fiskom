import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Dashboard Analisis", layout="wide")
st.title("📊 DASHBOARD ANALISIS 20 SOAL")
st.markdown("---")

# Baca data
try:
    data = pd.read_excel('data_bersih.xlsx')
    st.success("✅ Data berhasil dimuat!")
except:
    st.error("❌ File data_bersih.xlsx tidak ditemukan")
    st.stop()

# Tampilkan data
with st.expander("📋 LIHAT DATA"):
    st.dataframe(data)

st.divider()

# STATISTIK
st.header("📊 STATISTIK DESKRIPTIF")

mean_scores = data.mean()
stats_df = pd.DataFrame({
    'Soal': [f'Soal {i+1}' for i in range(20)],
    'Rata-rata': mean_scores.values.round(2)
})

st.dataframe(stats_df)

st.divider()

# SOAL TERBAIK & TERBURUK
st.header("🏆 SOAL TERBAIK & TERBURUK")

# Urutkan
nilai_list = [(mean_scores.iloc[i], i) for i in range(20)]
nilai_list.sort(reverse=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("5 Soal Terbaik")
    for i in range(5):
        val, idx = nilai_list[i]
        st.write(f"{i+1}. Soal {idx+1}: {val:.2f}")

with col2:
    st.subheader("5 Soal Terburuk")
    for i in range(5):
        val, idx = nilai_list[-(i+1)]
        st.write(f"{i+1}. Soal {idx+1}: {val:.2f}")

st.divider()

# KESIMPULAN
st.header("📌 KESIMPULAN")

best_val, best_idx = nilai_list[0]
worst_val, worst_idx = nilai_list[-1]

col1, col2, col3 = st.columns(3)
with col1:
    st.success(f"Soal Terbaik: Soal {best_idx+1} ({best_val:.2f})")
with col2:
    st.error(f"Soal Terburuk: Soal {worst_idx+1} ({worst_val:.2f})")
with col3:
    st.info(f"Rata-rata Total: {data.mean().mean():.2f}")

st.success("✅ SELESAI!")
