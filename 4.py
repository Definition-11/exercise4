import sqlite3


def create_database():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    # Create Books table
    c.execute('''  
        CREATE TABLE Books (  
            BookID TEXT PRIMARY KEY,  
            Title TEXT,  
            Author TEXT,  
            ISBN TEXT,  
            Status TEXT  
        )  
    ''')

    # Create Users table
    c.execute('''  
        CREATE TABLE Users (  
            UserID TEXT PRIMARY KEY,  
            Name TEXT,  
            Email TEXT  
        )  
    ''')

    # Create Reservations table
    c.execute('''  
        CREATE TABLE Reservations (  
            ReservationID TEXT PRIMARY KEY,  
            BookID TEXT,  
            UserID TEXT,  
            ReservationDate DATE,  
            FOREIGN KEY (BookID) REFERENCES Books(BookID),  
            FOREIGN KEY (UserID) REFERENCES Users(UserID)  
        )  
    ''')

    conn.commit()
    conn.close()


def add_book(conn):
    book_data = input("Enter book details (format: BookID Title Author ISBN Status): ")
    book_data = book_data.split()
    try:
        conn.execute('''  
            INSERT INTO Books (BookID, Title, Author, ISBN, Status)   
            VALUES (?, ?, ?, ?, ?)  
        ''', (book_data[0], book_data[1], book_data[2], book_data[3], book_data[4]))
        conn.commit()
        print("Book added successfully.")
    except Exception as e:
        print("Error adding book:", e)
        conn.rollback()


def find_book(conn):
    book_id = input("Enter book ID: ")
    try:
        c = conn.cursor()
        c.execute(f"SELECT * FROM Books WHERE BookID = ?", (book_id,))
        book = c.fetchone()
        if book is None:
            print("Book not found.")
            return
        print("Book found:")
        print(f"BookID: {book[0]}")
        print(f"Title: {book[1]}")
        print(f"Author: {book[2]}")
        print(f"ISBN: {book[3]}")
        print(f"Status: {book[4]}")
    except Exception as e:
        print("No Book Found with the Given ID", e)


# Finding Book Reservation Status
def find_book_reservation_status(text):
    if text.startswith("LB"):  # If the Text is BookID
        c.execute("""SELECT Books.Status, Users.Name, Users.Email, Reservations.ReservationDate
                        FROM Books
                        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                        LEFT JOIN Users ON Reservations.UserID = Users.UserID 
                        WHERE Books.BookID = ?""", (text,))
    elif text.startswith("LU"):  # If the Text is UserID
        c.execute("""SELECT Books.Title, Books.Status, Reservations.ReservationDate
                        FROM Books
                        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                        WHERE Reservations.UserID = ?""", (text,))
    elif text.startswith("LR"):  # If the Text is ReservationID
        c.execute("""SELECT Books.Title, Books.Status, Users.Name, Users.Email, Reservations.ReservationDate
                        FROM Books
                        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                        LEFT JOIN Users ON Reservations.UserID = Users.UserID 
                        WHERE Reservations.ReservationID = ?""", (text,))
    else:  # If the Text is Title
        c.execute("""SELECT Books.BookID, Books.Isbn, Books.Status, Users.Name, Users.Email, Reservations.ReservationDate
                        FROM Books
                        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                        LEFT JOIN Users ON Reservations.UserID = Users.UserID 
                        WHERE Books.Title = ?""", (text,))
    book_details = c.fetchone()
    if book_details:
        if text.startswith("LB") or text.startswith("LR") or text:  # If the Text is BookID, ReservationID or Title
            print("Book ID:", book_details[0])
            print("Book ISBN:", book_details[1])
            print("Book Status:", book_details[2])
        elif text.startswith("LU"):  # If the Text is UserID
            print("Book Title:", book_details[0])
            print("Book Status:", book_details[1])
            print("Reservation Date:", book_details[2])
        if book_details[3]:
            print("Reserved By:", book_details[3])
            print("Reserved By Email:", book_details[4])
            print("Reservation Date:", book_details[5])
    else:
        print("No Record Found with the Given Text!")


# Finding All the Books
def find_all_books():
    cur.execute("""SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status, Users.Name, Users.Email, Reservations.ReservationDate
                    FROM Books
                    LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                    LEFT JOIN Users ON Reservations.UserID = Users.UserID""")
    all_books = cur.fetchall()
    if all_books:
        for book in all_books:
            print("Book ID:", book[0])
            print("Book Title:", book[1])
            print("Book Author:", book[2])
            print("Book ISBN:", book[3])
            print("Book Status:", book[4])
            if book[5]:
                print("Reserved By:", book[5])
                print("Reserved By Email:", book[6])
                print("Reservation Date:", book[7])
            print("\n")
    else:
        print("No Books Found in the Database!")


# Updating Book Details
def modify_book_details(book_id, status):
    cur.execute("""UPDATE Books SET Status = ? WHERE BookID = ?""", (status, book_id))
    cur.execute("""UPDATE Reservations SET ReservationDate = NULL WHERE BookID = ?""", (book_id,))
    conn.commit()
    print("Book Details Updated Successfully!")


# Deleting Book from the Database
def delete_book(book_id):
    cur.execute("""SELECT * FROM Reservations WHERE BookID = ?""", (book_id,))
    if cur.fetchone():
        cur.execute("""DELETE FROM Reservations WHERE BookID = ?""", (book_id,))
        cur.execute("""DELETE FROM Books WHERE BookID = ?""", (book_id,))
        conn.commit()
        print("Book and Associated Reservation Deleted Successfully!")
    else:
        cur.execute("""DELETE FROM Books WHERE BookID = ?""", (book_id,))
        conn.commit()
        print("Book Deleted Successfully!")


# Running the Program
while True:
    print("\nWelcome to the Library Management System!\n")
    print("1. Add a New Book to the Database")
    print("2. Find a Book Details Based on BookID")
    print("3. Find a Book Reservation Status Based on the BookID, Title, UserID or ReservationID")
    print("4. Find All the Books")
    print("5. Modify / Update Book Details Based on its BookID")
    print("6. Delete a Book Based on its BookID")
    print("7. Exit")
    choice = int(input("\nEnter Your Choice: "))
    if choice == 1:
        title = input("Enter the Book Title: ")
        author = input("Enter the Book Author: ")
        isbn = input("Enter the Book ISBN: ")
        status = input("Enter the Book Status: ")
        add_book(title, author, isbn, status)
    elif choice == 2:
        book_id = int(input("Enter the Book ID: "))
        find_book_details(book_id)
    elif choice == 3:
        text = input("Enter the Book ID, Title, UserID or ReservationID: ")
        find_book_reservation_status(text.upper())
    elif choice == 4:
        find_all_books()
    elif choice == 5:
        book_id = int(input("Enter the Book ID: "))
        status = input("Enter the Book Status: ")
        modify_book_details(book_id, status)
    elif choice == 6:
        book_id = int(input("Enter the Book ID: "))
        delete_book(book_id)
    elif choice == 7:
        print("Thank You For Using the Library Management System!")
        break
    else:
        print("Invalid Choice! Choose Again.")