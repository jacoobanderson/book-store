from mysql.connector import connect, Error
from datetime import datetime, timedelta
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
                    memberOption = handleMemberOptions(connection, user)
                    menuOption = 0
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
    print("2. Search by Author/Title\n")
    print("3. Checkout\n")
    print("4. Logout")

    userInput = input()
    return userInput

def handleMemberOptions(connection, user):
    memberOption = showMemberMenu()
    if memberOption == "1":
        browseBySubject(connection, user)
        handleMemberOptions(connection, user)
    if memberOption == "2":
        searchByAuthorOrTitle(connection, user)
        handleMemberOptions(connection, user)
    if memberOption == "3":
        checkOut(connection, user)
    if memberOption == "4":
        return 4
    
def getCart(connection, userId):
    with connection.cursor() as cursor:
        cartQuery = f"""SELECT isbn, qty FROM cart WHERE userid = {userId}"""
        cursor.execute(cartQuery)
        cart = cursor.fetchall()
        return cart

def getPriceAndTitleByIsbn(connection, isbn):
    with connection.cursor() as cursor:
        query = f"""SELECT title, price FROM books WHERE isbn = {isbn}"""
        cursor.execute(query)
        books = cursor.fetchone()
        return books
    
def checkOut(connection, user):
    userId = user[8]
    currentCart = getCart(connection, userId)

    print("Current cart contents: \n")
    print("ISBN         Title                                                                           Qty     Total")
    print("----------------------------------------------------------------------------------------------------------")

    totalPrice = 0
    for book in currentCart:
        fixed_width = 40
        priceAndTitle = getPriceAndTitleByIsbn(connection, book[0])
        totalPrice += priceAndTitle[1] * book[1]
        title = priceAndTitle[0]
        print(str(book[0]) + "       " + f"{title:{fixed_width}}" + "                                      " + str(book[1]) + "    " + str(book[1] * priceAndTitle[1]))
        print("----------------------------------------------------------------------------------------------------------")

    print("Total                                                                                            " + "$" + str(totalPrice))
    print("----------------------------------------------------------------------------------------------------------")
    correctInput = False
    while correctInput == False:
        proceedInput = input("\nProceed to check out (Y/N)?: ")
        if proceedInput.lower() == "y":
            addOrder(connection, user)
            handleMemberOptions(connection, user)
            correctInput = True
        if proceedInput.lower() == "n":
            handleMemberOptions(connection, user)
            correctInput = True

    
def addOrder(connection, user):
    date = datetime.date(datetime.today())
    dateInOneWeek = datetime.date(datetime.today() + timedelta(days=7))
    city = user[3]
    state = user[4]
    address = user[2]
    userId = user[8]
    zip = user[5]

    with connection.cursor() as cursor:
        addOrderQuery = f"""INSERT INTO orders (userid, recieved, shipped, shipAdress, shipCity, shipState, shipZip)
        VALUES ({userId}, \"{date}\", \"{dateInOneWeek}\", \"{address}\", \"{city}\", \"{state}\", \"{zip}\")"""
        cursor.execute(addOrderQuery)
        connection.commit()
    
    addOdetails(connection, user)

def showInvoice(connection, user, ono):
    city = user[3]
    state = user[4]
    address = user[2]
    zip = user[5]

    print(f"Invoice for Order no.{ono}")
    print("Shipping Address")
    print("Name: " + user[0] + " " + user[1])
    print(f"Address: {address}\n         {city}\n         {state} {zip}")


    userId = user[8]
    currentCart = getCart(connection, userId)
    print("ISBN         Title                                                                           Qty     Total")
    print("----------------------------------------------------------------------------------------------------------")

    totalPrice = 0
    for book in currentCart:
        fixed_width = 40
        priceAndTitle = getPriceAndTitleByIsbn(connection, book[0])
        totalPrice += priceAndTitle[1] * book[1]
        title = priceAndTitle[0]
        print(str(book[0]) + "       " + f"{title:{fixed_width}}" + "                                      " + str(book[1]) + "    " + str(book[1] * priceAndTitle[1]))
        print("----------------------------------------------------------------------------------------------------------")

    print("Total                                                                                            " + "$" + str(totalPrice))
    print("----------------------------------------------------------------------------------------------------------")

    emptyCart(connection, user)
    print("\n Press enter to go back to menu")
    while input() != "":
        print("Press enter to go back to menu")

def addOdetails(connection, user):
    # Get ono from order
    userId = user[8]
    currentCart = getCart(connection, userId)

    with connection.cursor() as cursor:
        onoQuery = f"SELECT ono FROM orders WHERE userid = {userId}"
        cursor.execute(onoQuery)
        userOnos = cursor.fetchall()
        ono = userOnos[0][0]

        for book in currentCart:
            priceAndTitle = getPriceAndTitleByIsbn(connection, book[0])
            qty = book[1]
            isbn = book[0]

            odetailsQuery = "INSERT INTO odetails (ono, isbn, qty, price) VALUES (%s, %s, %s, %s)"
            price = float(priceAndTitle[1]) * qty
            values = (ono, isbn, qty, price)
            cursor.execute(odetailsQuery, values)
            connection.commit()
        
        showInvoice(connection, user, ono)

def emptyCart(connection, user):
    with connection.cursor() as cursor:
        emptyCartQuery = f"DELETE FROM cart WHERE userid = {user[8]}"
        cursor.execute(emptyCartQuery)
        connection.commit()
    
def browseBySubject(connection, user):
    userId = user[8]
    subjects = getSubject(connection)
    showSubjectChoice(subjects)
    userInput = int(input())
    chosenSubject = subjects[userInput][0]
    books = getBooksBySubject(connection, chosenSubject)
    showBooksWithOptions(connection, userId, books)

def searchByAuthorOrTitle(connection, user):
    print("\n1. Author Search")
    print("2. Title Search")
    print("3. Go back to Member Menu\n")

    userId = user[8]
    userInput = int(input())

    if userInput == 1:
        authorSearch = input("Enter author or part of the author's name: ")
        authorBooks = getBooksByAuthor(connection, authorSearch)
        showBooksWithOptions(connection, userId, authorBooks)
    if userInput == 2:
        titleSearch = input("Enter title or part of the title: ")
        titleBooks = getBooksByTitle(connection, titleSearch)
        showBooksWithOptions(connection, userId, titleBooks)
    if userInput == 3:
        handleMemberOptions(connection, user)


def showBooksWithOptions(connection, userId, books):
    print(str(len(books)) + " books available on this search.\n")

    i = 0
    while i < len(books):
        print("Author: " + books[i][0])
        print("Title: " + books[i][1])
        print("ISBN: " + books[i][2])
        print("Price: " + str(books[i][3]))
        print("Subject: " + books[i][4] + "\n")

        if i != len(books) - 1:
            print("Author: " + books[i+1][0])
            print("Title: " + books[i+1][1])
            print("ISBN: " + books[i+1][2])
            print("Price: " + str(books[i+1][3]))
            print("Subject: " + books[i+1][4] + "\n")

        userInput = input("Enter ISBN to add to cart or n Enter to browse or ENTER to go back to menu: ")

        if userInput == 'n':
            i += 2
        elif userInput == "":
            return
        else:
            addToCart(connection, userId, userInput)
            break



def getBooksByAuthor(connection, author):
    with connection.cursor() as cursor:
        query = f"""SELECT author, title, isbn, price, subject FROM books WHERE author LIKE \"%{author}%\""""
        cursor.execute(query)
        books = cursor.fetchall()
        return books
    
def getBooksByTitle(connection, title):
    with connection.cursor() as cursor:
        query = f"""SELECT author, title, isbn, price, subject FROM books WHERE title LIKE \"%{title}%\""""
        cursor.execute(query)
        books = cursor.fetchall()
        return books


def addToCart(connection, userId, isbn):
    with connection.cursor() as cursor:
        # check if book exists
        checkIfBookExistsQuery = f"""SELECT 1 FROM books WHERE isbn = {isbn}"""
        cursor.execute(checkIfBookExistsQuery)
        book = cursor.fetchone()
        
        if (book is not None):
            quantityOfBooks = input("Enter quantity: ")
            addToCartQuery = f"""INSERT INTO cart (userid, isbn, qty) VALUES ({userId}, {isbn}, {quantityOfBooks})"""
            cursor.execute(addToCartQuery)
            connection.commit()
        else:
            print("Book with that ISBN does not exist.")
    
def getBooksBySubject(connection, subject):
    with connection.cursor() as cursor:
        query = f"""SELECT author, title, isbn, price, subject FROM books WHERE subject = \"{subject}\""""
        cursor.execute(query)
        books = cursor.fetchall()
        return books

def getSubject(connection):
    with connection.cursor() as cursor:
        subjectQuery = """SELECT DISTINCT subject FROM books ORDER BY subject"""
        cursor.execute(subjectQuery)
        subjects = cursor.fetchall()
        return subjects

def showSubjectChoice(subjects):
    for count, subject in enumerate(subjects):
        print(str(count + 1) + ". " + str(subject[0]))

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