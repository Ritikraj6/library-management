"""Command-line library manager that stores records in library_records.dat.

Run this file with Python to use the numbered menu. This program is separate
from index.html: it uses a local pickle file, while the HTML page uses browser
localStorage.
"""

import pickle
import os

# Name of the binary file used to store the library's book records.
FILE_NAME = "library_records.dat"

def setup_file():
    """Create an empty database file when one does not already exist."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'wb') as file:
            pass

def add_book():
    """Ask for a book's details and append a new record to the database."""
    print("\n--- Add a New Book ---")
    try:
        book_id = input("Enter Book ID: ")
        title = input("Enter Book Title: ")
        author = input("Enter Author Name: ")
        
        # Keep each book's fields together in one dictionary record.
        book = {
            'book_id': book_id,
            'title': title,
            'author': author,
            'status': 'Available',
            'issued_to': ''
        }
        
        with open(FILE_NAME, 'ab') as file:
            pickle.dump(book, file)
            
        print(f"Success: '{title}' added to the library!")
    except Exception as e:
        print(f"Error while adding book: {e}")

def view_all_books():
    """Read and display every book record stored in the database."""
    print("\n--- All Books in Library ---")
    try:
        if os.path.getsize(FILE_NAME) == 0:
            print("The library is currently empty.")
            return

        with open(FILE_NAME, 'rb') as file:
            print(f"{'Book ID':<10} | {'Title':<25} | {'Author':<20} | {'Status':<15} | {'Issued To'}")
            print("-" * 90)
            while True:
                try:
                    book = pickle.load(file)
                    print(f"{book['book_id']:<10} | {book['title']:<25} | {book['author']:<20} | {book['status']:<15} | {book['issued_to']}")
                except EOFError:
                    break
    except FileNotFoundError:
        print("Error: Library database not found.")
    except Exception as e:
        print(f"Error while reading books: {e}")

def search_book():
    """Find a book by ID and display its details, including borrower if issued."""
    print("\n--- Search Book ---")
    search_id = input("Enter Book ID to search: ")
    found = False
    
    try:
        with open(FILE_NAME, 'rb') as file:
            while True:
                try:
                    book = pickle.load(file)
                    if book['book_id'] == search_id:
                        print("\nBook Found!")
                        print(f"Title: {book['title']}")
                        print(f"Author: {book['author']}")
                        print(f"Status: {book['status']}")
                        if book['status'] == 'Issued':
                            print(f"Issued To: {book['issued_to']}")
                        found = True
                        break
                except EOFError:
                    break
        if not found:
            print(f"No book found with ID: {search_id}")
    except Exception as e:
        print(f"Error while searching: {e}")

def update_book():
    """Update the title or author of a book identified by its ID."""
    print("\n--- Update Book Details ---")
    search_id = input("Enter Book ID to update: ")
    books = []
    found = False
    
    try:
        # Load all records because the file must be rewritten to update one.
        with open(FILE_NAME, 'rb') as file:
            while True:
                try:
                    books.append(pickle.load(file))
                except EOFError:
                    break
                    
        # Change only the matching book; blank answers keep the current value.
        for book in books:
            if book['book_id'] == search_id:
                print(f"Current Title: {book['title']}")
                book['title'] = input("Enter New Title (leave blank to keep current): ") or book['title']
                
                print(f"Current Author: {book['author']}")
                book['author'] = input("Enter New Author (leave blank to keep current): ") or book['author']
                
                found = True
                break
                
        if found:
            # Replace the database contents with the updated records.
            with open(FILE_NAME, 'wb') as file:
                for book in books:
                    pickle.dump(book, file)
            print("Book details updated successfully!")
        else:
            print(f"No book found with ID: {search_id}")
            
    except Exception as e:
        print(f"Error while updating: {e}")

def delete_book():
    """Remove the matching book and rewrite the remaining database records."""
    print("\n--- Delete a Book ---")
    search_id = input("Enter Book ID to delete: ")
    books = []
    found = False
    
    try:
        with open(FILE_NAME, 'rb') as file:
            while True:
                try:
                    book = pickle.load(file)
                    if book['book_id'] == search_id:
                        found = True
                    else:
                        books.append(book)
                except EOFError:
                    break
                    
        if found:
            with open(FILE_NAME, 'wb') as file:
                for book in books:
                    pickle.dump(book, file)
            print(f"Book with ID {search_id} has been deleted successfully.")
        else:
            print(f"No book found with ID: {search_id}")
            
    except Exception as e:
        print(f"Error while deleting: {e}")

def issue_book():
    """Issue an available book to a named borrower and save the new status."""
    print("\n--- Issue a Book ---")
    search_id = input("Enter Book ID to issue: ")
    books = []
    found = False
    
    try:
        with open(FILE_NAME, 'rb') as file:
            while True:
                try:
                    books.append(pickle.load(file))
                except EOFError:
                    break
                    
        for book in books:
            if book['book_id'] == search_id:
                found = True
                if book['status'] == 'Available':
                    student_name = input("Enter Name of the person borrowing the book: ")
                    book['status'] = 'Issued'
                    book['issued_to'] = student_name
                    print(f"Success: Book issued to {student_name}.")
                else:
                    print(f"Sorry, this book is already issued to {book['issued_to']}.")
                break
                
        if found:
            with open(FILE_NAME, 'wb') as file:
                for book in books:
                    pickle.dump(book, file)
        else:
            print(f"No book found with ID: {search_id}")
            
    except Exception as e:
        print(f"Error while issuing book: {e}")

def return_book():
    """Mark an issued book as available and clear its borrower name."""
    print("\n--- Return a Book ---")
    search_id = input("Enter Book ID to return: ")
    books = []
    found = False
    
    try:
        with open(FILE_NAME, 'rb') as file:
            while True:
                try:
                    books.append(pickle.load(file))
                except EOFError:
                    break
                    
        for book in books:
            if book['book_id'] == search_id:
                found = True
                if book['status'] == 'Issued':
                    print(f"Book was issued to {book['issued_to']}. Returning it now...")
                    book['status'] = 'Available'
                    book['issued_to'] = ''
                    print("Success: Book returned.")
                else:
                    print("This book is already marked as 'Available'.")
                break
                
        if found:
            with open(FILE_NAME, 'wb') as file:
                for book in books:
                    pickle.dump(book, file)
        else:
            print(f"No book found with ID: {search_id}")
            
    except Exception as e:
        print(f"Error while returning book: {e}")

def main():
    """Create the database, show the menu, and run the selected book action."""
    setup_file()
    while True:
        # Keep showing the menu until the user chooses the exit option.
        print("\n" + "="*40)
        print("      LIBRARY MANAGEMENT SYSTEM      ")
        print("="*40)
        print("1. Add a New Book")
        print("2. View All Books")
        print("3. Search for a Book")
        print("4. Update Book Details")
        print("5. Delete a Book")
        print("6. Issue a Book")
        print("7. Return a Book")
        print("8. Exit")
        print("="*40)
        
        choice = input("Enter your choice (1-8): ")
        
        # Route the user's menu choice to the matching library operation.
        if choice == '1':
            add_book()
        elif choice == '2':
            view_all_books()
        elif choice == '3':
            search_book()
        elif choice == '4':
            update_book()
        elif choice == '5':
            delete_book()
        elif choice == '6':
            issue_book()
        elif choice == '7':
            return_book()
        elif choice == '8':
            print("Thank you for using the Library Management System. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main()
