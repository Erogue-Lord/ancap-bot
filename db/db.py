import os

import psycopg2

class DataBase:
    def __init__(self, credentials):
        self.credentials = credentials

    def __enter__(self):
        self.connector = psycopg2.connect(**self.credentials)
        self.cursor = self.connector.cursor()
        return self

    def __exit__(self, *results):
        self.connector.commit()
        self.connector.close()