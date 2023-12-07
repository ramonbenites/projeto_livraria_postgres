from model.categoria import Categoria
from database.conexao_factory import ConexaoFactory


class CategoriaDAO:

    def __init__(self):
        self.__categorias: list[Categoria] = list()
        self.__conexao_factory: ConexaoFactory = ConexaoFactory()

    def listar(self) -> list[Categoria]:
        categorias = list()

        conexao = self.__conexao_factory.get_conexao()
        cursor = conexao.cursor()
        cursor.execute('SELECT id, nome FROM categorias')
        resultados = cursor.fetchall()
        for resultado in resultados:
            cat = Categoria(resultado[1])
            cat.id = resultado[0]
            categorias.append(cat)
        cursor.close()
        conexao.close()

        return categorias

    def adicionar(self, categoria: Categoria) -> None:
        conexao = self.__conexao_factory.get_conexao()
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO categorias (nome) VALUES (%(nome)s)
            """,
                       ({'nome': categoria.nome, }))
        conexao.commit()
        cursor.close()
        conexao.close()

    def remover(self, categoria_id: int) -> bool:
        encontrado = False

        for c in self.__categorias:
            if (c.id == categoria_id):
                index = self.__categorias.index(c)
                self.__categorias.pop(index)
                encontrado = True
                break
        return encontrado

    def buscar_por_id(self, categoria_id) -> Categoria:
        cat = None
        for c in self.__categorias:
            if (c.id == categoria_id):
                cat = c
                break
        return cat

    def ultimo_id(self) -> int:
        index = len(self.__categorias) - 1
        if (index == -1):
            id = 0
        else:
            id = self.__categorias[index].id
        return id
