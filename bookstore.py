import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('bookstore.db')
cur = conn.cursor()

# Create the books table
def create_table():
    cur.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        isbn TEXT NOT NULL UNIQUE
    )
    ''')
    conn.commit()

# Add a new book
def add_book(title, author, isbn):
    try:
        cur.execute("INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)", (title, author, isbn))
        conn.commit()
        print("Book added successfully.")
    except sqlite3.IntegrityError:
        print("A book with this ISBN already exists.")

# Remove a book by ID
def remove_book(book_id):
    cur.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    if cur.rowcount == 0:
        print("Book not found.")
    else:
        print("Book removed successfully.")

# Update book details by ID
def update_book(book_id, title, author, isbn):
    cur.execute("UPDATE books SET title = ?, author = ?, isbn = ? WHERE id = ?", (title, author, isbn, book_id))
    conn.commit()
    if cur.rowcount == 0:
        print("Book not found.")
    else:
        print("Book updated successfully.")

# Search for books by title, author, or ISBN
def search_books(keyword):
    cur.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?", 
                (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
    results = cur.fetchall()
    if results:
        for row in results:
            print(f"ID: {row[0]}, Title: {row[1]}, Author: {row[2]}, ISBN: {row[3]}")
    else:
        print("No books found.")

# Display the list of books
def display_books():
    cur.execute("SELECT * FROM books")
    results = cur.fetchall()
    if results:
        for row in results:
            print(f"ID: {row[0]}, Title: {row[1]}, Author: {row[2]}, ISBN: {row[3]}")
    else:
        print("No books in the store.")

# Menu-driven program
def menu():
    create_table()
    while True:
        print("\nBookstore Management System")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Update Book")
        print("4. Search Book")
        print("5. Display All Books")
        print("6. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            isbn = input("Enter book ISBN: ")
            add_book(title, author, isbn)

        elif choice == '2':
            book_id = input("Enter the ID of the book to remove: ")
            remove_book(book_id)

        elif choice == '3':
            book_id = input("Enter the ID of the book to update: ")
            title = input("Enter new title: ")
            author = input("Enter new author: ")
            isbn = input("Enter new ISBN: ")
            update_book(book_id, title, author, isbn)

        elif choice == '4':
            keyword = input("Enter a keyword (title, author, or ISBN) to search: ")
            search_books(keyword)

        elif choice == '5':
            display_books()

        elif choice == '6':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

# Close the connection when done
def close_connection():
    conn.close()

if __name__ == "__main__":
    menu()
    close_connection()
