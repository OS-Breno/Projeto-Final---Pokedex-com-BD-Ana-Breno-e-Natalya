import base64
from pathlib import Path
import streamlit as st
from poketop import cadastrar_pokemon
import requests

def imagem_base64(nome_arquivo):
    caminho = Path(__file__).resolve().parent.parent / "imagens" / nome_arquivo
    with open(caminho, "rb") as f:
        return base64.b64encode(f.read()).decode()

TIPOS = ["Normal", "Fogo", "Água", "Elétrico", "Grama", "Gelo", "Luta", "Veneno",
         "Terra", "Voo", "Vidente", "Inseto", "Pedra", "Fantasma", "Dragão",
         "Escuridão", "Aço", "Fada"]

fundo = imagem_base64("fundo_inserir.png")
st.markdown(f"""
<style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{fundo}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    /* barra do topo transparente */
    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* espaço do topo (deixa o logo inteiro à mostra) e entre os campos */
    .block-container {
        padding-top: 4rem;
        padding-bottom: 1rem;
    }
    div[data-testid="stVerticalBlock"] {
        gap: 0.4rem;
    }

    /* caixas de texto */
    .stTextInput div[data-baseweb="input"] {
        background-color: #f7f5b7;
        border: none;
        border-radius: 0;
    }
    .stTextInput input {
        background-color: #f7f5b7;
        color: #1800ad;
        font-weight: bold;
        font-size: 18px;
    }
    .stTextInput input::placeholder {
        color: #1800ad;
        opacity: 1;
    }

    /* caixa de seleção do tipo */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #f7f5b7;
        border: none;
        border-radius: 0;
    }
    .stSelectbox div[data-baseweb="select"] * {
        color: #1800ad;
        font-weight: bold;
        font-size: 18px;
    }

    /* botões */
    .stButton {
        display: flex;
        justify-content: center;
    }
    .stButton button {
        background-color: #f7f5b7;
        border: 2px solid #1800ad;
        border-radius: 0;
        width: 110px;
        height: 40px;
    }
    .stButton button p {
        color: #1800ad;
        font-weight: bold;
        font-size: 18px;
    }
    .stButton button:hover {
        background-color: #e8e5a0;
    }
</style>
""", unsafe_allow_html=True)

logo = imagem_base64("pokeinserir.png")
st.markdown(f'<div style="text-align: center;"><img src="data:image/png;base64,{logo}" width="300"></div>',unsafe_allow_html=True)

nome = st.text_input("nome", placeholder="Nome...", label_visibility="collapsed")
tipo = st.selectbox("tipo", TIPOS, index=None, placeholder="Tipo...", label_visibility="collapsed")
nivel = st.text_input("nivel", placeholder="Nivel...", label_visibility="collapsed")
hp = st.text_input("hp", placeholder="HP...", label_visibility="collapsed")
atq = st.text_input("atq", placeholder="Ataque...", label_visibility="collapsed")
defe = st.text_input("defe", placeholder="Defesa...", label_visibility="collapsed")

# Voltar e Salvar lado a lado
col1, col2 = st.columns(2)

with col1:
    voltar = st.button("Voltar")
with col2:
    salvar = st.button("Salvar")

if voltar:
    st.switch_page("streamlittela1.py")

if salvar:
    if tipo is None:
        st.error("Escolha o tipo do pokémon")
    else:
        try:
            resposta=requests.get(f"https://pokeapi.co/api/v2/pokemon/{nome}")
            if resposta.status_code == 200:
                dadosimg = resposta.json()
                urlimg = dadosimg["sprites"]["other"]["official-artwork"]["front_default"]
                respostaimg = requests.get(urlimg)
                img = respostaimg.content
                cadastrar_pokemon(nome, tipo, int(nivel), int(hp), int(atq), int(defe), bytes(img))
                st.success("Pokemon cadastrado")
            else:
                st.warning("Pokemon não identificado; Verifique a ortografia do nome que digitou, ou tente novamente mais tarde (por possível erro de servidor).")

        # se digitar letra onde tinha que ser número
        except ValueError:
            st.error("Nível, vida, ataque e defesa precisam ser números inteiros")

        # se der erro no banco
        except Exception as err:
            st.error(f"Erro no banco de dados: {err}")
            
