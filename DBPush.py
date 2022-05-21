import psycopg2
from config import host, user, password, db_name, port


try:
    # connect to exist database
    connection = psycopg2.connect(
        database=db_name,
        user=user,
        password=password,
        host=host,
        port=port
    )

    connection.autocommit = True
    # cursor for perfoming database operations

    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         "SELECT version();"
    #     )
    #
    #     print(f"Server version: {cursor.fetchone()}")

    #insert data into table
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """INSERT INTO list1 (order_number, price_dollars, delivery_time) VALUES (1182407, 214, '13.05.2022')"""
    #     )
    #
    #     print ("[INFO] Data was succesfully inserted")

    #get data from table
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT * from list1;"""
        )
        print(cursor.fetchone())

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print("[INFO] PostgreSQL connection closed")