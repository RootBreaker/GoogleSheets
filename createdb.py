import psycopg2
from config import host, user, password, port, db_name


def create_tables():
    connection = psycopg2.connect(
        database="postgres",
        user=user,
        password=password,
        host=host,
        port=port
    )
    connection.autocommit = True

    cursor = connection.cursor()
    # check if database exists
    cursor.execute("SELECT COUNT(*) = 0 FROM pg_catalog.pg_database WHERE datname = 'googlesheets'")
    not_exists, = cursor.fetchone()
    if not_exists:
        cursor.execute('CREATE DATABASE googlesheets')
    connection.close()

    # connect to googlesheets database
    connection = psycopg2.connect(
        database=db_name,
        user=user,
        password=password,
        host=host,
        port=port
    )
    connection.autocommit = True

    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE list1(
                   № integer primary key,
                   order_number integer,
                   price_dollars char(15),
                   delivery_time date,
                   price_rubles char(20)
                   )"""
                   )

    cursor.execute("""CREATE TABLE list2(
                   № integer primary key,
                   order_number integer,
                   price_dollars char(15),
                   delivery_time date,
                   price_rubles char(20)
                   )"""
                   )


create_tables()
