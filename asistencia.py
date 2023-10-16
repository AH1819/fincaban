from datetime import datetime
from connectionDB import DatabaseConnection


class AsistenciaDB:
    def __init__(self):
        self.db = DatabaseConnection()

    def validar_registro(self, noemp):
        try:
            consult_query = """
            SELECT * FROM lista_asist WHERE noemp = %s AND hora_sale is null
            """
            with self.db.connection.cursor() as cursor:
                cursor.execute(consult_query, (noemp, ))
                self.db.connection.commit()
                rows = cursor.fetchall()
                if rows:
                    return True
                else:
                    return False

        except Exception as e:
            print(f"Error al consultar datos: {str(e)}")
            return False

    def registrar_asistencia_entrada(self, noemp):
        try:
            fecha_actual = datetime.now().date()
            hora_entra_actual = datetime.now().time()
            insert_query = """
            INSERT INTO lista_asist (noemp, fecha, hora_entra)
            VALUES (%s, %s, %s);
            """
            with self.db.connection.cursor() as cursor:
                cursor.execute(insert_query, (noemp, fecha_actual, hora_entra_actual))
                self.db.connection.commit()
                return True
        except Exception as e:
            print(f"Error al insertar datos: {str(e)}")
            return False

    def registrar_asistencia_salida(self, noemp):
        try:
            fecha_actual = datetime.now().date()
            hora_salida_actual = datetime.now().time()
            insert_query = """
            UPDATE lista_asist SET hora_sale = %s WHERE noemp = %s AND fecha = %s
            """
            with self.db.connection.cursor() as cursor:
                cursor.execute(insert_query, (hora_salida_actual, noemp, fecha_actual))
                self.db.connection.commit()
                return True
        except Exception as e:
            print(f"Error al insertar datos: {str(e)}")
            return False


