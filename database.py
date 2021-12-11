import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE = "musica"
HOST = "localhost"
PASSWORD = "root"
USERNAME = "samue"


def _initialize_cursor(_host, _username, _password, _database):
    connection = psycopg2.connect(host=_host, user=_username, password=_password, dbname=_database)
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    return connection, cursor


def fetch_query(_query):
    connection, cursor = _initialize_cursor(HOST, USERNAME, PASSWORD, DATABASE)
    cursor.execute(_query)
    response = cursor.fetchall()
    cursor.close()
    connection.close()
    return response


def execute_query(_query):
    connection, cursor = _initialize_cursor(HOST, USERNAME, PASSWORD, DATABASE)
    cursor.execute(_query)
    connection.commit()
    cursor.close()
    connection.close()
