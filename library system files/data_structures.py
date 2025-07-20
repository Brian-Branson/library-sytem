# Binary Search Tree for books
class TreeNode:
    def __init__(self, book_data):
        self.data = book_data
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.search_count = 0

    def insert(self, book_data):
        if not self.root:
            self.root = TreeNode(book_data)
        else:
            self._insert_recursive(self.root, book_data)

    def _insert_recursive(self, node, book_data):
        if book_data['isbn'] < node.data['isbn']:
            if not node.left:
                node.left = TreeNode(book_data)
            else:
                self._insert_recursive(node.left, book_data)
        else:
            if not node.right:
                node.right = TreeNode(book_data)
            else:
                self._insert_recursive(node.right, book_data)

    def search(self, isbn):
        self.search_count += 1
        return self._search_recursive(self.root, isbn)

    def _search_recursive(self, node, isbn):
        if not node or node.data['isbn'] == isbn:
            return node.data if node else None
        if isbn < node.data['isbn']:
            return self._search_recursive(node.left, isbn)
        return self._search_recursive(node.right, isbn)

    def get_all_books(self):
        books = []
        self._inorder_traversal(self.root, books)
        return books

    def _inorder_traversal(self, node, books):
        if node:
            self._inorder_traversal(node.left, books)
            books.append(node.data)
            self._inorder_traversal(node.right, books)

# Hash Table for members
class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.collision_count = 0

    def _hash(self, key):
        return hash(str(key)) % self.size

    def insert(self, key, value):
        index = self._hash(key)
        bucket = self.table[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        if len(bucket) > 0:
            self.collision_count += 1

        bucket.append((key, value))

    def get(self, key):
        index = self._hash(key)
        bucket = self.table[index]
        for k, v in bucket:
            if k == key:
                return v
        return None

    def delete(self, key):
        index = self._hash(key)
        bucket = self.table[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return True
        return False

    def get_all_members(self):
        members = []
        for bucket in self.table:
            for key, value in bucket:
                members.append(value)
        return members

# Stack for transactions
class Stack:
    def __init__(self):
        self.items = []
        self.operation_count = 0

    def push(self, item):
        self.items.append(item)
        self.operation_count += 1

    def pop(self):
        if not self.is_empty():
            self.operation_count += 1
            return self.items.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def get_all(self):
        return list(reversed(self.items))

# Queue for reservations
class Queue:
    def __init__(self):
        self.items = []
        self.operation_count = 0

    def enqueue(self, item):
        self.items.append(item)
        self.operation_count += 1

    def dequeue(self):
        if not self.is_empty():
            self.operation_count += 1
            return self.items.pop(0)
        return None

    def front(self):
        if not self.is_empty():
            return self.items[0]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def get_all(self):
        return self.items.copy()

# Circular Linked List for circulation history
class CircularNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0
        self.operation_count = 0

    def append(self, data):
        new_node = CircularNode(data)
        self.operation_count += 1

        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = new_node
            new_node.next = self.head

        self.size += 1

    def get_circulation_history(self, limit=10):
        if not self.head:
            return []

        history = []
        current = self.head
        count = 0

        while count < min(limit, self.size):
            history.append(current.data)
            current = current.next
            count += 1

        return history

    def get_size(self):
        return self.size