from datetime import datetime
from connectionDB import DatabaseConnection


class AsistenciaDB:
    def __init__(self):
        self.db = DatabaseConnection()

    def validar_existencia_registro(self, noemp):  # Válida si el empleado está registrado y si se encuentra activo
        try:
            consult_query = """
            SELECT * FROM cat_empleado WHERE noemp = %s AND status = 'Activo'
            """
            with self.db.connection.cursor() as cursor:
                cursor.execute(consult_query, (noemp,))
                self.db.connection.commit()
                rows = cursor.fetchall()
                if rows:
                    return True
                else:
                    return False

        except Exception as e:
            print(f"Error al consultar datos: {str(e)}")
            return False

    def validar_registro_entrada(self, noemp):  # Válida si ya hay una entrada relacionada con el empleado ese mismo día
        try:
            consult_query = """
            SELECT * FROM lista_asist WHERE noemp = %s AND hora_entra is null
            """
            with self.db.connection.cursor() as cursor:
                cursor.execute(consult_query, (noemp,))
                self.db.connection.commit()
                rows = cursor.fetchall()
                if rows:
                    return True
                else:
                    return False

        except Exception as e:
            print(f"Error al consultar datos: {str(e)}")
            return False

    def validar_registro_salida(self, noemp):  # Válida si ya hay una salida relacionada con el empleado ese mismo día
        try:
            consult_query = """
            SELECT * FROM lista_asist WHERE noemp = %s AND hora_sale IS NULL AND hora_entra IS NOT NULL
            """
            with self.db.connection.cursor() as cursor:
                cursor.execute(consult_query, (noemp,))
                self.db.connection.commit()
                rows = cursor.fetchall()
                return rows
        except Exception as e:
            print(f"Error al consultar datos: {str(e)}")
            return False

    def registrar_asistencia_entrada(self, noemp):  # Se registra la entrada
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

    def registrar_asistencia_salida(self, noemp):  # Se registra la salida
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

    def getAsistencia(self):  # Recupera los registros hasta el momento
        try:
            consult_query = """
            SELECT ce.noemp, (ce.nombre ||' '|| ce.app ||''|| ce.apm) as nombre, la.hora_entra, la.hora_sale
            FROM cat_empleado ce 
            INNER JOIN lista_asist la 
            ON la.noemp = ce.noemp
            """
            with self.db.connection.cursor() as cursor:
                cursor.execute(consult_query)
                self.db.connection.commit()
                rows = cursor.fetchall()
                if rows:
                    return rows
                else:
                    return False

        except Exception as e:
            print(f"Error al consultar datos: {str(e)}")
            return False


if __name__ == "__main__":
    ast = AsistenciaDB()
    print(ast.validar_existencia_registro('VR-2023-00001'))
    print(ast.validar_registro_entrada('VR-2023-00001'))
