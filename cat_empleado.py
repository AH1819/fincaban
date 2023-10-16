from connectionDB import DatabaseConnection


class CatEmpleadoModel:
    def __init__(self):
        self.db = DatabaseConnection()

    def fetch_all(self):
        # Crear una instancia de DatabaseConnection
        self.db = DatabaseConnection()

        try:
            with self.db.connection.cursor() as cursor:
                cursor.execute("select "
                               "ce.noemp,"
                               "(ce.nombre||' '||ce.app||' '||ce.apm) as nombre"
                               ", fa.nombre"
                               ", ce.status "
                               "from cat_empleado ce "
                               "inner join finca_install fa "
                               "on fa.nofinca = ce.nofinca "
                               "left join datos_biometricos dbs "
                               "on ce.noemp = dbs.noemp "
                               "where ce.status = 'Activo' and dbs.noemp is null")
                rows = cursor.fetchall()
        except Exception as e:
            print(f"Error al insertar datos: {str(e)}")

        return rows

    def search_emp(self, noemp):
        self.db = DatabaseConnection()
        try:
            consultar = ("SELECT ce.noemp, (ce.nombre||' '||ce.app||' '||ce.apm) as nombre, fa.nombre, ce.status "
                         "FROM cat_empleado ce "
                         "INNER JOIN finca_install fa ON fa.nofinca = ce.nofinca "
                         "INNER JOIN datos_biometricos dbs ON dbs.noemp = ce.noemp "
                         "LEFT JOIN lista_asist la "
                         "ON la.noemp = ce.noemp "
                         "WHERE ce.noemp = %s AND dbs.rostro IS NOT NULL AND ce.status = 'Activo'")
            with self.db.connection.cursor() as cursor:
                cursor.execute(consultar, (noemp,))
                rows = cursor.fetchall()
                return rows
        except Exception as e:
            print(f"Error al consultar datos: {str(e)}")
