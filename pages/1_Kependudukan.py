import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(layout='wide')

st.title(':orange[STATISTIK] :blue[KEPENDUDUKAN] :green[Kabupaten Subang]')
#st.subheader('BANDUNG KOTA :orange[dalam] :green[GRAFIK] :orange[dan] :blue[INDIKATOR]', divider='rainbow')
st.subheader('', divider='rainbow')

# Menampilkan grafik tahunan
with st.container(border=True):
    # URL API Open Data
    url = "https://data.jabarprov.go.id/api-backend//bigdata/disdukcapil_2/od_17892_jml_penduduk__jk_kabupatenkota?limit=100&skip=0&where=%7B%22kode_kabupaten_kota%22%3A%5B%223213%22%5D%7D"

    # Fungsi untuk mengambil data
    response = requests.get(url)
    data = response.json()

    # Mengubah data menjadi pandas dataframe
    df = pd.DataFrame(data['data'])

    df_total = df.groupby(['nama_kabupaten_kota', 'tahun'])['jumlah_penduduk'].sum().reset_index()

    st.subheader('Perkembangan Jumlah Penduduk Kabupaten Subang')
    
    tab1, tab2, tab3, tab4 = st.tabs(['Total', 'Jenis Kelamin', 'Umur', 'Status Kawin'])
    
    fig1 = px.bar(df_total, x='tahun', y='jumlah_penduduk', text='jumlah_penduduk')
    fig2 = px.bar(df, x='tahun', y='jumlah_penduduk', color='jenis_kelamin', 
                  text='jumlah_penduduk')
    
    # Menempatkan legenda di bawah grafik
    fig2.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5,
        title_text=''
    ))
    
    # TOTAL
    with tab1:
        st.plotly_chart(fig1, use_container_width=True)
        
        with st.expander('Lihat Tabel'):
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption('Sumber: https://opendata.jabarprov.go.id/id/dataset/jumlah-penduduk-berdasarkan-jenis-kelamin-dan-kabupatenkota-di-jawa-barat')

    # JENIS KELAMIN
    with tab2:
        st.plotly_chart(fig2, use_container_width=True)
        
        with st.expander('Lihat Tabel'):
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption('Sumber: https://opendata.jabarprov.go.id/id/dataset/jumlah-penduduk-berdasarkan-jenis-kelamin-dan-kabupatenkota-di-jawa-barat')

    # KELOMPOK UMUR
    with tab3:
        url3 = 'https://data.jabarprov.go.id/api-backend//bigdata/disdukcapil_2/od_18305_jml_penduduk__kelompok_umur_kabupatenkota?limit=1000&skip=0&where=%7B%22kode_kabupaten_kota%22%3A%5B%223213%22%5D%7D'
        
        response3 = requests.get(url3)
        
        data3 = response3.json()
        
        df3 = pd.DataFrame(data3['data'])
        
        df3['kelompok_umur'] = df3['kelompok_umur'].replace({'00-04':'00 - 04', '05-09':'05 - 09'})
        
        df3 = df3.sort_values(by=['tahun', 'kelompok_umur'], ascending=[False, True])
        
        tahun = df3['tahun'].unique()
        
        pilihan = st.selectbox('Filter Tahun', tahun)
        
        if pilihan:
            st.subheader(f'Penduduk Kabupaten Subang menurut Kelompok Umur Tahun {pilihan}')
        
            df_tahun = df3[df3['tahun'] == pilihan]
            df_tahun['kelompok_umur'] = df_tahun['kelompok_umur'].astype(str)
            
            piramida = df_tahun.pivot_table(index='kelompok_umur', columns='jenis_kelamin', values='jumlah_penduduk')
            piramida = piramida.reset_index()
            piramida['kelompok_umur'] = piramida['kelompok_umur'].astype(str)
            
            piramida['LAKI-LAKI'] = -piramida['LAKI-LAKI']
            
            kol1, kol2 = st.columns(2)
            with kol1:
                grafik = px.bar(piramida, x=['LAKI-LAKI', 'PEREMPUAN'], y='kelompok_umur')
                
                # Menempatkan legenda di bawah grafik
                grafik.update_layout(legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.3,
                    xanchor="center",
                    x=0.5,
                    title_text=''
                ))
                st.plotly_chart(grafik, use_container_width=True)
            
            with kol2:
                fig3 = px.sunburst(df_tahun, path=['nama_kabupaten_kota', 'jenis_kelamin', 'kelompok_umur'],
                            values='jumlah_penduduk')

                st.plotly_chart(fig3, use_container_width=True)
                
            fig3a = px.treemap(df_tahun, path=['nama_kabupaten_kota', 'kelompok_umur', 'jenis_kelamin'],
                            values='jumlah_penduduk')

            st.plotly_chart(fig3a, use_container_width=True)
        
            with st.expander('Lihat Tabel'):
                del df3['id']
                st.dataframe(df3, use_container_width=True, hide_index=True)

                st.caption('Sumber: https://opendata.jabarprov.go.id/id/dataset/jumlah-penduduk-berdasarkan-kelompok-umur-dan-kabupatenkota-di-jawa-barat')
    
    # STATUS KAWIN    
    with tab4:
        st.subheader('Penduduk Kabupaten Subang menurut Status Kawin')
        url4 = 'https://data.jabarprov.go.id/api-backend//bigdata/disdukcapil_2/od_15135_jumlah_penduduk_berdasarkan_status_perkawinan_v1?limit=3000&skip=0&where=%7B%22kode_kabupaten_kota%22%3A%5B%223213%22%5D%7D'

        response4 = requests.get(url4)
        data4 = response4.json()
        
        df4 = pd.DataFrame(data4['data'])
        
        fig4 = px.bar(df4, x='tahun', y='jumlah_penduduk', text='jumlah_penduduk', 
                      color='status_kawin')
        
        # Menempatkan legenda di bawah grafik
        fig4.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
            title_text=''
        ))
        
        st.plotly_chart(fig4, use_container_width=True, hide_index=True)
        
        with st.expander('Lihat Tabel'):
            st.dataframe(df4, use_container_width=True, hide_index=True)
            st.caption('Sumber: https://opendata.jabarprov.go.id/id/dataset/jumlah-penduduk-berdasarkan-status-perkawinan-di-jawa-barat')    

st.subheader('', divider='rainbow')
st.caption(':green[Statistik Daerah Kabupaten Subang]')
st.caption(':green[Hak Cipta @ BPS Kabupaten Subang]')