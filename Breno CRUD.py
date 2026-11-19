import requests
class servicos:
    def inserir(self, nome, tipo, nivel, hp, atq, defe):
        conexao = criar_conexao()
        if conexao:
            try:
                cursor = conexao.cursor() 
                sql = 'INSERT INTO pokemons (nome, tipo, nivel, hp, atq, defe, id) VALUES (%s, %s, %s, %s, %s, %s, %s)'
                valores = (nome, tipo, nivel, hp, atq, defe)
                cursor.execute(sql, valores)
                conexao.commit()
                return True
            except Error as e:
                print(f'Houve um erro ao inserir: {e}')
                return False
            finally:
                cursor.close()
                conexao.close()
        return False

    def consultar(self):
        conexao = criar_conexao()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute('SELECT id, nome, tipo, nivel, hp, atq, defe, quantidade FROM pokemons') 
                resultados = cursor.fetchall()
                return resultados
            except Error as e:
                print(f'Erro ao listar: {e}')
                return []
            finally:
                cursor.close()
                conexao.close()
        return []

    def atualizar(self, id, nome, tipo, nivel, hp, atq, defe):
        conexao = criar_conexao()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = 'UPDATE pokemons SET nome=%s, tipo=%s, nivel=%s, hp=%s, atq=%s, defe=%s, id=%s'
                valores = (nome, tipo, nivel, hp, atq, defe, id_pokemon)
                cursor.execute(sql, valores)
                conexao.commit()
                return True
            except Error as e:
                print(f'Erro ao atualizar: {e}')
                return False
            finally:
                cursor.close()
                conexao.close()
        return False

    def deletar(self, id):
        conexao = criar_conexao()
        if conexao:
            try:
                cursor = conexao.cursor()
                sql = 'DELETE FROM pokemons WHERE id=%s'
                cursor.execute(sql, (id_pokemon,))
                conexao.commit()
                return True
            except Error as e:
                print(f'Erro ao deletar: {e}')
                return False
            finally:
                cursor.close()
                conexao.close()
        return False

    def baixar_imagem(self, nome):
        imagem=requests.get(f"https://pokeapi.co/api/v2/pokemon/{nome}"["sprites"]["other"]["official-artwork"]["front_default"], width=200)
        if imagem.status_code == 200:
            return imagem.content
        else:
            print("Erro ao obter a imagem!")
            return None
