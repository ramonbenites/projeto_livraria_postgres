import psycopg2


class ConexaoFactory:

    def get_conexao(self):
        return psycopg2.connect(
            host='berry.db.elephantsql.com',
            database='otqstxeh',
            user='otqstxeh',
            password='tuSTkI5QSck6ZWNQCDrFayEoui9Druph'
        )
