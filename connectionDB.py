import psycopg2


class DatabaseConnection:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname="fincaban",
            user="postgres",
            password="AH18192001",
            host="localhost",
            port="5432"
        )

    def close_connection(self):
        self.connection.close()
