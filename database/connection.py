import pymysql

class ConnectionBD:
    host = 'localhost'
    user = 'root'
    password = ''
    database = 'TA2-POO'
    connection = None

    def conectar(self):
        try:
            if not ConnectionBD.connection:
                ConnectionBD.connection = pymysql.connect(
                    host=ConnectionBD.host,
                    user=ConnectionBD.user,
                    password=ConnectionBD.password,
                    database=ConnectionBD.database
                )
            return ConnectionBD.connection
        except pymysql.Error as e:
            raise e

    def desconectar(self):
        if ConnectionBD.connection and ConnectionBD.connection.open:
            try:
                ConnectionBD.connection.close()
                return True
            except pymysql.Error as e:
                raise e
        else:
            return False

    def ejecutar_consulta(self, query):
        try:
            with self.conectar() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    result = cursor.fetchall()
                    return result
        except pymysql.Error as e:
            raise e
