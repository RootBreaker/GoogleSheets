import psycopg2
from config import host, user, password, db_name, port


# connect to exist database
connection = psycopg2.connect(
    database=db_name,
    user=user,
    password=password,
    host=host,
    port=port
)

connection.autocommit = True


def getvaluesfromlist1():
    with connection.cursor() as cursor:
        cursor.execute("SELECT (№, order_number, price_dollars, delivery_time) FROM list1;")
        return cursor.fetchall()


def getvaluesfromlist2():
    with connection.cursor() as cursor:
        cursor.execute("SELECT (№, order_number, price_dollars, delivery_time) FROM list2;")
        return cursor.fetchall()


def getdollars():
    with connection.cursor() as cursor:
        cursor.execute("SELECT (price_dollars) FROM list1")
        return cursor.fetchall()
