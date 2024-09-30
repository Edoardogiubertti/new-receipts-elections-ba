import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Receitas")
df = pd.read_csv("./data/receitas_candidatos_2024_BA.csv", encoding='latin-1', sep=';')
df = df[['NM_UE', 'NR_CNPJ_PRESTADOR_CONTA', 
       'DS_CARGO', 'NM_CANDIDATO',
       'SG_PARTIDO',
       'NM_PARTIDO', 'NM_DOADOR',
       'NM_DOADOR_RFB', 'SG_UF_DOADOR', 
       'NM_MUNICIPIO_DOADOR', 
       'NR_PARTIDO_DOADOR', 'SG_PARTIDO_DOADOR', 'NM_PARTIDO_DOADOR',
       'VR_RECEITA', 'DS_GENERO', 'DS_COR_RACA']]
df['VR_RECEITA'] = df['VR_RECEITA'].str.replace(",", ".")
df['VR_RECEITA'] = df['VR_RECEITA'].astype(float)
lista_cidades = ['SALVADOR', 'CAMAÇARI', 'LAURO DE FREITAS', 'VITÓRIA DA CONQUISTA', 'FEIRA DE SANTANA', 'ILHÉUS', 'ITABUNA', 'SANTO ANTÔNIO DE JESUS']
df_cidades = df.loc[df['NM_UE'].isin(lista_cidades)]
# df_cidades

df_candidatos = df_cidades.groupby(['NM_CANDIDATO', 'DS_CARGO', 'SG_PARTIDO', 'NM_UE'])['VR_RECEITA'].sum().reset_index()
df_candidatos = df_candidatos.loc[df_candidatos['NM_UE'] == "SALVADOR"]
df_candidatos = df_candidatos.sort_values("VR_RECEITA", ascending=False).head(10)
# df_candidatos
df_grouped = df_cidades.groupby(['NM_UE', 'SG_PARTIDO'])['VR_RECEITA'].sum().reset_index()
# Encontrar o partido com maior investimento por cidade
df_max_partido_cidade = df_grouped.loc[df_grouped.groupby('NM_UE')['VR_RECEITA'].idxmax()].reset_index(drop=True)
df_max_partido_cidade = df_max_partido_cidade.sort_values("VR_RECEITA", ascending=False)


fig = px.bar(df_max_partido_cidade, x='NM_UE', y='VR_RECEITA', color="SG_PARTIDO")
st.markdown("### Partidos que mais investiram nas cidades observadas")
fig
fig_candidato = px.bar(df_candidatos, x='NM_CANDIDATO', y='VR_RECEITA', color='SG_PARTIDO')
st.markdown("### Candidatos que mais receberam recursos para a eleição de Salvador")
fig_candidato