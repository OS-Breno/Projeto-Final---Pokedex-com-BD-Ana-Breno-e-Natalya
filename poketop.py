import mysql.connector

print("--- Cadastro de Pokémon --")

# 1. Coletamos os dados digitados primeiro


       
nome = input("\nentre com o nome do seu pokemon: ")
tipo = input("entre com o tipo do seu pokemon: ")
nivel = int(input("entre com o nivel do seu pokemon: "))
hp = int(input("entre com a vida do seu pokemon: "))
atq = int(input("entre com o ataque do seu pokemon: "))
defe = int(input("entre com a defesa do seu pokemon: "))



try:
    #conectamos ao banco de dados mysql
    conn = mysql.connector.connect(
        host="pokemondb.mysql.dbaas.com.br",
        user="pokemondb",
        password="Ana#200907",
        database="pokemondb"
    )
    # garante que a tabela existe 
    query_tabela = """
        CREATE TABLE IF NOT EXISTS pokemontop (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100),
            tipo VARCHAR(50),
            nivel INT,
            hp INT,
            atq INT,
            defe INT
        )
        """
    cursor = conn.cursor()

  # Inseri o novo pokemon aos dados danadinhos
    query_insert = "INSERT INTO pokemontop (nome, tipo, nivel, hp, atq, defe) VALUES (%s, %s, %s, %s, %s, %s)"
    valores = (nome, tipo, nivel, hp, atq, defe)
    cursor.execute(query_insert, valores)
    conn.commit()
    print("\nPokémon cadastrado")

    # Mostra a lista completa de TODOS pokmons salvos no banco
    cursor.execute("SELECT * FROM pokemontop")
    todos_os_pokemons = cursor.fetchall()
    
    print("\n lista poketopzeira")
    for pokemon in todos_os_pokemons:
        print(pokemon)

        #se tudo der errado

except mysql.connector.Error as err:
    print(f"Erro no banco de dados: {err}")

finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("\nfim")