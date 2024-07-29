import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
from babel.numbers import format_currency

sns.set(style='dark')

def load_day():
    read_day = pd.read_csv('day.csv')
    return read_day

def load_hour():
    read_hour = pd.read_csv('hour.csv')
    return read_hour

day_df = load_day()
hour_df = load_hour()

# Merge data
day_hour_df = pd.merge(
    left=hour_df,
    right=day_df,
    how="left",
    left_on="instant",
    right_on="instant"
)

#Sidebar
# Sidebar
with st.sidebar:
        # Pilihan untuk memilih bulan
    selected_month = st.selectbox('Pilih Bulan', ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'])
    st.title('Analyst')
    st.image("img.jpg")
    st.caption('Robertos H Wijaya - Junior Data Analyst')    


# Title
st.title("Bike Sharing Analysisis")
st.write("Dashboard analisis Bike-Sharing")

# Filter data berdasarkan bulan yang dipilih
selected_month_number = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'][['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'].index(selected_month)]
selected_data = day_hour_df[day_hour_df['dteday_x'].str.startswith(f'2011-{selected_month_number}')]

# All Data
st.subheader(f"Total peminjaman di bulan {selected_month}")

daily_data = selected_data.groupby('dteday_x')['cnt_x'].sum()
fig = px.line(x=daily_data.index, y=daily_data.values, labels={'x': 'Date', 'y': 'Total Bike Users'})
st.plotly_chart(fig)


st.subheader("Jumlah peminjaman sepeda berdasarkan Hari kerja dan libur")
grouped = day_df.groupby('workingday').sum()[['casual', 'registered', 'cnt']].reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(x='workingday', y='cnt', data=grouped, palette='viridis')
plt.ylabel('Jumlah Peminjaman')
plt.xticks(ticks=[0, 1], labels=['Hari Libur', 'Hari Kerja'])
plt.tight_layout()
st.pyplot(plt)


#Sorted by season
st.subheader("Jumlah peminjaman sepeda berdasarkan musimmnya")

season_labels = {
    1: 'Spring',
    2: 'Summer',
    3: 'Fall',
    4: 'Winter'
}

day_df['season'] = day_df['season'].map(season_labels)

# Mengelompokkan data berdasarkan musim dan menghitung jumlah peminjaman
grouped_season = day_df.groupby('season').sum()['cnt'].reset_index()

# Membuat bar plot untuk membandingkan jumlah peminjaman pada setiap musim
plt.figure(figsize=(10, 6))
sns.barplot(x='season', y='cnt', data=grouped_season, palette='muted')
plt.xlabel('Musim')
plt.ylabel('Jumlah Peminjaman')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
st.pyplot(plt)


#Sorted casual and register user
st.subheader("Perbandingan rata-rata jumlah peminjaman sepeda antara pengguna casual dan pengguna terdaftar pada setiap hari kerja (Senin-Jumat)")
# Filter data untuk hari kerja (Senin-Jumat)
df_weekdays = day_df[(day_df['weekday'] >= 0) & (day_df['weekday'] <= 4)]

# Hitung rata-rata jumlah peminjaman casual dan registered untuk setiap hari kerja
average_casual = df_weekdays.groupby('weekday')['casual'].mean()
average_registered = df_weekdays.groupby('weekday')['registered'].mean()

# Buat label hari kerja
weekday_labels = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']

# Buat visualisasi
fig, ax = plt.subplots()
ax.plot(weekday_labels, average_casual, label='Casual')
ax.plot(weekday_labels, average_registered, label='Registered')
ax.set_xlabel('Hari Kerja')
ax.set_ylabel('Rata-rata Jumlah Peminjaman')
ax.legend()
st.pyplot(fig)

st.caption('Copyright © Robertos H Wijaya 2023')