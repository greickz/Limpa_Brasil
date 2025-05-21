import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

st.set_page_config(page_title='Dashboard de Campanhas', page_icon='📊', layout='wide')

df = pd.read_excel('planilha_GERAL.xlsx')
df.columns = df.columns.str.strip()  

df['Data'] = pd.to_datetime(df['Data'], errors='coerce')

st.sidebar.header('🎛️ Filtros')

ano_campanha = st.sidebar.multiselect(
    'Selecione o Ano:',
    options=sorted(df['Data'].dt.year.dropna().unique()), 
    default=sorted(df['Data'].dt.year.dropna().unique()),
    key='Ano'
)

tipo_campanha = st.sidebar.multiselect(
    'Selecione o Tipo da Campanha:',
    options=sorted(df['Tipo Campanha'].dropna().unique()),
    default=sorted(df['Tipo Campanha'].dropna().unique()),
    key='Campanha'
)

df_selecao = df.query('`Data`.dt.year in @ano_campanha and `Tipo Campanha` in @tipo_campanha')

if df_selecao.empty:
    st.warning("Nenhuma campanha encontrado para os critérios selecionados.")
else:
    def Home():
        st.title("Campanhas Limpa Brasil (2021–2025)")
        total_campanhas = len(df_selecao)

        st.markdown("Visão Geral")
        st.metric(label="Total de Campanhas Selecionados", value=total_campanhas)
        st.markdown("---")

    def Graficos():
        st.title("📈 Análises de Campanhas")

        contagem_campanhas = df['Tipo Campanha'].value_counts().reset_index()   
        contagem_campanhas.columns = ['Tipo Campanha', 'Quantidade']

        fig_barras = px.bar(
            contagem_campanhas,
            x='Tipo Campanha',
            y='Quantidade',
            color='Tipo Campanha',
            title='Distribuição de Campanhas por Tipo',
            text='Quantidade'
        )

        df_selecao = df.set_index('Data')
        comparativo_anual = df_selecao.groupby('Tipo Campanha').resample('Y').size().reset_index(name='Quantidade')

        fig_comparativo = px.line(
            comparativo_anual,
            x='Data',
            y='Quantidade',
            color='Tipo Campanha',
            title='Comparativo de Campanhas por Ano e Tipo',
            text='Quantidade'
        )

        st.plotly_chart(fig_barras, use_container_width=True)
        st.plotly_chart(fig_comparativo, use_container_width=True)

    def Menu():
        with st.sidebar:
            selecionado = option_menu(
                menu_title='📂 Menu',
                options=['Home', 'Gráficos'],
                icons=['house', 'bar-chart'],
                default_index=0
            )
        return selecionado

    def load_css(file_name):
        try:
            with open(file_name) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        except FileNotFoundError:
            pass

    selecao = Menu()

    if selecao == 'Home':
        Home()
    elif selecao == 'Gráficos':
        Graficos()

    load_css("plot.css")
