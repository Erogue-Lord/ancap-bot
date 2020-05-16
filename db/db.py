import psycopg2
import configparser
from decimal import Decimal

config = configparser.ConfigParser()
config.read('config.ini')
conn = psycopg2.connect(
    host=config['bot_db']['host'],
    user=config['bot_db']['user'],
    password=config['bot_db']['passwd'],
    database=config['bot_db']['database'],
    port=config['bot_db']['port']
)
cursor = conn.cursor()

