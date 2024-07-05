"""
Author: Sohan Patel
Date Written: 6/25/24
Assignment: Final Project Tkinter GUI
"""
# Import tkinter
import tkinter as tk
from tkinter import ttk, messagebox


# Defining the main application class for the main page window
class MainApp:
    def __init__(self, root):
        """
        Initialise the main application window.
        :param root: The root for Tkinter window.
        """
        self.root = root
        self.root.title("Main Window")  # Title of the main window
        self.root.resizable(False, False)  # Make the main window not resizable
        # Title at the top of the main window and the grid placement
        title = tk.Label(text="Welcome to Book Buddy!", width=26, height=3,
                         font="helvetica 10 bold")
        title.grid(row=0, column=0, pady=10, padx=42)

        # Both images on the main window initialized and placed on grid
        self.my_image = tk.PhotoImage(file="image1.png")
        label = tk.Label(root, image=self.my_image)
        label.grid(row=1, column=0, sticky=tk.W)
        self.my_image2 = tk.PhotoImage(file="image2.png")
        label2 = tk.Label(root, image=self.my_image2)
        label2.grid(row=1, column=0, sticky=tk.E)

        # Button to access the second window of the library, and grid placement
        libraryAccess = tk.Button(text="[Your Library]", width=10, height=3,
                                  bg="blue", fg="white", command=self.open_library_window)
        libraryAccess.grid(row=3, column=0)

        # Exit button that closes out the window
        exitButton = tk.Button(text="[Exit]", command=root.destroy,
                               bg="red", fg="white")
        exitButton.grid(row=0, column=0, sticky=tk.E)

    def open_library_window(self):
        """
        Opens the Library window
        """
        # Creates a new top level window
        library_window = tk.Toplevel(self.root)
        library_window.title("Library Manager")

        # Passes the new window to the LibraryApp class
        LibraryApp(library_window)


class LibraryApp:
    def __init__(self, root):
        """
        Initialise the Library manager window
        :param root: The root Tkinter window for the library manager
        """
        self.root = root

        # List to store details of each book as dictionaries
        self.books = []

        # Main frame for organizing the layout
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Book details input section
        self.title_var = tk.StringVar()  # Variable to store the book title
        self.author_var = tk.StringVar()  # Variable to store book author
        self.status_var = tk.StringVar(value="Not Started")  # Variable to store the book status with
        # default value 'Not Started'

        # Label and entry for the book title space
        ttk.Label(main_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(main_frame, textvariable=self.title_var, width=30).grid(row=0, column=1, padx=5, pady=5)

        # Label and entry for the book's author
        ttk.Label(main_frame, text="Author:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(main_frame, textvariable=self.author_var, width=30).grid(row=1, column=1, padx=5, pady=5)

        # Label and drop down menu for the book status
        ttk.Label(main_frame, text="Status:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.OptionMenu(main_frame, self.status_var, "Not Started", "Not Started", "In Progress", "Completed").grid(
            row=2, column=1, padx=5, pady=5, sticky="w")

        # Button section, for keeping the buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        style = ttk.Style()
        # Button to add a book
        ttk.Button(button_frame, text="[Add Book]", command=self.add_book).grid(row=0, column=0, padx=5, pady=5)
        # Button to edit a book
        ttk.Button(button_frame, text="[Edit Book]", command=self.edit_book).grid(row=0, column=1, padx=5, pady=5)
        # Button to delete one of the books
        ttk.Button(button_frame, text="[Delete Book]", command=self.delete_book).grid(row=0, column=2, padx=5, pady=5)
        # Button to exit the window
        ttk.Button(button_frame, text="[Exit]", command=self.exit_app).grid(row=0, column=3, padx=5, pady=5)

        # Book list displaying section
        self.book_list = ttk.Treeview(main_frame, columns=("Title", "Author", "Status"), show="headings")
        self.book_list.heading("Title", text="Title")  # Heading for the Title column
        self.book_list.heading("Author", text="Author")  # Heading for the Author column
        self.book_list.heading("Status", text="Status")  # Heading for the Status Column
        self.book_list.grid(row=4, column=0, columnspan=2, pady=10, sticky="nsew")  # Positioning the book list

        # Add a scrollbar for the list of books
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.book_list.yview)
        self.book_list.configure(yscroll=scrollbar.set)  # Connecting the scrollbar to the Treeview
        scrollbar.grid(row=4, column=2, sticky='ns')

        # Bind the selection event to update the input fields whenever a book is selected
        self.book_list.bind('<ButtonRelease-1>', self.select_item)

        # Configure column weights to make the GUI responsive
        root.columnconfigure(0, weight=1)  # Make the root window column expandable
        root.rowconfigure(0, weight=1)  # Make the root window row expandable
        main_frame.columnconfigure(1, weight=1)  # Make the main frame column expandable

    def add_book(self):
        """
        Add a new book to the library based on the things in the input fields.
        """
        title = self.title_var.get()  # retrieve the title from the input field
        author = self.author_var.get()  # make the root window row expandable
        status = self.status_var.get()  # Make the main frame column expandable

        if title and author:  # Ensure both the author and title are provided
            self.books.append({"Title": title, "Author": author, "Status": status})  # Add the new book to the list
            self.update_book_list()  # Refresh the Treeview with the updated list
            self.clear_inputs()  # Clear input fields after adding the book
        else:
            # A little warning if either the title or author is missing
            messagebox.showwarning("Input Error", "Please provide both title and author.")

    def edit_book(self):
        """
        Edit the selected book's details regarding, status, title and/or author
        """
        selected_item = self.book_list.selection()  # Get the selected item from the treeview
        if selected_item:  # Check if a book is selected by the user
            index = int(selected_item[0]) - 1  # Convert selection to list index
            title = self.title_var.get()  # Retrieve the updated title from input area
            author = self.author_var.get()  # Retrieve the updated author from input area
            status = self.status_var.get()  # Retrieve the updated status of the book from input area

            if title and author:  # Ensure both author and title are provided
                self.books[index] = {"Title": title, "Author": author, "Status": status}  # Update the books details
                self.update_book_list()  # Refresh the treeview with the updated list.
                self.clear_inputs()  # Clear input fields after the book is edited.
            else:
                # A warning is shown if the title or author is not there
                messagebox.showwarning("Input Error", "Please provide both title and author.")
        else:
            # Also show a warning if a book is not selected for editing
            messagebox.showwarning("Selection Error", "Please select a book to edit.")

    def delete_book(self):
        """
        Delete the selected book from the list.
        """
        selected_item = self.book_list.selection()  # Get the selected item from Treeview
        if selected_item:  # Check is a book is selected
            index = int(selected_item[0]) - 1  # Convert selection to list index
            del self.books[index]  # Remove the selected book from the list
            self.update_book_list()  # Refresh the Treeview with the updated list
            self.clear_inputs()
        else:
            # Show warning if a book isn't selected for deletion
            messagebox.showwarning("Selection Error", "Please select a book to delete.")

    def update_book_list(self):
        """
        Update the Treeview to display the current list of books.
        """
        for i in self.book_list.get_children():
            self.book_list.delete(i)  # Clear the current items in the treeview
        for index, book in enumerate(self.books):  # Add each book to the treeview
            self.book_list.insert("", "end", iid=index + 1, values=(book["Title"], book["Author"], book["Status"]))

    def clear_inputs(self):
        """
        Clear the input fields after adding, editing or deleting a book.
        """
        # Clear the title and author input field
        self.title_var.set("")
        self.author_var.set("")
        self.status_var.set("Not Started")  # Resets the dropdown to the default value, 'Not Started'.

    def select_item(self, event):
        """
        Enters the input fields with the selected book's details.
        :param event: The event that triggered the method
        """
        selected_item = self.book_list.selection()  # Get the selected item from book list
        if selected_item:
            index = int(selected_item[0]) - 1  # Convert the selected item index to a zero-based index
            book = self.books[index]  # Retrieve the book data from the list based on an index
            self.title_var.set(book["Title"])  # Set the title variable in the GUI with the book title
            self.author_var.set(book["Author"])  # Set the title variable in the GUI with book author
            self.status_var.set(book["Status"])  # Set the status variable in the GUI with book's status

    def exit_app(self):
        """
        Destroys the main application window to exit out
        """
        self.root.destroy()


# Initialize the main application window
root = tk.Tk()  # Creates tkinter window
app = MainApp(root)  # Create MainApp with the root window
root.mainloop()  # Start the tkinter event loop to display the GUI and take care of events.
