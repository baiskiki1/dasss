import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi layout dashboard
st.set_page_config(layout="wide")
st.title("🚲 Dashboard Analisis Peminjaman Sepeda")

# Load data harian dengan cache
@st.cache_data
def load_daily_data():
    return pd.read_csv("main_data.csv")

df_day = load_daily_data()

# Validasi kolom yang dibutuhkan
required_cols = ['dteday', 'season', 'weathersit', 'cnt', 'workingday']
if not all(col in df_day.columns for col in required_cols):
    st.error("Beberapa kolom penting tidak ditemukan dalam data.")
    st.stop()

# Konversi tanggal dan tambahkan label musiman/cuaca
df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_day['season_label'] = df_day['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
df_day['weather_label'] = df_day['weathersit'].map({
    1: 'Cerah/Berawan',
    2: 'Kabut/Cloudy',
    3: 'Hujan Ringan/Salju Ringan',
    4: 'Hujan Lebat/Snow+Fog'
})

# Tampilkan data mentah
with st.expander("📄 Lihat 5 Baris Pertama Data"):
    st.write(df_day.head())

# 1. Distribusi Jumlah Peminjaman
st.subheader("1. Distribusi Jumlah Peminjaman Harian")
fig1, ax1 = plt.subplots()
sns.histplot(df_day['cnt'], kde=True, bins=30, color='skyblue', ax=ax1)
ax1.set_title("Distribusi Jumlah Peminjaman Sepeda Harian")
ax1.set_xlabel("Jumlah Peminjaman")
ax1.set_ylabel("Frekuensi")
st.pyplot(fig1)

# 2. Korelasi antar fitur numerik
st.subheader("2. Korelasi antar Fitur Numerik")
numeric_features = ['temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt']
fig2, ax2 = plt.subplots()
sns.heatmap(df_day[numeric_features].corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax2)
st.pyplot(fig2)

# 3. Rata-rata peminjaman per musim
st.subheader("3. Rata-rata Peminjaman Sepeda per Musim")
fig3, ax3 = plt.subplots()
sns.barplot(x='season_label', y='cnt', data=df_day, palette='coolwarm', ax=ax3)
ax3.set_ylabel("Rata-rata Jumlah Peminjaman")
ax3.set_xlabel("Musim")
st.pyplot(fig3)

# 4. Hari kerja vs libur
st.subheader("4. Distribusi Peminjaman: Hari Kerja vs Libur")
fig4, ax4 = plt.subplots()
sns.boxplot(x='workingday', y='cnt', data=df_day, palette='pastel', ax=ax4)
ax4.set_xticklabels(["Libur", "Hari Kerja"])
ax4.set_xlabel("Jenis Hari")
ax4.set_ylabel("Jumlah Peminjaman")
st.pyplot(fig4)

# 5. Tren peminjaman sepanjang waktu
st.subheader("5. Tren Peminjaman Sepanjang Waktu")
fig5, ax5 = plt.subplots()
ax5.plot(df_day['dteday'], df_day['cnt'], color='green')
ax5.set_xlabel("Tanggal")
ax5.set_ylabel("Jumlah Peminjaman")
ax5.set_title("Tren Peminjaman Harian")
st.pyplot(fig5)

# 6. Distribusi berdasarkan cuaca
st.subheader("6. Distribusi Peminjaman Berdasarkan Cuaca")
fig6, ax6 = plt.subplots()
sns.boxplot(x='weather_label', y='cnt', data=df_day, palette='Set2', ax=ax6)
ax6.set_xlabel("Kondisi Cuaca")
ax6.set_ylabel("Jumlah Peminjaman")
ax6.set_xticklabels(ax6.get_xticklabels(), rotation=15)
st.pyplot(fig6)

# 7. Rata-rata peminjaman per jam
st.subheader("7. Rata-rata Jumlah Peminjaman Sepeda per Jam")
try:
    df_hour = pd.read_csv("hour.csv")
    if 'hr' in df_hour.columns and 'cnt' in df_hour.columns:
        hourly_avg = df_hour.groupby('hr')['cnt'].mean()
        fig7, ax7 = plt.subplots()
        sns.lineplot(x=hourly_avg.index, y=hourly_avg.values, marker='o', ax=ax7)
        ax7.set_xlabel("Jam")
        ax7.set_ylabel("Rata-rata Peminjaman")
        ax7.set_xticks(range(0, 24))
        ax7.set_title("Rata-rata Jumlah Peminjaman per Jam")
        st.pyplot(fig7)
    else:
        st.warning("Kolom 'hr' atau 'cnt' tidak ditemukan di hour.csv.")
except FileNotFoundError:
    st.warning("Data per jam (hour.csv) tidak ditemukan.")
except Exception as e:
    st.error(f"Terjadi kesalahan saat memproses data per jam: {e}")

# Footer
st.markdown("---")
st.markdown("📊 Dashboard dibuat oleh **Muhammad Bais Al Hakiki** — Tugas Akhir Analisis Data Sepeda 🚴")
