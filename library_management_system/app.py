import streamlit as st
from data_structure import LibrarySystem, Book


def main():
    st.title("Library Management System")

    # Initialize library system
    if 'library' not in st.session_state:
        st.session_state.library = LibrarySystem()

    # Add sample books if not already added
    if 'initialized' not in st.session_state:
        sample_books = [
            Book(1, "Python Programming", "John Smith", "Programming", 3),
            Book(2, "Data Structures", "Jane Doe", "Programming", 2),
            Book(3, "Machine Learning", "Bob Johnson", "AI", 1),
        ]
        for book in sample_books:
            st.session_state.library.add_book(book)
        st.session_state.initialized = True

    # Sidebar navigation
    menu = st.sidebar.selectbox(
        "Menu",
        ["Browse Books", "Borrow/Return", "Place Hold", "View Borrowed"]
    )

    if menu == "Browse Books":
        st.subheader("Available Books")
        for book_id, book in st.session_state.library.books_hash.items():
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"Title: {book.title}")
                st.write(f"Author: {book.author}")
            with col2:
                st.write(f"Category: {book.category}")
                st.write(f"Available: {book.available_copies}/{book.copies}")
            st.write("---")

    elif menu == "Borrow/Return":
        st.subheader("Borrow or Return Books")
        action = st.radio("Select Action", ["Borrow", "Return"])
        book_id = st.number_input("Book ID", min_value=1, step=1)
        user_id = st.text_input("User ID")

        if st.button("Submit"):
            if action == "Borrow":
                if st.session_state.library.borrow_book(book_id, user_id):
                    st.success("Book borrowed successfully!")
                else:
                    st.error("Book not available")
            else:
                if st.session_state.library.return_book(book_id, user_id):
                    st.success("Book returned successfully!")
                else:
                    st.error("Return failed")

    elif menu == "Place Hold":
        st.subheader("Place Hold on Books")
        book_id = st.number_input("Book ID", min_value=1, step=1)
        user_id = st.text_input("User ID")
        priority = st.slider("Priority", 1, 5, 3)

        if st.button("Place Hold"):
            if st.session_state.library.place_hold(book_id, user_id, priority):
                st.success("Hold placed successfully!")
            else:
                st.error("Unable to place hold")

    elif menu == "View Borrowed":
        st.subheader("View Borrowed Books")
        user_id = st.text_input("Enter User ID")
        if user_id:
            borrowed = st.session_state.library.borrowed_books.get(user_id, [])
            if borrowed:
                for borrow in borrowed:
                    book = st.session_state.library.search_book(borrow['book_id'])
                    st.write(f"Title: {book.title}")
                    st.write(f"Due Date: {borrow['due_date'].strftime('%Y-%m-%d')}")
                    st.write("---")
            else:
                st.write("No books currently borrowed")


if __name__ == "__main__":
    main()