#esse é o streamlittela1

import base64
import streamlit as st

def imagem_base64(caminho):
    with open(caminho, "rb") as f:
        return base64.b64encode(f.read()).decode()

st.markdown("""
<style>
    .stApp {
        background-color: #f7f5b7;
    }

    .stHorizontalBlock {
        margin-top: 225px;
    }

    .stButton {
        display: flex;
        justify-content: center;
    }

    .stButton button {
        background-color: #a61933;
        color: white;
        border: 2px solid #B71C1C;
        border-radius: 10px;
        width: 120px;
    }

    .stButton button p {
        color: white;
        display: flex;
        justify-content: center;
    }

    .stButton button:hover {
        background-color: #7a1226;
        color: white;
    }

    .st-key-botao_Consultar button {
        background-color: #1800ad;
        border: 2px solid #1800ad;
    }

    .st-key-botao_Consultar button:hover {
        background-color: #14085f;
        border: 2px solid #1800ad;
    }
</style>
""", unsafe_allow_html=True)

titulo = imagem_base64("imagens/titulo_poketop_sem_fundo.png")
img = imagem_base64("imagens/pokebola_sem_fundo.png")
img2 = imagem_base64("imagens/pokebola_vermelha_sem_fundo.png")

st.markdown(f"""
<style>
    .titulo {{
        position: fixed;
        top: 60px;
        left: 50%;
        transform: translateX(-50%);
        width: 450px;
        z-index: 5;
    }}
    .bola {{
        position: fixed;
        top: 60%;
        transform: translateY(-50%);
        width: 350px;
        z-index: 0;
    }}
    .bolaa {{
        position: fixed;
        top: 60%;
        transform: translateY(-50%);
        width: 900px;
        z-index: 0;
    }}
    .bola-esq {{
        left: -450px;
    }}
    .bola-dir {{
        right: -175px;
    }}
</style>
<img class="titulo" src="data:image/png;base64,{titulo}">
<img class="bolaa bola-esq" src="data:image/png;base64,{img}">
<img class="bola bola-dir" src="data:image/png;base64,{img2}">
""", unsafe_allow_html=True)

_, ins, cons, lis, _ = st.columns([2, 1, 1, 1, 2])

if ins.button("Inserir"):
    st.switch_page("pages/inserir.py")

with cons:
    with st.container(key="botao_Consultar"):
        clicou_Consultar = st.button("Consultar")

if clicou_Consultar:
    st.switch_page("pages/consultar.py")

if lis.button("Lista"):
    st.switch_page("pages/lista.py")

st.markdown("""
<style>
    .rodape {
        position: fixed;
        bottom: 15px;
        left: 50%;
        transform: translateX(-50%);
        white-space: nowrap;
        color: #1800ad;
        font-weight: bold;
        z-index: 999;
    }
</style>
<div class="rodape">Ana Luiza Machado, Breno Oliveira e Natalya Novais/2026</div>
""", unsafe_allow_html=True)