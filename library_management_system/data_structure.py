from collections import defaultdict
import heapq
import networkx as nx
from datetime import datetime, timedelta


class Book:
    def __init__(self, id, title, author, category, copies=1):
        self.id = id
        self.title = title
        self.author = author
        self.category = category
        self.copies = copies
        self.available_copies = copies


class BSTNode:
    def __init__(self, book):
        self.book = book
        self.left = None
        self.right = None


class LibrarySystem:
    def __init__(self):
        self.books_hash = {}  # Hash Table for books
        self.bst_root = None  # BST for title-based organization
        self.hold_requests = []  # Priority Queue
        self.recommendation_graph = nx.Graph()  # Graph for recommendations
        self.borrowed_books = defaultdict(list)  # Hash table for borrowed books

    def add_book(self, book):
        # Hash Table operation
        self.books_hash[book.id] = book

        # BST operation
        if not self.bst_root:
            self.bst_root = BSTNode(book)
        else:
            self._insert_bst(self.bst_root, book)

        # Graph operation
        self.recommendation_graph.add_node(book.id, title=book.title, category=book.category)
        for other_id in self.books_hash:
            if self.books_hash[other_id].category == book.category and other_id != book.id:
                self.recommendation_graph.add_edge(book.id, other_id)

    def _insert_bst(self, node, book):
        if book.title < node.book.title:
            if node.left is None:
                node.left = BSTNode(book)
            else:
                self._insert_bst(node.left, book)
        else:
            if node.right is None:
                node.right = BSTNode(book)
            else:
                self._insert_bst(node.right, book)

    def search_book(self, book_id):
        return self.books_hash.get(book_id)

    def place_hold(self, book_id, user_id, priority):
        if book_id in self.books_hash:
            heapq.heappush(self.hold_requests, (priority, datetime.now(), book_id, user_id))
            return True
        return False

    def get_recommendations(self, book_id):
        if book_id in self.recommendation_graph:
            return [self.books_hash[n] for n in self.recommendation_graph.neighbors(book_id)]
        return []

    def borrow_book(self, book_id, user_id):
        book = self.books_hash.get(book_id)
        if book and book.available_copies > 0:
            book.available_copies -= 1
            self.borrowed_books[user_id].append({
                'book_id': book_id,
                'borrow_date': datetime.now(),
                'due_date': datetime.now() + timedelta(days=14)
            })
            return True
        return False

    def return_book(self, book_id, user_id):
        book = self.books_hash.get(book_id)
        if book:
            for borrow in self.borrowed_books[user_id]:
                if borrow['book_id'] == book_id:
                    book.available_copies += 1
                    self.borrowed_books[user_id].remove(borrow)
                    return True
        return False