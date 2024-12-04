import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')

st.title(':orange[STATISTIK] :blue[DAERAH] :green[KABUPATEN SUBANG]')
#st.subheader('BANDUNG KOTA :orange[dalam] :green[GRAFIK] :orange[dan] :blue[INDIKATOR]', divider='rainbow')
st.subheader('', divider='rainbow')

with st.expander('PENGANTAR'):
    st.success('Aplikasi ini berisi kumpulan Indikator Makro yang resmi dirilis oleh Badan Pusat Statistik, \
        ditambah data-data lain yang sumber resminya tercantum.')
    st.info('Aplikasi ini dibuat untuk memudahkan Para Pemangku Kepentingan dalam proses Perencanaan, Pelaksanaan, \
        Monitoring dan Evaluasi Pembangunan di Kabupaten Subang.')
    st.warning('Silakan mengakses setiap indikator makro melalui menu di sebelah kiri.')

st.subheader('', divider='green')

kol1, kol2, kol3, kol4 = st.columns(4)
with kol1:
    with st.container(border=True):
        with st.container(border=True):
            st.subheader(':green[Luas Wilayah (Km2)]')
            st.header(':green[2.165,55]')

with kol2:
    with st.container(border=True):
        with st.container(border=True):
            st.subheader(':blue[Jumlah Kecamatan]')
            st.header(':blue[30]')

with kol3:
    with st.container(border=True):
        with st.container(border=True):
            st.subheader(':orange[Jumlah Kelurahan]')
            st.header(':orange[8]')

with kol4:
    with st.container(border=True):
        with st.container(border=True):
            st.subheader(':blue[Jumlah Desa]')
            st.header(':blue[245]')

            
with st.expander('Catatan'):
    st.caption('Berdasarkan Keputusan Menteri Dalam Negeri No. 050-145 Tahun 2022')

st.subheader('', divider='green')

# LUAS KECAMATAN
with st.expander('Luas Kecamatan'):
    with st.container(border=True):
        st.subheader('Luas Kabupaten Subang menurut Kecamatan (Km2)')

        # URL luas wilayah
        url = "https://data.jabarprov.go.id/api-backend//bigdata/dpmdes/idm_luas_wilayah_desa__des_kel?limit=1000&skip=0&where=%7B%22bps_nama_kabupaten_kota%22%3A%5B%22KABUPATEN+SUBANG%22%5D%2C%22tahun%22%3A%5B%222020%22%5D%7D"

        response = requests.get(url)
        data = response.json()
        
        # Mengubah data yang sudah difilter menjadi pandas dataframe
        df = pd.DataFrame(data['data'])
        
        df = df.rename(columns={'luas_wilayah_desa':'luas_wilayah'})
        
        df_luas = df.groupby(['bps_nama_kabupaten_kota', 'kemendagri_nama_kecamatan'])['luas_wilayah'].sum().reset_index()

        trimep = px.treemap(df_luas, path=['bps_nama_kabupaten_kota', 'kemendagri_nama_kecamatan'],
                            values='luas_wilayah')

        paycart = px.pie(df_luas, values='luas_wilayah', color='kemendagri_nama_kecamatan',
                        names='kemendagri_nama_kecamatan')

        kol6, kol7 = st.columns(2)
        with kol6:
            st.plotly_chart(trimep, use_container_width=True)

        with kol7:
            st.plotly_chart(paycart, use_container_width=True)

# Menampilkan dataframe
with st.expander('Lihat Tabel'):
    st.dataframe(df_luas, use_container_width=True, hide_index=True)
    st.caption('Sumber: https://opendata.jabarprov.go.id/id/dataset/luas-wilayah-desa-berdasarkan-desakelurahan-di-jawa-barat')

st.subheader('', divider='green')

with st.expander('Luas Desa'):
    with st.container(border=True):
        pilihan = df['kemendagri_nama_kecamatan'].unique()

        kec_terpilih = st.selectbox('Pilih Kecamatan', pilihan)

        if kec_terpilih:
            df2 = df[df['kemendagri_nama_kecamatan'] == kec_terpilih]
            
            st.subheader(f'Luas Wilayah Kecamatan {kec_terpilih} menurut Desa (Km2)')
            
            kol1a, kol2a = st.columns(2)
            with kol1a:
                fig = px.treemap(df2, path=['kemendagri_nama_kecamatan', 'kemendagri_nama_desa_kelurahan'], 
                                values='luas_wilayah')
                st.plotly_chart(fig, use_container_width=True)

            with kol2a:
                fig2 = px.pie(df2, values='luas_wilayah', names='kemendagri_nama_desa_kelurahan')
                st.plotly_chart(fig2, use_container_width=True)
            
with st.expander('Lihat Tabel'):
    st.dataframe(df2, use_container_width=True, hide_index=True)
    st.caption('Sumber: https://opendata.jabarprov.go.id/id/dataset/luas-wilayah-desa-berdasarkan-desakelurahan-di-jawa-barat')

st.subheader('', divider='rainbow')
st.caption(':green[Statistik Daerah Kabupaten Subang]')
st.caption(':green[Hak Cipta @ BPS Kabupaten Subang]')