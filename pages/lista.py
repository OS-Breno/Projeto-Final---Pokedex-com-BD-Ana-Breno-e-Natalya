import streamlit as st
import base64
import mysql.connector
from pathlib import Path

def imagem_base64(nome_arquivo):
    caminho = Path(__file__).resolve().parent.parent / "imagens" / nome_arquivo
    with open(caminho, "rb") as arquivo:
        return base64.b64encode(arquivo.read()).decode()

imagem_poketop = imagem_base64("pokelista.PNG")
st.markdown(
    f'<img src="data:image/png;base64,{imagem_poketop}" width="250">',
    unsafe_allow_html=True,
)

# guarda qual pokemon está sendo alterado
if "editando" not in st.session_state:
    st.session_state.editando = None

# conexão com o banco
conexao = mysql.connector.connect(
    host="pokemondb.mysql.dbaas.com.br",
    user="pokemondb",
    password="Ana#200907",
    database="pokemondb"
)

cursor = conexao.cursor()
cursor.execute("SELECT id, nome, tipo, nivel, hp, atq, defe, img FROM pokemontop")
dados = cursor.fetchall()

st.markdown(
    """
    <style>
        .stApp {
            background-color: #A0AEE8;
        }
    [class*="st-key-pokemon-row-"] {
        background-color: #fef7c4;
        border-radius: 0.5rem;
        color: #12345a;
    }
    [class*="st-key-pokemon-row-"] [data-testid="stMarkdownContainer"],
    [class*="st-key-pokemon-row-"] [data-testid="stMarkdownContainer"] *,
    .st-key-lista-header [data-testid="stMarkdownContainer"],
    .st-key-lista-header [data-testid="stMarkdownContainer"] * {
        color: #12345a;
    }
    .st-key-voltar-button button {
        background-color: #fef7c4;
        color: #12345a;
        font-weight: 700;
    }
    .st-key-voltar-button button p {
        color: #12345a;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

col_acc, col_lista = st.columns([2.5, 7.5],gap="small",vertical_alignment="bottom",)

with col_acc:
    imagem_pokechila = imagem_base64("Pokechila.PNG")
    st.markdown(
        f'<img src="data:image/png;base64,{imagem_pokechila}" width="250">',
        unsafe_allow_html=True,
    )


with col_lista:
    with st.container(key="lista-header"):
        cab = st.columns([1, 1, 1.5, 0.7, 1, 0.8, 0.8, 1, 0.9, 1])
        cab[2].write("**Nome**")
        cab[3].write("**ID**")
        cab[4].write("**Tipo**")
        cab[5].write("**LVL**")
        cab[6].write("**HP**")
        cab[7].write("**ATQ**")
        cab[8].write("**DEF**")
        cab[9].write("**IMG**")

    # uma linha para cada pokémon, com lixeira e lápis
    for p in dados:
        pid, nome, tipo, nivel, hp, atq, defe, img = p
        with st.container(border=True, key=f"pokemon-row-{pid}"):
            col = st.columns(
                [1, 1, 1.5, 0.7, 1, 0.8, 0.8, 1, 0.9, 1],
                vertical_alignment="center",
            )

            # apagar: remove o pokémon do banco pelo id
            if col[0].button("🗑️", key=f"apagar{pid}"):
                cursor.execute("DELETE FROM pokemontop WHERE id = %s", (pid,))
                conexao.commit()
                st.rerun()

            # editar: guarda o id do pokémon escolhido
            if col[1].button("✏️", key=f"editar{pid}"):
                st.session_state.editando = pid
                st.rerun()

            col[2].write(nome)
            col[3].write(str(pid))
            col[4].write(tipo)
            col[5].write(str(nivel))
            col[6].write(str(hp))
            col[7].write(str(atq))
            col[8].write(str(defe))
            if img:
                col[9].image(img)
            else:
                col[9].write("Sem imagem")

    # formulário que aparece ao clicar no lápis
    if st.session_state.editando is not None:
        for p in dados:
            if p[0] == st.session_state.editando:
                st.subheader("Editar pokémon")
                with st.form("form_editar"):
                    novo_nome = st.text_input("Nome", p[1])
                    novo_tipo = st.text_input("Tipo", p[2])
                    novo_nivel = st.number_input("Nível", value=p[3], step=1)
                    novo_hp = st.number_input("HP", value=p[4], step=1)
                    novo_atq = st.number_input("Ataque", value=p[5], step=1)
                    novo_defe = st.number_input("Defesa", value=p[6], step=1)
                    salvar = st.form_submit_button("Salvar")

                # atualiza os dados do pokémon no banco pelo id
                if salvar:
                    cursor.execute(
                        "UPDATE pokemontop SET nome = %s, tipo = %s, nivel = %s, hp = %s, atq = %s, defe = %s WHERE id = %s",
                        (novo_nome, novo_tipo, novo_nivel, novo_hp, novo_atq, novo_defe, p[0])
                    )
                    conexao.commit()
                    st.session_state.editando = None
                    st.rerun()
    if st.button("Voltar", use_container_width=True, key="voltar-button"):
        st.switch_page("streamlittela1.py")

# fecha a conexão no final
cursor.close()
conexao.close()
