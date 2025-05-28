import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

st.set_page_config(page_title='Dashboard de Campanhas', page_icon='📊', layout='wide')

cores = ['#118DFF', '#102790' ]

df = pd.read_excel('planilha_GERAL.xlsx')
df.columns = df.columns.str.strip()
df['Data'] = pd.to_datetime(df['Data'], errors='coerce')

st.sidebar.header('🎛️ Filtros')

anos_disponiveis = sorted(df['Data'].dt.year.dropna().unique())
ano_campanha = st.sidebar.multiselect(
    'Selecione o Ano:',
    options=anos_disponiveis,
    default=anos_disponiveis,
    key='Ano'
)

tipos_disponiveis = sorted(df['Tipo Campanha'].dropna().unique())
tipo_campanha = st.sidebar.multiselect(
    'Selecione o Tipo da Campanha:',
    options=tipos_disponiveis,
    default=tipos_disponiveis,
    key='Campanha'
)

df_filtrado = df[
    df['Data'].dt.year.isin(ano_campanha) &
    df['Tipo Campanha'].isin(tipo_campanha)
]

def Home():
    st.title("")

    total_campanhas_sp = len(df_filtrado)
    total_estados = '15'
    total_campanhas_br = '976'
    total_cidades_sp = '42'
    total_tematica = '8'
    periodo_dados = 'Dados referente ao período de jan/21 a mai/25'

    st.markdown("### Visão Geral")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(label="Registros/BR", value=total_campanhas_br)

    with col2:
        st.metric(label="UF", value=total_estados)
    with col3:
        st.metric(label="Registros/SP", value=total_campanhas_sp)

    with col4:
        st.metric(label="Cidades/SP", value=total_cidades_sp)

    with col5:
        st.metric(label="Temáticas", value=total_tematica)

    st.text(periodo_dados)

    st.markdown("---")

    st.title("📈 Análises de Dados")

    contagem_campanhas = df_filtrado['Tipo Campanha'].value_counts().reset_index()
    contagem_campanhas.columns = ['Tipo Campanha', 'Quantidade']
    fig_pizza = px.pie(
        contagem_campanhas,
        names='Tipo Campanha',
        values='Quantidade',
        title='Distribuição de Campanhas por Tipo',
        color_discrete_sequence=cores
    )

    df_filtrado['Ano'] = df_filtrado['Data'].dt.year
    comparativo_anual = df_filtrado.groupby(['Ano', 'Tipo Campanha']).size().reset_index(name='Quantidade')

    fig_ano = px.bar(
        comparativo_anual,
        x='Ano',
        y='Quantidade',
        color='Tipo Campanha',
        title='Comparativo de Campanhas por Ano e Tipo',
        text='Quantidade',
        barmode='group',
        color_discrete_sequence=cores
    )

    origem_contagem = df_filtrado['Origem Base Dados'].value_counts().reset_index()
    origem_contagem.columns = ['Origem Base Dados', 'Quantidade']

    fig_origem = px.bar(
        origem_contagem,
        x='Quantidade',
        y='Origem Base Dados',
        title='Origem dos Dados',
        orientation='h',
        color = 'Origem Base Dados',
        color_discrete_sequence=cores,
        text='Quantidade'        
    )

    
    tabela = {'Cidade': ['São Paulo', 'Praia Grande', 'São Vicente', 'Guarulhos', 'Indaiatuba', 'CampinasS'],'Quantidade':[117,13,13,10,9,8]}
    df_tabela = pd.DataFrame(tabela)
    


    if 'Campanha' in df_filtrado.columns:
        freq = df_filtrado['Campanha'].value_counts().reset_index()
        freq.columns = ['Campanha', 'Número de Registros']
        fig_frequencia = px.bar(
            freq,
            x='Campanha',
            y='Número de Registros',
            title='Frequência de Cada Campanha',
            text='Número de Registros',
            color_discrete_sequence=cores
        )
        fig_frequencia.update_traces(textangle=0)



    st.plotly_chart(fig_origem, use_container_width=True)
    st.plotly_chart(fig_pizza, use_container_width=True)
    st.plotly_chart(fig_frequencia, use_container_width=True) 
    st.plotly_chart(fig_ano, use_container_width=True)
    st.markdown("<p style='font-size:18px; font-weight:bold;'>Cidades com Maior Número de Registros</p>", unsafe_allow_html=True)
    st.table(df_tabela)

def Menu():
    with st.sidebar:
        selecionado = option_menu(
            menu_title='Menu',
            options=['Projeto Limpa Brasil'],
            icons=['house',],
            default_index=0
        )
    return selecionado

def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css("streamlit.css")

if df_filtrado.empty:
    st.warning("Nenhuma campanha encontrada para os critérios selecionados.")
else:
    selecao = Menu()
    if selecao == 'Projeto Limpa Brasil':
        Home()

