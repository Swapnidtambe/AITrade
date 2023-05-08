import mysql.connector


class Database:
    def __init__(self, host, username, password, database_name):
        self.host = host
        self.username = username
        self.password = password
        self.database_name = database_name
        self.connection = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            database=self.database_name
        )

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def execute(self, query, values=None):
        cursor = self.connection.cursor()
        cursor.execute(query, values)
        self.connection.commit()
        return cursor.lastrowid
