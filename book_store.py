from mysql.connector import connect, Error
from getpass import getpass


def connectToDatabase():
    try:
        connection = connect(
            host="localhost",
            user=input("Enter username: "),
            password=getpass("Enter password: "),
            database="book_store"
        )
    except Error as e:
        print(e)
        return None
    return connection

def main():
    isRunning = True
    connection = connectToDatabase()
    menuOption = 0

    if connection:
        while isRunning:
            if menuOption == 0:
                menuOption = showMainMenu()
            if menuOption == "1":
                print(menuOption)
            if menuOption == "2":
                createUser(connection)
                menuOption = 0
            if menuOption == "q":
                isRunning = False

    # if connection:
    #     testConnection(connection)


# def testConnection(connection):
#     with connection.cursor() as cursor:
#         bookQuery = "SELECT * FROM books"
#         cursor.execute(bookQuery)
#         result = cursor.fetchall()
#         for row in result:
#             print(row)


def showMainMenu():
    print("***        Welcome to the online bookstore        ***\n")
    print("1. Member Login\n")
    print("2. New Member Registration\n")
    print("q. Quit\n")

    userInput = input()
    return userInput

def createUser(connection):
    print("Welcome to the Online Book store\n")
    print("New Member Registration")
    
    firstName = input("Enter first name: ")
    lastName = input("Enter last name: ")
    streetAddress = input("Enter street address: ")
    city = input("Enter city: ")
    state = input("Enter state: ")
    zipCode = input("Enter zip: ")
    phoneNumber = input("Enter phone: ")
    email = input("Enter email: ")
    password = input("Enter password: ")

    createMemberQuery = f"""
     INSERT INTO members
    (fname, lname, address, city, state, zip, phone, email, password)
    VALUES
    ("{firstName}", "{lastName}", "{streetAddress}", "{city}", "{state}",
    {zipCode}, "{phoneNumber}", "{email}", "{password}")
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute(createMemberQuery)
            connection.commit()
            print("You have registered successfully!")
    except Error as e:
        print("You have not been registered.\n")
        print(e)

main()