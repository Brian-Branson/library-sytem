from data_structures import BinarySearchTree, HashTable, Stack, Queue, CircularLinkedList
from datetime import datetime, timedelta
import json
import os

class LibrarySystem:
    def __init__(self):
        self.books_bst = BinarySearchTree()
        self.members_hash = HashTable()
        self.transaction_stack = Stack()
        self.reservation_queue = Queue()
        self.circulation_history = CircularLinkedList()
        self.current_user = None

        self.load_sample_data()

    def load_sample_data(self):
        # Sample books
        sample_books = [
            {"isbn": "978-0134685991", "title": "Effective Java", "author": "Joshua Bloch", "genre": "Programming", "status": "Available", "copies": 3},
            {"isbn": "978-0135166307", "title": "Clean Code", "author": "Robert Martin", "genre": "Programming", "status": "Available", "copies": 2},
            {"isbn": "978-0596517748", "title": "JavaScript: The Good Parts", "author": "Douglas Crockford", "genre": "Programming", "status": "Borrowed", "copies": 1},
            {"isbn": "978-0321125215", "title": "Domain-Driven Design", "author": "Eric Evans", "genre": "Software Engineering", "status": "Available", "copies": 2},
            {"isbn": "978-0201616224", "title": "The Pragmatic Programmer", "author": "Andy Hunt", "genre": "Programming", "status": "Available", "copies": 4},
            {"isbn": "978-0132350884", "title": "Clean Architecture", "author": "Robert Martin", "genre": "Software Engineering", "status": "Available", "copies": 2},
            {"isbn": "978-0134494166", "title": "Clean Coder", "author": "Robert Martin", "genre": "Professional Development", "status": "Borrowed", "copies": 1},
            {"isbn": "978-0321146533", "title": "Test Driven Development", "author": "Kent Beck", "genre": "Programming", "status": "Available", "copies": 3}
        ]

        for book in sample_books:
            self.books_bst.insert(book)

        # Sample members
        sample_members = [
            {"member_id": "STU001", "name": "Alice Johnson", "email": "alice.j@university.edu", "role": "Student", "books_borrowed": 2, "fine_amount": 0},
            {"member_id": "FAC001", "name": "Dr. Robert Smith", "email": "r.smith@university.edu", "role": "Faculty", "books_borrowed": 5, "fine_amount": 0},
            {"member_id": "STU002", "name": "Bob Wilson", "email": "bob.w@university.edu", "role": "Student", "books_borrowed": 1, "fine_amount": 15.50},
            {"member_id": "STU003", "name": "Carol Davis", "email": "carol.d@university.edu", "role": "Student", "books_borrowed": 0, "fine_amount": 0},
            {"member_id": "FAC002", "name": "Prof. Sarah Lee", "email": "s.lee@university.edu", "role": "Faculty", "books_borrowed": 3, "fine_amount": 0},
            {"member_id": "LIB001", "name": "Michael Chen", "email": "m.chen@university.edu", "role": "Librarian", "books_borrowed": 0, "fine_amount": 0},
            {"member_id": "STU004", "name": "Diana Martinez", "email": "diana.m@university.edu", "role": "Student", "books_borrowed": 4, "fine_amount": 5.00},
            {"member_id": "ADM001", "name": "Admin User", "email": "admin@university.edu", "role": "Administrator", "books_borrowed": 0, "fine_amount": 0}
        ]

        for member in sample_members:
            self.members_hash.insert(member["member_id"], member)

        # Sample transactions
        sample_transactions = [
            {"id": "TXN001", "member_id": "STU001", "book_isbn": "978-0134685991", "type": "Borrow", "date": "2024-01-15", "due_date": "2024-02-15"},
            {"id": "TXN002", "member_id": "FAC001", "book_isbn": "978-0135166307", "type": "Borrow", "date": "2024-01-20", "due_date": "2024-03-20"},
            {"id": "TXN003", "member_id": "STU002", "book_isbn": "978-0596517748", "type": "Borrow", "date": "2024-01-10", "due_date": "2024-02-10"},
            {"id": "TXN004", "member_id": "STU001", "book_isbn": "978-0321125215", "type": "Return", "date": "2024-01-25", "due_date": None},
            {"id": "TXN005", "member_id": "FAC002", "book_isbn": "978-0201616224", "type": "Borrow", "date": "2024-01-22", "due_date": "2024-03-22"}
        ]

        for transaction in sample_transactions:
            self.transaction_stack.push(transaction)
            self.circulation_history.append(transaction)

        # Sample reservations
        sample_reservations = [
            {"member_id": "STU003", "book_isbn": "978-0596517748", "date_requested": "2024-01-25"},
            {"member_id": "STU004", "book_isbn": "978-0134685991", "date_requested": "2024-01-26"}
        ]

        for reservation in sample_reservations:
            self.reservation_queue.enqueue(reservation)

    def search_book(self, isbn):
        """Search for a book by ISBN"""
        return self.books_bst.search(isbn)

    def get_member(self, member_id):
        """Get member information by ID"""
        return self.members_hash.get(member_id)

    def borrow_book(self, member_id, isbn):
        """Borrow a book"""
        book = self.search_book(isbn)
        member = self.get_member(member_id)
        
        if not book:
            return False, "Book not found"
        
        if not member:
            return False, "Member not found"
        
        if book["status"] != "Available":
            return False, "Book is not available"
        
        if book["copies"] <= 0:
            return False, "No copies available"
        
        # Update book status
        book["status"] = "Borrowed"
        book["copies"] -= 1
        
        # Update member
        member["books_borrowed"] += 1
        
        # Create transaction
        transaction = {
            "id": f"TXN{len(self.transaction_stack.items) + 1:03d}",
            "member_id": member_id,
            "book_isbn": isbn,
            "type": "Borrow",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "due_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        }
        
        self.transaction_stack.push(transaction)
        self.circulation_history.append(transaction)
        
        return True, "Book borrowed successfully"

    def return_book(self, member_id, isbn):
        """Return a book"""
        book = self.search_book(isbn)
        member = self.get_member(member_id)
        
        if not book or not member:
            return False, "Book or member not found"
        
        # Update book status
        book["status"] = "Available"
        book["copies"] += 1
        
        # Update member
        member["books_borrowed"] -= 1
        
        # Create return transaction
        transaction = {
            "id": f"TXN{len(self.transaction_stack.items) + 1:03d}",
            "member_id": member_id,
            "book_isbn": isbn,
            "type": "Return",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "due_date": None
        }
        
        self.transaction_stack.push(transaction)
        self.circulation_history.append(transaction)
        
        return True, "Book returned successfully"

    def get_all_books(self):
        """Get all books in the system"""
        return self.books_bst.get_all_books()

    def get_all_members(self):
        """Get all members in the system"""
        return self.members_hash.get_all_members()

    def get_transaction_history(self, limit=10):
        """Get recent transaction history"""
        return self.transaction_stack.get_all()[:limit]

    def get_circulation_history(self, limit=10):
        """Get circulation history"""
        return self.circulation_history.get_circulation_history(limit)

    def get_pending_reservations(self):
        """Get all pending reservations"""
        return self.reservation_queue.get_all()

    def add_book(self, book_data):
        """Add a new book to the system"""
        self.books_bst.insert(book_data)
        return True

    def add_member(self, member_data):
        """Add a new member to the system"""
        self.members_hash.insert(member_data["member_id"], member_data)
        return True

    def authenticate_user(self, member_id, password="default"):
        """Simple authentication (placeholder)"""
        member = self.get_member(member_id)
        if member:
            self.current_user = member
            return True
        return False