import mysql.connector
import streamlit as st
import base64

def imagem_base64(caminho):
    with open(caminho, "rb") as arquivo:
        return base64.b64encode(arquivo.read()).decode()

type_colors = {
    "Normal": "#A8A77A",
    "Fogo": "#EE8130",
    "Água": "#6390F0",
    "Elétrico": "#F7D02C",
    "Grama": "#7AC74C",
    "Gelo": "#96D9D6",
    "Luta": "#C22E28",
    "Veneno": "#A33EA1",
    "Terra": "#E2BF65",
    "Voo": "#A98FF3",
    "Vidente": "#F95587",
    "Inseto": "#A6B91A",
    "Pedra": "#B6A136",
    "Fantasma": "#735797",
    "Dragão": "#6F35FC",
    "Escuridão": "#705746",
    "Aço": "#B7B7CE",
    "Fada": "#D685AD",
}

if "pokemon_results" not in st.session_state:
    st.session_state.pokemon_results = []
if "pokemon_result_index" not in st.session_state:
    st.session_state.pokemon_result_index = 0
if "pokemon_search_done" not in st.session_state:
    st.session_state.pokemon_search_done = False

imagem_poketop = imagem_base64("imagens/pokeconsulta.png")
st.markdown(
    f'<img src="data:image/png;base64,{imagem_poketop}" width="250">',
    unsafe_allow_html=True,
)

col_input, col_button = st.columns([5, 1], vertical_alignment="bottom")
with col_input:
    procurado = st.text_input("",placeholder="Pesquisar")
with col_button:
    procurar = st.button("Procurar", use_container_width=True)

if procurar:
    conexao = mysql.connector.connect(
        host="pokemondb.mysql.dbaas.com.br",
        user="pokemondb",
        password="Ana#200907",
        database="pokemondb",
    )
    try:
        cursor = conexao.cursor()
        try:
            cursor.execute(
                "SELECT id, nome, tipo, nivel, hp, atq, defe, img "
                "FROM pokemontop WHERE nome = %s",
                (procurado.strip().lower(),),
            )
            st.session_state.pokemon_results = cursor.fetchall()
        finally:
            cursor.close()
    finally:
        conexao.close()

    st.session_state.pokemon_result_index = 0
    st.session_state.pokemon_search_done = True

resultados = st.session_state.pokemon_results
cor_fundo = "#424242"

if resultados:
    if len(resultados) > 1:
        col_ultimo, col_proximo = st.columns([1, 1])
        with col_ultimo:
            if st.button(
                "Resultado anterior",
                use_container_width=True,
                key="antecessor_pokemon_result",
            ):
                st.session_state.pokemon_result_index = (
                    st.session_state.pokemon_result_index - 1
                ) % len(resultados)
        with col_proximo:
            if st.button(
                "Próximo resultado",
                use_container_width=True,
                key="next_pokemon_result",
            ):
                st.session_state.pokemon_result_index = (
                    st.session_state.pokemon_result_index + 1
                ) % len(resultados)

    pokemon = resultados[st.session_state.pokemon_result_index]
    pokemon_id, nome, tipo, nivel, hp, atq, defe, img = pokemon
    cor_fundo = type_colors.get(str(tipo).strip().title(), "#424242")

    with st.container(key="pokemon-card"):
        col_imagem, col_dados = st.columns([1, 2], vertical_alignment="center")
        with col_imagem:
            if img:
                st.image(img, width=220)
        with col_dados:
            st.markdown(f"### {nome}")
            st.write(f"**Tipo:** {tipo}")
            st.write(f"**Nível:** {nivel}")
            st.write(f"**HP:** {hp}")
            st.write(f"**Ataque:** {atq}")
            st.write(f"**Defesa:** {defe}")
elif st.session_state.pokemon_search_done:
    st.info("Nenhum Pokémon encontrado com esse nome.")

st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {cor_fundo};
        }}
        .st-key-pokemon-card {{
            background-color: #ffffff;
            color: #111111;
            padding: 24px;
            border-radius: 16px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        }}
        .st-key-pokemon-card [data-testid="stMarkdownContainer"],
        .st-key-pokemon-card [data-testid="stMarkdownContainer"] * {{
            color: #111111 !important;
        }}
        div[data-testid="stButton"] button,
        div[data-testid="stButton"] button p {{
            background-color: #ffffff !important;
            color: #000000 !important;
            font-weight: 700 !important;
        }}
        div[data-testid="stTextInput"] input {{
            background-color: #ffffff !important;
            color: #000000 !important;
        }}
        div[data-testid="stTextInput"] input::placeholder {{
            color: #808080 !important;
            opacity: 1;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

if st.button("Voltar à tela inicial"):
    st.switch_page("streamlittela1.py")
