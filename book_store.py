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
    # menuOption 0 is the main menu.
    menuOption = 0
    user = {}

    if connection:
        while isRunning:
            if menuOption == 0:
                menuOption = showMainMenu()
            if menuOption == "1":
                user = login(connection)
                if (user is None):
                    menuOption = 0
                else:
                    memberOption = handleMemberOptions(connection)
                    # If the user has entered 1 in the member menu then it puts the user in the main menu
                    # If the user has entered 4 it logs out/exits the program.
                    if memberOption == 1:
                        menuOption = 0
                    if memberOption == 4:
                        isRunning = False
                    

            if menuOption == "2":
                createUser(connection)
                menuOption = 0
            if menuOption == "q":
                isRunning = False


def showMainMenu():
    print("***        Welcome to the online bookstore        ***\n")
    print("1. Member Login\n")
    print("2. New Member Registration\n")
    print("q. Quit\n")

    userInput = input()
    return userInput

def showMemberMenu():
    print("1. Browse by Subject\n")
    print("2. Search by Author\n")
    print("3. Checkout\n")
    print("4. Logout")

    userInput = input()
    return userInput

def handleMemberOptions(connection):
    memberOption = showMemberMenu()

    if memberOption == "4":
        return 4

def login(connection):
    with connection.cursor() as cursor:
        email = input("Enter email: ")
        password = input("Enter password: ")

        loginQuery = f"""SELECT fname, lname, address, city, state, zip, phone, email, userid, password
        FROM members
        WHERE email = \"{email}\" AND password = \"{password}\""""

        cursor.execute(loginQuery)
        user = cursor.fetchone()

        if user is None:
            print("Wrong credentials!")
        else:
            return user


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