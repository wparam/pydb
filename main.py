''' Main module. '''
import os
import sys
import time
from typing import List, Tuple

import pyodbc
from faker import Faker

DB_HOST='0.0.0.0'
DB_PORT='1433'
DB_NAME='tempdb'
DB_USERNAME='sa'
DB_PASSWORD='<YourStrong@Passw0rd>'

CONNECTION_STRING: str = 'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server},{PORT};DATABASE={database};UID={username};PWD={password};'

SQL_CREATE_TABLE: str = '''
    CREATE TABLE users (
        id INT,
        name VARCHAR(50),
        city VARCHAR(50)
    )
'''

SQL_INSERT_DATA: str = 'INSERT INTO users (id, name, city) VALUES (?, ?, ?)'

RECORD_COUNT: int = 10000

def get_data(count: int) -> List[Tuple]:
    ''' Generate user data. '''
    fake = Faker()
    row = lambda n: (n + 1, fake.format('name'), fake.format('city'))

    return [row(i) for i in range(count)]


def connect_db() -> pyodbc.Connection:
    ''' Connect to database. '''
    print('Establishing mssql database connection.')
    connection_str = CONNECTION_STRING.format(
        server=DB_HOST,
        PORT=DB_PORT,
        database=DB_NAME,
        username=DB_USERNAME,
        password=DB_PASSWORD
    )
    print(connection_str)

    return pyodbc.connect(connection_str, timeout=15)


def setup_table(cur: pyodbc.Cursor, data: List):
    ''' Create table and populate data. '''
    print('Create a new table for users.')
    cur.execute(SQL_CREATE_TABLE)
    cur.commit()

    print('Populate users data.')
    for row in data:
        cur.execute(SQL_INSERT_DATA, row)
    cur.commit()


def fetch_data(cur: pyodbc.Cursor) -> List:
    ''' Fetch all data from the table. '''
    print('List of data.')
    cur.execute('SELECT * FROM users')

    return cur.fetchall()


def display_data(rows: List[Tuple[int, str, str]]):
    ''' Print rows in the console. '''
    template = '{:<5} {:<15} {:<10}'
    print(template.format('ID', 'NAME', 'CITY'))
    print('-' * 32)
    for row in rows:
        print(template.format(row.id, row.name, row.city))


def main():
    ''' App entrypoint. '''
    time.sleep(5)  # Wait for mssql database server to fully spawn.
    conn = connect_db()
    cur = conn.cursor()
    data = get_data(RECORD_COUNT)

    setup_table(cur, data)
    rows = fetch_data(cur)
    display_data(rows)

    print('Closing the connection.')
    cur.close()
    conn.close()
    sys.exit(0)

print('Start the app')
main()
