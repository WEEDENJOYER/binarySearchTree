from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.text import Text

# Initialize the console
console = Console()

class Book:
    def __init__(self, isbn, title, author, publisher, year):
        self.isbn = int(isbn)  # Ensure ISBN is treated as an integer
        self.title = title
        self.author = author
        self.publisher = publisher
        self.year = year

    def __str__(self):
        return f'ISBN: {self.isbn}, Title: {self.title}, Author: {self.author}, Publisher: {self.publisher}, Year: {self.year}'


class Node:
    def __init__(self, key, data):
        self.left = None
        self.right = None
        self.key = key
        self.data = data


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key, data, overwrite=False):
        if self.root is None:
            self.root = Node(key, data)
            return True
        else:
            return self._insert(self.root, key, data, overwrite)

    def _insert(self, node, key, data, overwrite):
        node_key = int(node.key)
        key = int(key)
        if key < node_key:
            if node.left is None:
                node.left = Node(key, data)
                return True
            else:
                return self._insert(node.left, key, data, overwrite)
        elif key > node_key:
            if node.right is None:
                node.right = Node(key, data)
                return True
            else:
                return self._insert(node.right, key, data, overwrite)
        else:
            if overwrite:
                console.print("Overwriting the existing book.", style="bold yellow")
                node.data = data
                return True
            else:
                console.print("A book with the same ISBN already exists. Skipping insertion.", style="bold red")
                return False

    def search(self, key):
        try:
            key = int(key)
        except ValueError:
            console.print("Invalid ISBN format. ISBN should be an integer.", style="bold red")
            return None
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None or int(node.key) == key:
            return node
        if key < int(node.key):
            return self._search(node.left, key)
        return self._search(node.right, key)

    def delete(self, key):
        try:
            key = int(key)
        except ValueError:
            console.print("Invalid ISBN format. ISBN should be an integer.", style="bold red")
            return
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            console.print(f"Book with ISBN {key} not found. Deletion failed.", style="bold red")
            return node
        node_key = int(node.key)
        if key < node_key:
            node.left = self._delete(node.left, key)
        elif key > node_key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.data = temp.data
            node.right = self._delete(node.right, temp.key)
        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def inorder_traversal(self):
        result = []
        self._inorder_traversal(self.root, result)
        return result

    def _inorder_traversal(self, node, result):
        if node:
            self._inorder_traversal(node.left, result)
            result.append(node.data)
            self._inorder_traversal(node.right, result)

    def preorder_traversal(self):
        result = []
        self._preorder_traversal(self.root, result)
        return result

    def _preorder_traversal(self, node, result):
        if node:
            result.append(node.data)
            self._preorder_traversal(node.left, result)
            self._preorder_traversal(node.right, result)

    def postorder_traversal(self):
        result = []
        self._postorder_traversal(self.root, result)
        return result

    def _postorder_traversal(self, node, result):
        if node:
            self._postorder_traversal(node.left, result)
            self._postorder_traversal(node.right, result)
            result.append(node.data)

    def level_order_traversal(self):
        result = []
        if not self.root:
            return result
        queue = [self.root]
        while queue:
            current = queue.pop(0)
            result.append(current.data)
            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)
        return result


def initialize_books(bst):
    books = [
        (10, "Book One", "Author A", "Publisher X", "2001"),
        (5, "Book Two", "Author B", "Publisher Y", "2002"),
        (2, "Book Three", "Author C", "Publisher Z", "2003"),
        (8, "Book Four", "Author D", "Publisher W", "2004"),
        (15, "Book Five", "Author E", "Publisher V", "2005"),
        (12, "Book Six", "Author F", "Publisher U", "2006"),
        (18, "Book Seven", "Author G", "Publisher T", "2007"),
        (11, "Book Eight", "Author H", "Publisher S", "2008"),
        (14, "Book Nine", "Author I", "Publisher R", "2009"),
        (20, "Book Ten", "Author J", "Publisher Q", "2010")
    ]

    for isbn, title, author, publisher, year in books:
        book = Book(isbn, title, author, publisher, year)
        bst.insert(isbn, book)


def display_books(books, traversal_type):
    if books:
        table = Table(title=f"Books ({traversal_type} Traversal)")
        table.add_column("ISBN", justify="right", style="cyan", no_wrap=True)
        table.add_column("Title", style="magenta")
        table.add_column("Author", style="green")
        table.add_column("Publisher", style="blue")
        table.add_column("Year", style="yellow")

        for book in books:
            table.add_row(str(book.isbn), book.title, book.author, book.publisher, book.year)

        console.print(table)
    else:
        console.print("No books in the library.", style="bold red")


def menu():
    bst = BinarySearchTree()
    initialize_books(bst)

    while True:
        console.print("\n" + "=" * 50, style="bold blue")
        console.print(" Library Management System ".center(50, "="), style="bold yellow")
        console.print("=" * 50, style="bold blue")
        console.print("1. Insert Book")
        console.print("2. Delete Book")
        console.print("3. Search Book")
        console.print("4. Display All Books (Inorder)")
        console.print("5. Display All Books (Preorder)")
        console.print("6. Display All Books (Postorder)")
        console.print("7. Display All Books (Level Order)")
        console.print("8. Exit")
        console.print("=" * 50, style="bold blue")

        choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4", "5", "6", "7", "8"], default="8")

        if choice == '1':
            isbn = Prompt.ask("Enter ISBN")
            title = Prompt.ask("Enter Title")
            author = Prompt.ask("Enter Author")
            publisher = Prompt.ask("Enter Publisher")
            year = Prompt.ask("Enter Year")
            overwrite = Prompt.ask("Do you want to overwrite if a book with the same ISBN exists? (yes/no)", choices=["yes", "no"], default="no")
            try:
                book = Book(isbn, title, author, publisher, year)
                if overwrite == 'yes':
                    if bst.insert(isbn, book, overwrite=True):
                        console.print("Book inserted successfully.", style="bold green")
                else:
                    if bst.insert(isbn, book):
                        console.print("Book inserted successfully.", style="bold green")
            except ValueError:
                console.print("Invalid ISBN format. ISBN should be an integer.", style="bold red")

        elif choice == '2':
            isbn = Prompt.ask("Enter ISBN to delete")
            if bst.search(isbn) is not None:
                bst.delete(isbn)
                console.print("Book deleted successfully.", style="bold green")
            else:
                console.print(f"Book with ISBN {isbn} does not exist. Deletion failed.", style="bold red")
        elif choice == '3':
            isbn = Prompt.ask("Enter ISBN to search")
            node = bst.search(isbn)
            if node:
                console.print("Book found:", style="bold green")
                console.print(str(node.data), style="cyan")
            else:
                console.print("Book not found.", style="bold red")
        elif choice == '4':
            books = bst.inorder_traversal()
            display_books(books, "Inorder")
        elif choice == '5':
            books = bst.preorder_traversal()
            display_books(books, "Preorder")
        elif choice == '6':
            books = bst.postorder_traversal()
            display_books(books, "Postorder")
        elif choice == '7':
            books = bst.level_order_traversal()
            display_books(books, "Level Order")
        elif choice == '8':
            break
        else:
            console.print("Invalid choice, please try again.", style="bold red")

if __name__ == "__main__":
    menu()
