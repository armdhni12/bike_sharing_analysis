from PIL import Image
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st 
day_df = pd.read_csv("day.csv")
day_df.head()

# Menghapus kolom yang tidak diperlukan
drop_col = ['windspeed']

for i in day_df.columns:
  if i in drop_col:
    day_df.drop(labels=i, axis=1, inplace=True)
day_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_cond',
    'cnt': 'count'
}, inplace=True)
day_df['season'] = day_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
day_df['weather_cond']=day_df['weather_cond'].map({
   1:'Clear',2:'Misty',3:'Light Snow',4:'Severe Weather'
})
def create_season_rent_df(df):
    season_rent_df = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_rent_df
# Menyiapkan weather_rent_df
def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by='weather_cond').agg({
        'count': 'sum'
    })
    return weather_rent_df 

# Membuat komponen filter
min_date = pd.to_datetime(day_df['dateday']).dt.date.min()
max_date = pd.to_datetime(day_df['dateday']).dt.date.max()


with st.sidebar:
    image=Image.open('Dashboard/bike.jpg')
    st.image(image)
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df['dateday'] >= str(start_date)) & 
                (day_df['dateday'] <= str(end_date))]

main_df = day_df[(day_df['dateday'] >= str(start_date)) & 
                (day_df['dateday'] <= str(end_date))]
weather_rent_df = create_weather_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)

#Header
st.header('Pengembangan Dashboard Penyewaan Sepeda')

# Membuah jumlah penyewaan berdasarkan kondisi cuaca
st.subheader('Jumlah Penyewaan Berdasarkan Cuaca')
st.subheader('Weatherly Rentals')

#membuat barplot berdasarkan jumlah penyewaan berdasarkan kondisi cuaca
fig, ax = plt.subplots(figsize=(16, 8))

colors=["tab:blue", "tab:orange", "tab:green"]

sns.barplot(
    x=weather_rent_df.index,
    y=weather_rent_df['count'],
    palette=colors,
    ax=ax
)

for index, row in enumerate(weather_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

# Membuah jumlah penyewaan berdasarkan musim
st.subheader('Jumlah Penyewaan Berdasarkan Musim')
st.subheader('Seasonly Rentals')

#membuat plot berdasarkan jumlah penyewaan berdasarkan musim
fig,ax= plt.subplots(figsize=(16,8))
sns.barplot(
    x='season',
    y='registered',
    data=season_rent_df,
    label='Registered',
    color='yellow',
    ax=ax
)
sns.barplot(
    x='season',
    y='casual',
    data=season_rent_df,
    label='Casual',
    color='red',
    ax=ax
)
for index, row in season_rent_df.iterrows():
    ax.text(index, row['registered'], str(row['registered']), ha='center', va='bottom', fontsize=12)
    ax.text(index, row['casual'], str(row['casual']), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
ax.legend()
st.pyplot(fig)


# try:
#     image=Image.open(r'D:\proyek_analisis_data\bike.jpg')

# except Exception as e:
#     print(f"Error: {e}")
