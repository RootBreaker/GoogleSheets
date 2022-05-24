import gspread
import psycopg2
import dbpush
from config import host, user, password, db_name, port
from get_dollar_exchange_rate import get_dollar as gd


# get data from google sheets
serviceAccount = gspread.service_account(filename="service_account.json")
sheet = serviceAccount.open("table")
worksheet = sheet.worksheet("List1")
values = worksheet.get('A2:D50')

# for row in values:
#     print('%s, %s, %s, %s' % (row[0], row[1], row[2], row[3]))

print(values)
# connect to database
connection = psycopg2.connect(
    database=db_name,
    user=user,
    password=password,
    host=host,
    port=port
)

connection.autocommit = True

with connection.cursor() as cursor:
    cursor.execute("DELETE FROM list2")
    connection.commit()


# insert to list2 (only for comparing)
with connection.cursor() as cursor:
    for row in values:
        cursor.execute("INSERT INTO list2 (№, order_number, price_dollars, delivery_time) VALUES (%s, %s, %s, %s)",
                       (row[0], row[1], row[2], row[3]))
    connection.commit()

valueslist1 = []
valuesList1 = dbpush.getvaluesfromlist1()
print(valuesList1)

valueslist2 = []
valuesList2 = dbpush.getvaluesfromlist2()
print(valuesList2)


res = [x for x in valueslist1 + valuesList2 if x not in valuesList1 or x not in valueslist2]

if not res:
    print("Normalin Normalin")
else:
    with connection.cursor() as cursor:
        for row in values:
            cursor.execute("DELETE FROM list1")
            connection.commit()

    with connection.cursor() as cursor:
        for row in values:
            cursor.execute("INSERT INTO list1 (№, order_number, price_dollars, delivery_time) VALUES (%s, %s, %s, %s)",
                           (row[0], row[1], row[2], row[3]))
            connection.commit()

pricelistdollars = []
for row in values:
    pricelistdollars.append(row[2])

dollar_rate = int(gd())
pricelistrubles = [int(num) * dollar_rate for num in pricelistdollars]


print(pricelistdollars)
print(pricelistrubles)

# insert to list1
# with connection.cursor() as cursor:
#     for row in values:
#         cursor.execute("INSERT INTO list1 (№, order_number, price_dollars, delivery_time) VALUES (%s, %s, %s, %s)",
#                        (row[0], row[1], row[2], row[3]))
#     connection.commit()


print("[INFO] Data was succesfully inserted")
