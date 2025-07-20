from datetime import datetime, timedelta
import copy

class InMemoryDatabaseManager:
    def __init__(self):
        self.books = {}
        self.members = {}
        self.transactions = []
        self.insert_sample_data()

    def insert_sample_data(self):
        sample_books = [
            {"id": "B001", "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "isbn": "978-0-7432-7356-5",
             "genre": "Fiction", "status": "Available", "copies": 3, "available_copies": 2, "publish_year": 1925,
             "pages": 180, "rating": 4.2, "description": "Classic American novel"},
            {"id": "B002", "title": "Python Programming", "author": "John Smith", "isbn": "978-1-4919-5713-7",
             "genre": "Technology", "status": "Borrowed", "copies": 2, "available_copies": 0, "publish_year": 2023,
             "pages": 456, "rating": 4.8, "description": "Comprehensive Python guide"},
            {"id": "B003", "title": "Data Structures", "author": "Robert Sedgewick", "isbn": "978-0-321-57351-3",
             "genre": "Computer Science", "status": "Available", "copies": 4, "available_copies": 3, "publish_year": 2011,
             "pages": 955, "rating": 4.6, "description": "Algorithms textbook"},
            {"id": "B004", "title": "Effective Java", "author": "Joshua Bloch", "isbn": "978-0134685991",
             "genre": "Programming", "status": "Available", "copies": 3, "available_copies": 3, "publish_year": 2018,
             "pages": 412, "rating": 4.7, "description": "Java best practices"},
            {"id": "B005", "title": "Clean Code", "author": "Robert Martin", "isbn": "978-0135166307",
             "genre": "Programming", "status": "Available", "copies": 2, "available_copies": 2, "publish_year": 2008,
             "pages": 464, "rating": 4.5, "description": "Writing clean code principles"},
        ]
        sample_members = [
            {"member_id": "STU001", "name": "Alice Johnson", "email": "alice@university.edu", "role": "Student",
             "books_borrowed": 2, "fine_amount": 0, "password": "alice123"},
            {"member_id": "FAC001", "name": "Dr. Robert Smith", "email": "robert@university.edu", "role": "Faculty",
             "books_borrowed": 1, "fine_amount": 0, "password": "robert123"},
            {"member_id": "LIB001", "name": "Sarah Wilson", "email": "sarah@university.edu", "role": "Librarian",
             "books_borrowed": 0, "fine_amount": 0, "password": "sarah123"},
            {"member_id": "ADM001", "name": "Admin User", "email": "admin@university.edu", "role": "Administrator",
             "books_borrowed": 0, "fine_amount": 0, "password": "admin123"},
            {"member_id": "STU002", "name": "Bob Wilson", "email": "bob@university.edu", "role": "Student",
             "books_borrowed": 1, "fine_amount": 15.5, "password": "bob123"},
        ]

        for book in sample_books:
            self.books[book["isbn"]] = book
        for member in sample_members:
            self.members[member["member_id"]] = member

    def authenticate_user(self, member_id, password):
        member = self.members.get(member_id)
        if member and member["password"] == password:
            return copy.deepcopy(member)
        return None

    def get_all_books(self):
        return sorted([copy.deepcopy(book) for book in self.books.values()], key=lambda x: x["title"])

    def get_all_members(self):
        return sorted([copy.deepcopy(member) for member in self.members.values()], key=lambda x: x["name"])

    def search_books(self, search_term, search_type='title'):
        search_term = search_term.lower()
        results = []
        for book in self.books.values():
            if search_type == 'title' and search_term in book['title'].lower():
                results.append(copy.deepcopy(book))
            elif search_type == 'author' and search_term in book['author'].lower():
                results.append(copy.deepcopy(book))
            elif search_type == 'isbn' and search_term in book['isbn'].lower():
                results.append(copy.deepcopy(book))
            elif search_type == 'all':
                if (search_term in book['title'].lower() or
                    search_term in book['author'].lower() or
                    search_term in book['isbn'].lower()):
                    results.append(copy.deepcopy(book))
        return results

    def borrow_book(self, member_id, isbn):
        book = self.books.get(isbn)
        member = self.members.get(member_id)
        if not book or not member:
            return False, "Book or member not found"
        if book['available_copies'] <= 0:
            return False, "No available copies"
        # Update book
        book['available_copies'] -= 1
        if book['available_copies'] == 0:
            book['status'] = 'Borrowed'
        # Update member
        member['books_borrowed'] += 1
        # Add transaction
        txn_id = f"TXN{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        due_date = datetime.now() + timedelta(days=30)
        self.transactions.append({
            "id": txn_id,
            "member_id": member_id,
            "book_isbn": isbn,
            "type": "Borrow",
            "transaction_date": datetime.now().date(),
            "due_date": due_date.date(),
            "return_date": None,
            "fine_amount": 0.0
        })
        return True, "Book borrowed successfully"

    def return_book(self, member_id, isbn):
        book = self.books.get(isbn)
        member = self.members.get(member_id)
        if not book or not member:
            return False, "Book or member not found"
        if member['books_borrowed'] <= 0:
            return False, "No books borrowed to return"
        # Update book
        book['available_copies'] += 1
        if book['available_copies'] > 0:
            book['status'] = 'Available'
        # Update member
        member['books_borrowed'] -= 1
        # Update transaction
        for txn in reversed(self.transactions):
            if (txn['member_id'] == member_id and txn['book_isbn'] == isbn and
                txn['type'] == 'Borrow' and txn['return_date'] is None):
                txn['return_date'] = datetime.now().date()
                break
        # Add return transaction
        txn_id = f"TXN{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        self.transactions.append({
            "id": txn_id,
            "member_id": member_id,
            "book_isbn": isbn,
            "type": "Return",
            "transaction_date": datetime.now().date(),
            "due_date": None,
            "return_date": datetime.now().date(),
            "fine_amount": 0.0
        })
        return True, "Book returned successfully"

    def add_book(self, book_data):
        isbn = book_data.get('isbn')
        if not isbn:
            return False, "ISBN required"
        if isbn in self.books:
            return False, "Book already exists"
        new_book = {
            "id": book_data.get('id', f"B{datetime.now().strftime('%Y%m%d%H%M%S%f')}"),
            "title": book_data.get('title', ''),
            "author": book_data.get('author', ''),
            "isbn": isbn,
            "genre": book_data.get('genre', ''),
            "status": book_data.get('status', 'Available'),
            "copies": book_data.get('copies', 1),
            "available_copies": book_data.get('available_copies', book_data.get('copies', 1)),
            "publish_year": book_data.get('publish_year'),
            "pages": book_data.get('pages'),
            "rating": book_data.get('rating', 0.0),
            "description": book_data.get('description', '')
        }
        self.books[isbn] = new_book
        return True, "Book added successfully"

    def add_member(self, member_data):
        member_id = member_data.get('member_id')
        if not member_id:
            return False, "Member ID required"
        if member_id in self.members:
            return False, "Member already exists"
        new_member = {
            "member_id": member_id,
            "name": member_data.get('name', ''),
            "email": member_data.get('email', ''),
            "role": member_data.get('role', 'Student'),
            "books_borrowed": member_data.get('books_borrowed', 0),
            "fine_amount": member_data.get('fine_amount', 0.0),
            "password": member_data.get('password', 'default123'),
        }
        self.members[member_id] = new_member
        return True, "Member added successfully"

    def get_transactions(self, member_id=None, limit=10):
        filtered = [t for t in self.transactions if (member_id is None or t['member_id'] == member_id)]
        filtered = sorted(filtered, key=lambda x: x['transaction_date'], reverse=True)
        return copy.deepcopy(filtered[:limit])

    def close_connection(self):
        # Nothing to close in-memory
        print("In-memory database closed")
