import os

import psycopg2

class DataBase:
    def __enter__(self):
        self.connector = psycopg2.connect(
            host = os.environ["host"],
            dbname = os.environ["dbname"],
            user = os.environ["user"],
            port = os.environ["port"],
            password = os.environ["password"]
        )
        self.cursor = self.connector.cursor()
        return self

    def __exit__(self, *results):
        self.connector.commit()
        self.connector.close()