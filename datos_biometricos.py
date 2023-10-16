import psycopg2
from connectionDB import DatabaseConnection


class DatosBiometricos:

    def __init__(self):
        self.db = DatabaseConnection()

    def insertar_rostro(self, noemp, foto):
        try:
            with open(foto, "rb") as image_file:
                image_binary = image_file.read()

            insert_query = "INSERT INTO datos_biometricos (noemp, rostro) VALUES (%s, %s)"

            with self.db.connection.cursor() as cursor:
                cursor.execute(insert_query, (noemp, psycopg2.Binary(image_binary)))
                self.db.connection.commit()
                return True
        except Exception as e:
            print(f"Error al insertar datos: {str(e)}")
            return False
