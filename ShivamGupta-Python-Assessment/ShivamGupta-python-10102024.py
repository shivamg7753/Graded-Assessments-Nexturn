class InvalidBookDataError(Exception):
    """Custom exception raised when invalid data is provided for a book."""
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        super().__init__(f"Invalid book data: Title='{title}', Author='{author}'. Title and Author are required.")


class BorrowLimitExceededException(Exception):
    """Custom exception raised when a member exceeds their borrowing limit."""
    def __init__(self, member_name, max_books):
        self.member_name = member_name
        self.max_books = max_books
        super().__init__(f"Borrow limit exceeded for {member_name}. Max books allowed: {max_books}")

class BookUnavailableError(Exception):
    """Custom exception raised when a book is unavailable for borrowing."""
    def __init__(self, book_title):
        self.book_title = book_title
        super().__init__(f"Book '{book_title}' is unavailable for borrowing.")

class BookNotBorrowedError(Exception):
    """Custom exception raised when trying to return a book that was not borrowed by the member."""
    def __init__(self, book_title, member_name):
        self.book_title = book_title
        self.member_name = member_name
        super().__init__(f"Book '{book_title}' was not borrowed by {member_name}.")


class InvalidBookDataError(Exception):
    """Custom exception raised when invalid data is provided for a book."""
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        super().__init__(f"Invalid book data: Title='{title}', Author='{author}'. Title and Author are required.")


class Book:
    def __init__(self, book_id, title, author, category):
        if not title or not author:
            raise InvalidBookDataError(book_id, title, author)
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category  # 'fiction' or 'non-fiction'
        self.status = 'available'

    def borrow(self):
        if self.status == 'borrowed':
            raise BookUnavailableError(self.title)
        self.status = 'borrowed'

    def return_book(self):
        self.status = 'available'


class Member:
    def __init__(self, member_id, name, max_books):
        if not name:
            raise ValueError("Member must have a valid name.")
        self.member_id = member_id
        self.name = name
        self.max_books = max_books  # Regular: 3, Premium: 5
        self.borrowed_books = []

    def borrow_book(self, book):
        if len(self.borrowed_books) >= self.max_books:
            raise BorrowLimitExceededException(self.name, self.max_books)
        book.borrow()
        self.borrowed_books.append(book)

    def return_book(self, book):
        if book not in self.borrowed_books:
            raise BookNotBorrowedError(book.title, self.name)
        book.return_book()
        self.borrowed_books.remove(book)



class RegularMember(Member):
    def __init__(self, member_id, name):
        super().__init__(member_id, name, max_books=3)

class PremiumMember(Member):
    def __init__(self, member_id, name):
        super().__init__(member_id, name, max_books=5)



class Library:
    def __init__(self):
        self.book_collection = {}
        self.members = {}

    def add_book(self, book):
        if book.book_id in self.book_collection:
            raise ValueError(f"Book with ID {book.book_id} already exists.")
        self.book_collection[book.book_id] = book

    def register_member(self, member):
        if member.member_id in self.members:
            raise ValueError(f"Member with ID {member.member_id} already exists.")
        self.members[member.member_id] = member

    def lend_book(self, member_id, book_id):
        if member_id not in self.members:
            raise ValueError(f"Member with ID {member_id} does not exist.")
        if book_id not in self.book_collection:
            raise ValueError(f"Book with ID {book_id} does not exist.")
        
        member = self.members[member_id]
        book = self.book_collection[book_id]
        member.borrow_book(book)

    def receive_return(self, member_id, book_id):
        if member_id not in self.members:
            raise ValueError(f"Member with ID {member_id} does not exist.")
        if book_id not in self.book_collection:
            raise ValueError(f"Book with ID {book_id} does not exist.")
        
        member = self.members[member_id]
        book = self.book_collection[book_id]
        member.return_book(book)


if __name__ =="__main__":

 library = Library()

 try:
        book1 = Book(101, "", "George Orwell", "fiction")  # Missing title

 except InvalidBookDataError as e:
        print(f"Error: {e}")

 book2 = Book(102, "Sapiens", "Yuval Noah Harari", "non-fiction")
 book3 = Book(103, "Brave New World", "Aldous Huxley", "fiction")
    
 library.add_book(book2)
 library.add_book(book3)

    
 member1 = RegularMember(1, "Alice")
 member2 = PremiumMember(2, "Bob")

 library.register_member(member1)
 library.register_member(member2)

 print(f"{member1.name} borrows {book2.title} ")
 library.lend_book(1, 102)

  # Try to borrow the same book (which is already borrowed by Alice)

 try:
        print(f" {member2.name} tries to borrow {book2.title} ")
        library.lend_book(2, 102)
 except BookUnavailableError as e:
        print(f"Error: {e}")


 print(f"{member1.name} returns {book2.title}")
 library.receive_return(1, 102)

 # Bob tries to return a book he didn't borrow

 try:
        print(f"{member2.name} tries to return {book2.title}")
        library.receive_return(2, 102)
 except BookNotBorrowedError as e:
        print(f"Error: {e}")