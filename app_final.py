import streamlit as st
import pandas as pd
from datetime import datetime

@st.cache_data
def carregar_mensagens():
    df = pd.read_csv("lindo.csv", sep=";", encoding="utf-8")
    df.columns = df.columns.str.strip().str.lower()

    df["data"] = pd.to_datetime(df["data"], dayfirst=True, errors="coerce").dt.strftime("%-d/%-m/%y")

    mensagens = {}
    for _, row in df.iterrows():
        data = str(row["data"]).strip()
        tipo = str(row["tipo"]).strip().lower()
        conteudo = str(row["conteudo"]).strip()

        if not data or not tipo or not conteudo or conteudo.lower() == "nan":
            continue

        if data not in mensagens:
            mensagens[data] = {}
        mensagens[data][tipo] = conteudo

    return mensagens

st.set_page_config(page_title="356 Dias de Amor 💖", page_icon="💌")
st.title("💘 356 Dias de Amor 💘")
st.write("Escolha uma data para ver sua surpresa especial:")

dia = st.selectbox("Dia", list(range(1, 32)))
mes = st.selectbox("Mês", list(range(1, 13)))
ano = st.selectbox("Ano", ["24", "25"])

data_str = f"{dia}/{mes}/{ano}"
mensagens = carregar_mensagens()
msg = mensagens.get(data_str)

if msg:
    st.markdown(f"### Mensagem para {data_str}")
    
    if "poema" in msg and msg["poema"].strip():
        st.subheader("💌 Poema")
        st.write(msg["poema"])
    
    if "link" in msg and msg["link"].strip():
        st.subheader("🎵 Link especial")
        st.markdown(f'<a href="{msg["link"].strip()}" target="_blank">💖 Clique aqui 💖</a>', unsafe_allow_html=True)
else:
    st.warning("Data inválida ou sem mensagem cadastrada.")
