import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

st.set_page_config(page_title='Dashboard de Eventos', page_icon='🛒', layout='wide')
df = pd.read_excel('Base de Dados Final.xlsx')
df.columns = df.columns.str.strip()

st.sidebar.header('Selecione os Filtros')

tipo_evento = st.sidebar.multiselect(
    'Tipos de eventos', 
    options=df['Tipo Evento'].unique(),
    default=df['Tipo Evento'].unique(),
    key='Evento'
)
df_selecao = df.query('`Tipo Evento` in @tipo_evento')

def Home():
    st.title("Eventos Limpa Brasil (2021-2025)")

    total_eventos = len(df_selecao)

    col1 = st.columns(1)
    with col1[0]:
        st.metric('Total de Eventos', value=total_eventos)

    st.markdown('---')
def Graficos():
    contagem_eventos = df_selecao['Tipo Evento'].value_counts().reset_index()
    contagem_eventos.columns = ['Tipo Evento', 'Quantidade']

    fig_barras = px.bar(
        contagem_eventos,
        x='Tipo Evento',
        y='Quantidade',
        color='Tipo Evento',
        title='Distribuição de Eventos por Tipo'
    )

    graf1 = st.columns(1)
    with graf1[0]:
        st.plotly_chart(fig_barras, use_container_width=True)

def sideBar():
    with st.sidebar:
        selecionado = option_menu(
            menu_title='Menu',
            options=['Home', 'Gráficos'],
            icons=['🏠', '📊'],
            default_index=0
        )

    if selecionado == 'Home':
        Home()
        Graficos()
    elif selecionado == 'Gráficos':
        Graficos()
sideBar()
