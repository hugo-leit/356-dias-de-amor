import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="356 Dias de Amor", layout="centered")

st.markdown(
    """
    <style>
    body {
        background-color: #fff0f5;
    }
    .heart {
        position: fixed;
        bottom: -100px;
        width: 20px;
        height: 20px;
        background: url('https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Red_Heart.svg/1024px-Red_Heart.svg.png');
        background-size: cover;
        animation: floatUp 6s infinite ease-in;
    }
    @keyframes floatUp {
        0% { transform: translateY(0); opacity: 1; }
        100% { transform: translateY(-120vh); opacity: 0; }
    }
    </style>
    <script>
    for (let i = 0; i < 15; i++) {
        let heart = document.createElement("div");
        heart.className = "heart";
        heart.style.left = Math.random() * 100 + "vw";
        heart.style.animationDelay = Math.random() * 5 + "s";
        document.body.appendChild(heart);
    }
    </script>
    """,
    unsafe_allow_html=True
)

st.title("💘 356 Dias de Amor 💘")
st.write("Escolha uma data para descobrir a mensagem especial de amor.")

@st.cache_data
def carregar_mensagens():
    df = pd.read_csv("mensagens_356_dias_com_link_novo.csv", sep=";", encoding="ISO-8859-1")
    df["data"] = pd.to_datetime(df["data"], dayfirst=True, errors="coerce").dt.date
    mensagens = {}
    for _, row in df.iterrows():
        data = row["data"]
        tipo = row["tipo"]
        conteudo = row["conteudo"]
        if pd.isna(data) or pd.isna(conteudo):
            continue
        if data not in mensagens:
            mensagens[data] = {}
        mensagens[data][tipo] = conteudo
    return mensagens

mensagens = carregar_mensagens()

# Interface de seleção de data
hoje = datetime.date.today()
data_selecionada = st.date_input("Escolha a data", value=hoje, format="DD/MM/YYYY")

# Buscar e mostrar mensagem
data_str = data_selecionada.strftime("%Y-%m-%d")
msg = mensagens.get(data_selecionada)

if msg:
    st.markdown(f"### Mensagem para {data_selecionada.strftime('%d/%m/%Y')}")
    if "poema" in msg and msg["poema"]:
        st.subheader("💌 Poema")
        st.write(msg["poema"])
    if "link" in msg and msg["link"]:
        st.subheader("🎵 Link especial")
        st.markdown(
            f'<a href="{msg["link"].strip()}" target="_blank">💖 Clique aqui 💖</a>',
            unsafe_allow_html=True
        )
else:
    st.warning("Data inválida ou sem mensagem.")
