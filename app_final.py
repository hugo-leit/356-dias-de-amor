import streamlit as st
import pandas as pd
from datetime import datetime

@st.cache_data
def carregar_mensagens():
    df = pd.read_csv("mensagens_356_dias_com_link_novo.csv", sep=";", encoding="ISO-8859-1")
    
    # Normaliza e converte a data
    df["data"] = pd.to_datetime(df["data"], dayfirst=True, errors="coerce").dt.strftime("%-d/%-m/%y")
    
    # Cria dicionário com mensagens organizadas por data
    mensagens = {}
    for _, row in df.iterrows():
        data = row["data"]
        tipo = row["tipo"].strip().lower()
        conteudo = str(row["conteudo"]).strip()
        
        if not data or not tipo or not conteudo or conteudo == "nan":
            continue
        
        if data not in mensagens:
            mensagens[data] = {}
        mensagens[data][tipo] = conteudo

    return mensagens

# Interface
st.set_page_config(page_title="356 Dias de Amor 💖", page_icon="💌")
st.title("💘 356 Dias de Amor 💘")
st.write("Escolha uma data para ver sua surpresa especial:")

# Entrada do usuário
dia = st.selectbox("Dia", list(range(1, 32)))
mes = st.selectbox("Mês", list(range(1, 13)))
ano = st.selectbox("Ano", ["24", "25"])

data_str = f"{dia}/{mes}/{ano[-2:]}"
mensagens = carregar_mensagens()

# Mostrar mensagem
msg = mensagens.get(data_str)
if msg:
    st.markdown(f"### Mensagem para {data_str}")
    
    if "poema" in msg and pd.notna(msg["poema"]):
        st.subheader("💌 Poema")
        st.write(msg["poema"])
    
    if "link" in msg and pd.notna(msg["link"]):
        st.subheader("🎵 Link especial")
        st.markdown(f'<a href="{msg["link"]}" target="_blank">💖 Clique aqui 💖</a>', unsafe_allow_html=True)
else:
    st.warning("Data inválida ou sem mensagem cadastrada.")
