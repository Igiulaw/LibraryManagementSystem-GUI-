import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("800x600")  # Set fixed size
        self.root.resizable(False, False)  # Disable resizing
        self.books = []
        self.data_file = "library_books.json"
        self.dark_mode = False  # State for dark mode
        self.default_font_size = 12

        self.load_books()
        self.setup_ui()

    def setup_ui(self):
        # Title label
        self.title_label = tk.Label(self.root, text="Library Management System", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)

        # Frames
        self.input_frame = tk.Frame(self.root, padx=20, pady=10)
        self.input_frame.pack(fill="x", pady=5)

        self.button_frame = tk.Frame(self.root, padx=20, pady=10)
        self.button_frame.pack(fill="x", pady=5)

        self.search_frame = tk.Frame(self.root, padx=20, pady=10)
        self.search_frame.pack(fill="x", pady=5)

        self.table_frame = tk.Frame(self.root, padx=20, pady=10)
        self.table_frame.pack(fill="both", expand=True)

        # Input fields
        tk.Label(self.input_frame, text="Title:").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.title_entry = tk.Entry(self.input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.input_frame, text="Author:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.author_entry = tk.Entry(self.input_frame, width=30)
        self.author_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.input_frame, text="Year:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.year_entry = tk.Entry(self.input_frame, width=30)
        self.year_entry.grid(row=2, column=1, padx=10, pady=5)

        # Buttons for actions
        tk.Button(self.button_frame, text="Add Book", command=self.add_book, width=15).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(self.button_frame, text="Update Book", command=self.update_book, width=15).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(self.button_frame, text="Remove Book", command=self.remove_book, width=15).grid(row=0, column=2, padx=10, pady=5)
        tk.Button(self.button_frame, text="Check In/Out", command=self.toggle_check, width=15).grid(row=0, column=3, padx=10, pady=5)

        tk.Button(self.button_frame, text="Toggle Dark Mode", command=self.toggle_dark_mode, width=20).grid(row=1, column=0, padx=10, pady=5)
        tk.Button(self.button_frame, text="Increase Font", command=lambda: self.adjust_font_size(2), width=15).grid(row=1, column=1, padx=10, pady=5)
        tk.Button(self.button_frame, text="Decrease Font", command=lambda: self.adjust_font_size(-2), width=15).grid(row=1, column=2, padx=10, pady=5)
        tk.Button(self.button_frame, text="Refresh", command=self.refresh_table, width=15).grid(row=1, column=3, padx=10, pady=5)

        # Search and table frame
        tk.Label(self.search_frame, text="Search:").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.search_entry = tk.Entry(self.search_frame, width=50)
        self.search_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Button(self.search_frame, text="Search", command=self.search_books).grid(row=0, column=2, padx=10, pady=5)

        # Table
        self.tree = ttk.Treeview(self.table_frame, columns=("Title", "Author", "Year", "Status"), show="headings", height=12)
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Status", text="Status")
        self.tree.column("Title", width=200, anchor="w")
        self.tree.column("Author", width=150, anchor="w")
        self.tree.column("Year", width=100, anchor="center")
        self.tree.column("Status", width=100, anchor="center")
        self.tree.pack(fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Bind selection to input fields
        self.tree.bind("<ButtonRelease-1>", self.select_book)

        self.refresh_table()

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        year = self.year_entry.get().strip()

        if not title or not author or not year:
            messagebox.showerror("Error", "All fields are required!")
            return

        if not year.isdigit():
            messagebox.showerror("Error", "Year must be a number!")
            return

        self.books.append({"Title": title, "Author": author, "Year": year, "Status": "Available"})
        self.refresh_table()
        self.clear_entries()

    def update_book(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No book selected!")
            return

        # Get the selected book index from Treeview
        selected_item_id = selected_item[0]

        # Update the corresponding book in the books list
        book_index = self.tree.index(selected_item_id)

        # Get user inputs
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        year = self.year_entry.get().strip()

        # Validate inputs
        if not title or not author or not year:
            messagebox.showerror("Error", "All fields are required!")
            return

        if not year.isdigit():
            messagebox.showerror("Error", "Year must be a number!")
            return

        # Update the book in the list
        self.books[book_index].update({"Title": title, "Author": author, "Year": year})
        self.refresh_table()
        self.clear_entries()

    def select_book(self, event):
        """Populate the input fields with the details of the selected book."""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        selected_item_id = selected_item[0]
        selected_values = self.tree.item(selected_item_id, "values")

        # Populate the fields with selected book details
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, selected_values[0])

        self.author_entry.delete(0, tk.END)
        self.author_entry.insert(0, selected_values[1])

        self.year_entry.delete(0, tk.END)
        self.year_entry.insert(0, selected_values[2])

    def remove_book(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No book selected!")
            return

        confirm = messagebox.askyesno("Confirm", "Are you sure you want to remove this book?")
        if confirm:
            book_index = self.tree.index(selected_item[0])
            del self.books[book_index]
            self.refresh_table()
            self.clear_entries()

    def toggle_check(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No book selected!")
            return

        book_index = self.tree.index(selected_item[0])
        book = self.books[book_index]
        book["Status"] = "Checked Out" if book["Status"] == "Available" else "Available"
        self.refresh_table()

    def search_books(self):
        query = self.search_entry.get().strip().lower()
        if not query:
            messagebox.showinfo("Info", "Search query cannot be empty!")
            return

        filtered_books = [
            book for book in self.books
            if query in book["Title"].lower() or query in book["Author"].lower() or query == book["Year"]
        ]
        if not filtered_books:
            messagebox.showinfo("Info", "No books match your search query.")
        self.refresh_table(filtered_books)

    def refresh_table(self, books=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        books = books if books is not None else self.books
        for book in books:
            self.tree.insert("", "end", values=(book["Title"], book["Author"], book["Year"], book["Status"]))

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)

    def adjust_font_size(self, size_delta):
        self.default_font_size = max(8, self.default_font_size + size_delta)
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", self.default_font_size))
        self.refresh_table()

    def toggle_dark_mode(self):
        """Toggle between light and dark modes."""
        self.dark_mode = not self.dark_mode

        # Define colors for dark and light modes
        bg_color = "#2E2E2E" if self.dark_mode else "white"
        fg_color = "white" if self.dark_mode else "black"
        entry_bg = "#4A4A4A" if self.dark_mode else "white"
        entry_fg = "white" if self.dark_mode else "black"
        tree_bg = "#2E2E2E" if self.dark_mode else "white"
        tree_fg = "white" if self.dark_mode else "black"

        # Update main window and title label
        self.root.configure(bg=bg_color)
        self.title_label.configure(bg=bg_color, fg=fg_color)

        # Update all frames
        for frame in [self.input_frame, self.button_frame, self.search_frame, self.table_frame]:
            frame.configure(bg=bg_color)
            for widget in frame.winfo_children():
                if isinstance(widget, tk.Entry):
                    widget.configure(bg=entry_bg, fg=entry_fg)
                elif isinstance(widget, tk.Label):
                    widget.configure(bg=bg_color, fg=fg_color)
                elif isinstance(widget, tk.Button):
                    widget.configure(bg=bg_color, fg=fg_color)

        # Update Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=tree_bg, foreground=tree_fg, fieldbackground=tree_bg)
        style.configure("Treeview.Heading", background=bg_color, foreground=fg_color)

    def load_books(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                self.books = json.load(f)

    def save_books(self):
        with open(self.data_file, "w") as f:
            json.dump(self.books, f, indent=4)

    def on_closing(self):
        self.save_books()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
