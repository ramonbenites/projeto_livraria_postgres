from model.livro import Livro
from database.conexao_factory import ConexaoFactory
from dao.categoria_dao import CategoriaDAO
from dao.editora_dao import EditoraDAO
from dao.autor_dao import AutorDAO


class LivroDAO:

    def __init__(self, categoria_dao: CategoriaDAO, editora_dao: EditoraDAO, autor_dao: AutorDAO):
        self.__conexao_factory: ConexaoFactory = ConexaoFactory()
        self.__categoria_dao: CategoriaDAO = categoria_dao
        self.__editora_dao: EditoraDAO = editora_dao
        self.__autor_dao: AutorDAO = autor_dao

    def listar(self) -> list[Livro]:
        livros = list()

        conexao = self.__conexao_factory.get_conexao()
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT id, titulo, resumo, ano, paginas, isbn, categoria_id, editora_id, autor_id FROM livros")
        resultados = cursor.fetchall()
        for resultado in resultados:
            categoria = self.__categoria_dao.buscar_por_id(resultado[6])
            editora = self.__editora_dao.buscar_por_id(resultado[7])
            autor = self.__autor_dao.buscar_por_id(resultado[8])

            liv = Livro(resultado[1], resultado[2],
                        int(resultado[3]), int(resultado[4]), resultado[5], categoria, editora, autor)
            liv.id = resultado[0]
            livros.append(liv)
        cursor.close()
        conexao.close()

        return livros

    def adicionar(self, livro: Livro) -> None:
        conexao = self.__conexao_factory.get_conexao()
        cursor = conexao.cursor()
        cursor.execute("""
                        INSERT INTO livros 
                            (titulo, resumo, ano, paginas, isbn, categoria_id, editora_id, autor_id)
                        VALUES
                            (%(titulo)s, %(resumo)s, %(ano)s, %(paginas)s, %(isbn)s, %(categoria_id)s, 
                            %(editora_id)s, %(autor_id)s)
                        """,
                       ({'titulo': livro.titulo, 'resumo': livro.resumo, 'ano': livro.ano,
                         'paginas': livro.paginas, 'isbn': livro.isbn, 'categoria_id': livro.categoria.id,
                         'editora_id': livro.editora.id, 'autor_id': livro.autor.id}))
        conexao.commit()
        cursor.close()
        conexao.close()

    def remover(self, livro_id: int) -> bool:
        conexao = self.__conexao_factory.get_conexao()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM livros WHERE id = %s", (livro_id,))
        livros_removidos = cursor.rowcount
        conexao.commit()
        cursor.close()
        conexao.close()

        if (livros_removidos == 0):
            return False
        return True

    def buscar_por_id(self, livro_id) -> Livro:
        liv = None
        conexao = self.__conexao_factory.get_conexao()
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT id, titulo, resumo, ano, paginas, isbn, categoria_id, editora_id, autor_id "
            "FROM livros WHERE id = %s", (livro_id,))
        resultado = cursor.fetchone()
        if (resultado):
            categoria = self.__categoria_dao.buscar_por_id(resultado[6])
            editora = self.__editora_dao.buscar_por_id(resultado[7])
            autor = self.__autor_dao.buscar_por_id(resultado[8])

            liv = Livro(resultado[1], resultado[2],
                        int(resultado[3]), int(resultado[4]), resultado[5], categoria, editora, autor)
            liv.id = resultado[0]
        cursor.close()
        conexao.close()

        return liv
