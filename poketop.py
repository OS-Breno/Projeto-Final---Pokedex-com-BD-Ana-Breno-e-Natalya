import mysql.connector

def cadastrar_pokemon(nome, tipo, nivel, hp, atq, defe, img):
    try:
        #conectamos ao banco de dados mysql
        conn = mysql.connector.connect(
            host="pokemondb.mysql.dbaas.com.br",
            user="pokemondb",
            password="Ana#200907",
            database="pokemondb"
        )
        cursor = conn.cursor()

        # garante que a tabela existe
        query_tabela = """
            CREATE TABLE IF NOT EXISTS pokemontop (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100),
                tipo VARCHAR(50),
                nivel INT,
                hp INT,
                atq INT,
                defe INT,
                img LONGBLOB
            )
            """
        cursor.execute(query_tabela)

        # Inseri o novo pokemon aos dados danadinhos
        query_insert = "INSERT INTO pokemontop (nome, tipo, nivel, hp, atq, defe, img) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        valores = (nome, tipo, nivel, hp, atq, defe, img)
        cursor.execute(query_insert, valores)
        conn.commit()

        # Mostra a lista completa de TODOS pokmons salvos no banco
        cursor.execute("SELECT * FROM pokemontop")
        todos_os_pokemons = cursor.fetchall()
        return todos_os_pokemons

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
