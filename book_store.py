from mysql.connector import connect, Error
from getpass import getpass


def connectToDatabase():
    try:
        connection = connect(
            host="localhost",
            user="root",
            password="42s744ro",
            database="book_store"
        )
    except Error as e:
        print(e)
        return None
    return connection

def main():
    connection = connectToDatabase()
    if connection:
        testConnection(connection)


def testConnection(connection):
    with connection.cursor() as cursor:
        bookQuery = "SELECT * FROM books"
        cursor.execute(bookQuery)
        result = cursor.fetchall()
        for row in result:
            print(row)

main()