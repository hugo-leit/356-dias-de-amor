
import streamlit as st
import pandas as pd

# === FUNDO ANIMADO COM CORAÇÕES ===
hearts_animation = """
<style>
body {{
    background-color: #fff0f5;
    overflow: hidden;
}}
.heart {{
    position: absolute;
    width: 20px;
    height: 20px;
    background: red;
    transform: rotate(45deg);
    animation: float 10s linear infinite;
}}
.heart::before, .heart::after {{
    content: "";
    position: absolute;
    width: 20px;
    height: 20px;
    background: red;
    border-radius: 50%;
}}
.heart::before {{
    top: -10px;
    left: 0;
}}
.heart::after {{
    left: -10px;
    top: 0;
}}
@keyframes float {{
    0% {{
        bottom: -10%;
        left: calc(100% * var(--i));
        opacity: 1;
    }}
    100% {{
        bottom: 110%;
        left: calc(100% * var(--i) + 30px);
        opacity: 0;
    }}
}}
</style>
<div>
  {}
</div>
"""
hearts_divs = "".join([f'<div class="heart" style="--i:{i/10}"></div>' for i in range(10)])
st.markdown(hearts_animation.format(hearts_divs), unsafe_allow_html=True)

# === TÍTULO ===
st.title("356 Dias de Amor")

# === LEITURA DO CSV ===
@st.cache_data
def carregar_mensagens():
    df = pd.read_csv("mensagens_356_dias_com_link_novo.csv", sep=";", encoding="utf-8")
    mensagens = {}
    for _, row in df.iterrows():
        data = row["data"]
        tipo = row["tipo"]
        conteudo = row["conteudo"]
        if data not in mensagens:
            mensagens[data] = {}
        mensagens[data][tipo] = conteudo
    return mensagens

mensagens = carregar_mensagens()

# === SELEÇÃO DE DATA ===
dia = st.selectbox("Dia", list(range(1, 32)))
mes = st.selectbox("Mês", list(range(1, 13)))
ano = st.selectbox("Ano", [2024, 2025])

try:
    data_str = f"{ano}-{mes:02d}-{dia:02d}"
    msg = mensagens.get(data_str)

    if msg:
        st.markdown(f"### Mensagem para {data_str}")
        if "poema" in msg and msg["poema"]:
            st.subheader("💌 Poema")
            st.write(msg["poema"])
        if "link" in msg and msg["link"]:
            st.subheader("🎵 Link especial")
            st.markdown(f'<a href="{msg["link"].strip()}" target="_blank">💖 Clique aqui 💖</a>', unsafe_allow_html=True)
    else:
        st.warning("Ainda não há conteúdo para esse dia.")
except:
    st.error("Data inválida.")
