import streamlit as st
import pandas as pd
import numpy as np
import urllib.request
import plotly.express as px
import json
import plotly.graph_objects as go
import matplotlib
from matplotlib.backends.backend_agg import RendererAgg
import requests
import seaborn as sns
import plotly.express as px


st.set_page_config(layout='wide')

def load_url(url: str):
    r = requests.get(url)
    if r.status_code!=200:
        return None
    return r.json()

@st.cache
def get_data():
    url = 'https://pkgstore.datahub.io/world-bank/sh.tbs.incd/data_json/data/fb5bcc726d6fc91f2d1a0bedf77218ac/data_json.json'
    contents = urllib.request.urlopen(url).read()
    return(contents)

contents = json.loads(get_data())
df = pd.DataFrame(contents)
df['Country Name'] = df['Country Name'].astype('str')
df['Value'] = df['Value'].astype('int')
df = df.iloc[324:]

matplotlib.use('agg')
_lock=RendererAgg.lock

sns.set_style('darkgrid')
row0_space1, row0_1, row0_space2, row0_2, row0_space3 = st.columns(
    (.1, 2, .2, 1, .1)
)

row0_1.title('Analisis Data Jumlah Insiden TBC dalam 100.000 populasi per Tahun')

st.write('')
row1_space1, row1, row1_space2 = st.columns(
    (.1, 1, .1)
)

with row1, _lock:
    st.subheader('Grafik insiden TBC per tahun suatu negara')
    option = st.selectbox(
     'Pilih Negara?', tuple(np.unique(df['Country Name'])))

    start_year, end_year = st.select_slider(
     'Pilih jangka tahun',
     options=np.unique(df['Year']),
     value=(np.unique(df['Year']).min(), np.unique(df['Year']).max()))

    # year_filter = st.select_slider(
    #  'Select a year',
    #  options=df['Year'])

    df_chart = df.copy()
    df_chart = df_chart[df_chart['Country Name']==option]
    df_chart = df_chart[df_chart['Year']>=start_year]
    df_chart = df_chart[df_chart['Year']<=end_year]

    fig = go.Figure(go.Line(
            x=df_chart['Year'],
            y=df_chart['Value'],
            orientation='h'))
    fig.update_layout(height=600)

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df_chart)

    st.subheader('Diagram total populasi TBC di '+str(np.shape(np.unique(df['Country Name']))[0])+' Negara')
    df2 = df.copy()
    df2['Country Name'] = df2['Country Name'].astype('str')
    df2['Value'] = df2['Value'].astype('int')
    df2['total'] = df2.groupby(['Country Code'], as_index=False)['Value'].transform('sum')
    df2 = df2.groupby(['Country Code'], as_index=False).head(1).reset_index(drop=True)
    df2 = df2.drop(['Value', 'Year'], axis=1)

    fig2 = go.Figure(go.Bar(
            x=df2['total'],
            y=df2['Country Name'],
            orientation='h'))
    fig2.update_layout(height=3200)

    st.plotly_chart(fig2, use_container_width=True)

    st.subheader('Tabel 10 Negara dengan Kasus Terbanyak')
    df3 = df.copy()
    df3['Country Name'] = df3['Country Name'].astype('str')
    df3['Value'] = df3['Value'].astype('int')
    df3['total'] = df3.groupby(['Country Code'], as_index=False)['Value'].transform('sum')
    df3 = df3.groupby(['Country Code'], as_index=False).head(1).reset_index(drop=True)
    df3 = df3.drop(['Value', 'Year'], axis=1)
    df3 = df3.sort_values(by=['total'], ascending=False)
    st.dataframe(df3.head(10))

    st.subheader('Pie Chart Pembagian Negara Terbanyak')
    df4 = df3.copy()
    fig = px.pie(df4.head(10), values='total', names='Country Name')
    st.plotly_chart(fig)

    st.subheader('Tabel 10 Negara dengan Kasus Terendah')
    df3 = df.copy()
    df3['Country Name'] = df3['Country Name'].astype('str')
    df3['Value'] = df3['Value'].astype('int')
    df3['total'] = df3.groupby(['Country Code'], as_index=False)['Value'].transform('sum')
    df3 = df3.groupby(['Country Code'], as_index=False).head(1).reset_index(drop=True)
    df3 = df3.drop(['Value', 'Year'], axis=1)
    df3 = df3.sort_values(by=['total'], ascending=False)
    st.dataframe(df3.tail(10))

    st.subheader('Pie Chart Pembagian Negara Terendah')
    df4 = df3.copy()
    fig = px.pie(df4.tail(10), values='total', names='Country Name')
    st.plotly_chart(fig)
    
    st.subheader('Tabel Jumlah Rata-Rata Pertahun')
    df5 = df3.copy()
    df5['total'] = df5['total']/16
    st.dataframe(df5)

