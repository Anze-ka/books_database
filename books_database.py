''' The program for a bookstore that allows:
t○ add new books to the database,
t○ update book information,
t○ delete books from the database,
t○ search the database to find a specific book.'''

# Importing Libraries
import sqlite3


# Create a database called ebookstore and a table called books.
db = sqlite3.connect('ebookstore.db')
cursor = db.cursor()  # Get a cursor object

cursor.execute('''CREATE TABLE IF NOT EXISTS
                books(id INTEGER PRIMARY KEY, Title TEXT,Author TEXT, Qty INTEGER)
''')
db.commit()


books = [(3001,"A Tale of Two Cities","Charles Dickens",30),
        (3002,"Harry Potter and the Philosopher's Stone","J.K. Rowling",40),
        (3003,"The Lion, the Witch and the Wardrobe","C. S. Lewis",25),
        (3004,"The Lord of the Rings", "J.R.R Tolkien",37),
        (3005,"Alice in Wonderland","Lewis Carroll",12)
        ]
while True:
    # Populate the table with the values from the books list.
    try:
        cursor.executemany(''' INSERT INTO books(id, Title, Author, qty) VALUES(?,?,?,?)''', books)
        db.commit()
    # Catch an error if the data from the books list has already been added into the table.
    except sqlite3.IntegrityError:
        break

# ================ Functions ======================

# - Function that inserts new books to the database.
def add_book():
    
    dash_line = "-"*70
    print("Books in ebookstore")
    print(dash_line)
    # Return all rows in the books table.
    for row in cursor.execute('''SELECT * FROM books'''):
        print(row)
    print(dash_line)

    while True:

        while True:
            try:
                # Request an input of an ID for a new book.
                add_id = int(input("\nPlease enter an ID number for a new book: "))
                break
            # To catch an error when an input is not of an integer type.
            except ValueError:
                print("Input is not recongnized. Please enter a number.")
            
        # Check if the row with the input ID already exists in the books table.
        cursor.execute("SELECT id FROM books WHERE id = ?", (add_id,))
        data=cursor.fetchone()
        # If no rows with the input ID exists, create a new row.
        if data is None:
            # Request an input of all attributes required for a new book.
            add_title = str(input("Please enter the Title of the new book: "))
            add_auth = str(input("Please enter the Author of the new book: "))

            while True:
                try:
                    add_qty = int(input("Please enter the quantity of the new book: "))
                    break
                # To catch an error when an input is not of an integer type.
                except ValueError:
                    print("Not recognized. Please enter a quantity number.\n")

            # Insert a new book into the books table.
            cursor.execute('''INSERT INTO books(id, Title, Author, qty)
                        VALUES(?,?,?,?)''', (add_id,add_title,add_auth,add_qty))
            db.commit()
            print("The book added to the database!")
            break
        # If a row with the input ID exists, request a user to enter a unique ID.
        else:
            print(f"A book with the {add_id} found. Please create a unique ID number.")
    

# - Function that updates book information in the database.
def update_book():
    # Display the books table.
    dash_line = "-"*70
    print("Books in ebookstore")
    print(dash_line)
    # Return all rows in the books table.
    for row in cursor.execute('''SELECT * FROM books'''):
        print(row)
    print(dash_line)

    while True:
        try:
            # Request an input of an ID for the book that should be updated.
            id_select = int(input("Please enter the ID of the book you would like to update:"))
            break
        # To catch an error when an input is not of an integer type.
        except ValueError:
            print("Entry not recongnized. Please enter an ID number.")

    # Display the updated attributes for the book.
    cursor.execute('''SELECT * FROM books WHERE id = ? ''', (id_select,))
    book = cursor.fetchone()
    print(f"\n{book}\n")
    db.commit()

    # Request a Yes/No input to amend the title.
    update_title = str(input("\nWould you like to update the Title? (Yes/No): ")).capitalize()
    if update_title == "Yes":
        # Request an input of a title.
        new_title = str(input("Please enter a title: ")).title()
        # Update the title of the selected book in the books table.
        cursor.execute('''UPDATE books SET Title = ? WHERE id = ?''', (new_title, id_select))
        print("Title updated!")
        db.commit()
        pass
    else:
        pass
    # Request a Yes/No input to amend the author.
    update_auth = str(input("Would you like to update the Author? (Yes/No): ")).capitalize()
    if update_auth == "Yes":
        # Request an input of an author.
        new_auth = str(input("Please enter an author: ")).title()
        # Update the author of the selected book in the books table.
        cursor.execute('''UPDATE books SET Author = ? WHERE id = ?''', (new_auth, id_select))
        print("Author updated!")
        db.commit() 
    else:
        pass
    # Request a Yes/No input to amend the quantity.
    update_qty = str(input("Would you like to update the Quantity? (Yes/No): ")).capitalize()
    if update_qty == "Yes":
        while True:
            try:
                # Request an integer input of a quantity.
                new_qty = int(input("Please enter a quantity:"))
                # Update the quantity value.
                cursor.execute('''UPDATE books SET Qty = ? WHERE id = ?''', (new_qty, id_select))
                print("Quantity updated!")
                db.commit()
                break
            # To catch an error when an input is not of an integer type.    
            except ValueError:
                print("Not recognized. Please enter a quantity number.\n")
        pass 
    else:
        pass
    # Select the updated book.
    cursor.execute('''SELECT * FROM books WHERE id = ? ''', (id_select,))
    book = cursor.fetchone()
    # Display the row with the updated book attributes.
    print(f"\nUPDATED BOOK RECORD:\n{book}")
    db.commit()  

# - Function that deletes books from the database.
def delete_book():
    # Display the books table.
    dash_line = "-"*70
    print("Books in ebookstore")
    print(dash_line)
    # Return all rows in the current books table.
    for row in cursor.execute('''SELECT * FROM books'''):
        print(row)
    print(dash_line)
    # Request an input of an ID for the book that should be deleted from the database.
    id_select = input("Please enter the ID of the book that you would like to delete: ")
    # Delete the row with the specified ID.
    cursor.execute('''DELETE FROM books WHERE id = ? ''', (id_select,))
    print(f"\nThe book ID {id_select} deleted!")
    db.commit()

    # Display the updated books table.
    print("\nUPDATED: Books in ebookstore")
    print(dash_line)
    # Return all rows in the updated books table.
    for row in cursor.execute('''SELECT * FROM books'''):
        print(row)
    print(dash_line)

# - Function that searches the database to find a specific book.
def select_book():
    # Select all ID values from the books table.
    cursor.execute('''SELECT id FROM books''')
    # Display IDs for all books.
    ids = cursor.fetchall()
    print("BOOK ID:")
    print(ids)
 
    while True:
        while True:
            try:
                # Request an input of an id of a book to view.
                id_select = int(input("\nPlease select the ID number of the book you would like to view: "))
                break
            # To catch an error when an input is not of an integer type.
            except ValueError:
                print("Entry not recognized. Please enter an ID number.")

        # Select a row with the input ID and check if it exists in the books table.
        cursor.execute('''SELECT * FROM books WHERE id = ? ''', (id_select,))
        book = cursor.fetchone()
        # If the input ID is not in rows, ask for an input of an ID again.
        if book is None:
            print("Book not found.Please try again.")
        # Display the selected book if its row exists in the table.
        else:
            print(f"\nSELECTED BOOK RECORD:\n{book}")
            break
        db.commit()
       
# ================ Main Menu ======================

while True:
    while True:
        try:
            # Request an input of an integer from the menu.
            menu_choice = int(input('''
******** Bookstore Database *********

Please enter a number from the Menu below:

Database Menu:
\n1. Enter book
2. Update book
3. Delete book
4. Search books
0. Exit

'''))
            break
        # To catch an error when an input is not of an integer type.
        except ValueError:
            print("Oops!Please enter a number from the menu.")

    if menu_choice == 1:           
        add_book()
    elif menu_choice == 2:
        update_book()
    elif menu_choice == 3:
        delete_book()
    elif menu_choice == 4:
        select_book()
    elif menu_choice == 0:
        db.close()
        print("Goodbye!")
        break
    # The statement to account for an input number that is not in the menu.
    else:
        print("Invalid menu option. Please try again.")
