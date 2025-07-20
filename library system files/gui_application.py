import tkinter as tk
from tkinter import ttk, messagebox

class LibraryGUI:
    def __init__(self, system=None, db=None):
        self.system = system
        self.db = db
        self.current_user = None

        self.root = tk.Tk()
        self.root.title("Library Management System")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')

        self.setup_themes()
        self.frames = {}

        self.create_login_frame()
        self.create_student_dashboard()
        self.create_librarian_dashboard()
        self.create_admin_dashboard()

        self.show_frame("Login")

    def setup_themes(self):
        self.student_colors = {
            "primary": "#3498db",
            "accent": "#2ecc71",
            "background": "#ecf0f1",
            "card_bg": "#ffffff",
            "sidebar_bg": "#34495e",
            "text_color": "#2c3e50",
            "button_bg": "#3498db",
            "button_hover": "#2980b9",
            "status_colors": {
                "active": "#28A745",
                "nearing_due": "#FFC107",
                "overdue": "#DC3545"
            }
        }
        self.librarian_colors = {
            "primary": "#e74c3c",
            "accent": "#f39c12",
            "background": "#ecf0f1",
            "card_bg": "#ffffff",
            "sidebar_bg": "#2c3e50",
            "text_color": "#2c3e50",
            "button_bg": "#e74c3c",
            "button_hover": "#c0392b",
            "status_colors": {
                "active": "#28A745",
                "nearing_due": "#FFC107",
                "overdue": "#DC3545"
            }
        }
        self.admin_colors = {
            "primary": "#9b59b6",
            "accent": "#1abc9c",
            "background": "#ecf0f1",
            "card_bg": "#ffffff",
            "sidebar_bg": "#2c3e50",
            "text_color": "#2c3e50",
            "button_bg": "#9b59b6",
            "button_hover": "#8e44ad",
            "status_colors": {
                "active": "#28A745",
                "nearing_due": "#FFC107",
                "overdue": "#DC3545"
            }
        }

        self.style.configure('Student.TFrame', background=self.student_colors["background"])
        self.style.configure('Student.TLabel', background=self.student_colors["background"], foreground=self.student_colors["text_color"])
        self.style.configure('Student.TButton', background=self.student_colors["button_bg"], foreground=self.student_colors["card_bg"], borderwidth=0, relief='flat')
        self.style.map('Student.TButton', background=[('active', self.student_colors["button_hover"])])
        self.style.configure('Student.Treeview.Heading', background=self.student_colors["primary"], foreground=self.student_colors["card_bg"], font=("Segoe UI", 10, "bold"))
        self.style.configure('Student.Treeview', background=self.student_colors["card_bg"], fieldbackground=self.student_colors["card_bg"], foreground=self.student_colors["text_color"])
        self.style.map('Student.Treeview', background=[('selected', self.student_colors["accent"])])
        self.style.configure('Student.TEntry', fieldbackground=self.student_colors["card_bg"], foreground=self.student_colors["text_color"], bordercolor=self.student_colors["primary"])
        self.style.configure('Student.TCombobox', fieldbackground=self.student_colors["card_bg"], selectbackground=self.student_colors["card_bg"], selectforeground=self.student_colors["text_color"], bordercolor=self.student_colors["primary"])

        self.style.configure('Librarian.TFrame', background=self.librarian_colors["background"])
        self.style.configure('Librarian.TLabel', background=self.librarian_colors["background"], foreground=self.librarian_colors["text_color"])
        self.style.configure('Librarian.TButton', background=self.librarian_colors["button_bg"], foreground=self.librarian_colors["card_bg"], borderwidth=0, relief='flat')
        self.style.map('Librarian.TButton', background=[('active', self.librarian_colors["button_hover"])])
        self.style.configure('Librarian.Treeview.Heading', background=self.librarian_colors["primary"], foreground=self.librarian_colors["card_bg"], font=("Segoe UI", 10, "bold"))
        self.style.configure('Librarian.Treeview', background=self.librarian_colors["card_bg"], fieldbackground=self.librarian_colors["card_bg"], foreground=self.librarian_colors["text_color"])
        self.style.map('Librarian.Treeview', background=[('selected', self.librarian_colors["accent"])])
        self.style.configure('Librarian.TEntry', fieldbackground=self.librarian_colors["card_bg"], foreground=self.librarian_colors["text_color"], bordercolor=self.librarian_colors["primary"])
        self.style.configure('Librarian.TCombobox', fieldbackground=self.librarian_colors["card_bg"], selectbackground=self.librarian_colors["card_bg"], selectforeground=self.librarian_colors["text_color"], bordercolor=self.librarian_colors["primary"])

        self.style.configure('Admin.TFrame', background=self.admin_colors["background"])
        self.style.configure('Admin.TLabel', background=self.admin_colors["background"], foreground=self.admin_colors["text_color"])
        self.style.configure('Admin.TButton', background=self.admin_colors["button_bg"], foreground=self.admin_colors["card_bg"], borderwidth=0, relief='flat')
        self.style.map('Admin.TButton', background=[('active', self.admin_colors["button_hover"])])
        self.style.configure('Admin.Treeview.Heading', background=self.admin_colors["primary"], foreground=self.admin_colors["card_bg"], font=("Segoe UI", 10, "bold"))
        self.style.configure('Admin.Treeview', background=self.admin_colors["card_bg"], fieldbackground=self.admin_colors["card_bg"], foreground=self.admin_colors["text_color"])
        self.style.map('Admin.Treeview', background=[('selected', self.admin_colors["accent"])])
        self.style.configure('Admin.TEntry', fieldbackground=self.admin_colors["card_bg"], foreground=self.admin_colors["text_color"], bordercolor=self.admin_colors["primary"])
        self.style.configure('Admin.TCombobox', fieldbackground=self.admin_colors["card_bg"], selectbackground=self.admin_colors["card_bg"], selectforeground=self.admin_colors["text_color"], bordercolor=self.admin_colors["primary"])

    def apply_dashboard_style(self, frame, role):
        if role.lower() == "student":
            style_prefix = "Student."
            current_colors = self.student_colors
        elif role.lower() == "librarian":
            style_prefix = "Librarian."
            current_colors = self.librarian_colors
        elif role.lower() == "administrator":
            style_prefix = "Admin."
            current_colors = self.admin_colors
        else:
            return

        frame.configure(style=f'{style_prefix}TFrame')

        for widget in frame.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.configure(style=f'{style_prefix}TLabel')
            elif isinstance(widget, ttk.Button):
                widget.configure(style=f'{style_prefix}TButton')
            elif isinstance(widget, ttk.Frame):
                widget.configure(style=f'{style_prefix}TFrame')
                self.apply_dashboard_style(widget, role)
            elif isinstance(widget, ttk.Treeview):
                widget.configure(style=f'{style_prefix}Treeview')
                self.style.configure(f'{style_prefix}Treeview.Heading',
                                     background=current_colors["primary"],
                                     foreground=current_colors["card_bg"])
            elif isinstance(widget, ttk.Entry):
                widget.configure(style=f'{style_prefix}TEntry')
            elif isinstance(widget, ttk.Combobox):
                widget.configure(style=f'{style_prefix}TCombobox')

    def clear_frame(self, frame_name):
        frame = self.frames.get(frame_name)
        if frame:
            for widget in frame.winfo_children():
                widget.destroy()

    def show_frame(self, frame_name):
        for f in self.frames.values():
            f.pack_forget()
        frame = self.frames.get(frame_name)
        if frame:
            frame.pack(fill='both', expand=True)
            if frame_name == "StudentDashboard":
                self.apply_dashboard_style(frame, "student")
            elif frame_name == "LibrarianDashboard":
                self.apply_dashboard_style(frame, "librarian")
            elif frame_name == "AdminDashboard":
                self.apply_dashboard_style(frame, "administrator")

    def create_login_frame(self):
        frame = tk.Frame(self.root, bg="#931cd4")
        self.frames["Login"] = frame

        card = tk.Frame(frame, bg="white", bd=2, relief="groove")
        card.place(relx=0.5, rely=0.5, anchor='center', width=350, height=300)

        title = tk.Label(card, text="Library Management System", font=("Segoe UI", 18, "bold"), bg="white", fg="#2c3e50")
        title.pack(pady=20)

        lbl_id = tk.Label(card, text="Member ID:", bg="white", fg="#2c3e50")
        lbl_id.pack(pady=(10, 5))
        self.entry_member_id = tk.Entry(card)
        self.entry_member_id.pack(ipady=5, ipadx=5)

        lbl_pw = tk.Label(card, text="Password:", bg="white", fg="#2c3e50")
        lbl_pw.pack(pady=(10, 5))
        self.entry_password = tk.Entry(card, show="*")
        self.entry_password.pack(ipady=5, ipadx=5)

        login_btn = tk.Button(card, text="Login", bg="#3498db", fg="white", activebackground="#2980b9",
                               command=self.handle_login)
        login_btn.pack(pady=20, ipadx=10, ipady=5)

        frame.pack(fill='both', expand=True)

    def handle_login(self):
        member_id = self.entry_member_id.get().strip()
        password = self.entry_password.get().strip()

        if self.db:
            user = self.db.authenticate_user(member_id, password)
            if user:
                self.current_user = user
                role = user.get('role', 'Student')
                self.post_login(role)
            else:
                messagebox.showerror("Login Failed", "Invalid member ID or password")
        elif self.system:
            if self.system.authenticate_user(member_id, password):
                self.current_user = self.system.current_user
                role = self.current_user.get('role', 'Student')
                self.post_login(role)
            else:
                messagebox.showerror("Login Failed", "Invalid member ID or password")
        else:
            messagebox.showerror("Error", "No backend available")

    def post_login(self, role):
        self.entry_member_id.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

        if role.lower() == "student":
            self.show_frame("StudentDashboard")
            self.build_student_dashboard()
        elif role.lower() == "librarian":
            self.show_frame("LibrarianDashboard")
            self.build_librarian_dashboard()
        elif role.lower() == "administrator":
            self.show_frame("AdminDashboard")
            self.build_admin_dashboard()
        else:
            self.show_frame("StudentDashboard")
            self.build_student_dashboard()

    def create_student_dashboard(self):
        frame = ttk.Frame(self.root)
        self.frames["StudentDashboard"] = frame

        self.student_title = ttk.Label(frame, text="Student Dashboard", font=("Segoe UI", 18, "bold"))
        self.student_title.pack(pady=10)

        search_frame = ttk.Frame(frame)
        search_frame.pack(pady=10, fill='x')

        ttk.Label(search_frame, text="Search:").pack(side='left', padx=(5,2))
        self.student_search_var = tk.StringVar()
        self.student_search_entry = ttk.Entry(search_frame, textvariable=self.student_search_var)
        self.student_search_entry.pack(side='left', padx=5)
        self.student_search_entry.bind("<Return>", lambda e: self.student_search_books())

        ttk.Label(search_frame, text="Filter Genre:").pack(side='left', padx=(20,2))
        self.student_genre_var = tk.StringVar()
        self.student_genre_filter = ttk.Combobox(search_frame, textvariable=self.student_genre_var, state="readonly")
        self.student_genre_filter.pack(side='left', padx=5)
        self.student_genre_filter.bind("<<ComboboxSelected>>", lambda e: self.student_search_books())

        ttk.Label(search_frame, text="Filter Availability:").pack(side='left', padx=(20,2))
        self.student_avail_var = tk.StringVar()
        self.student_avail_filter = ttk.Combobox(search_frame, textvariable=self.student_avail_var, state="readonly")
        self.student_avail_filter['values'] = ["All", "Available", "Borrowed"]
        self.student_avail_filter.current(0)
        self.student_avail_filter.pack(side='left', padx=5)
        self.student_avail_filter.bind("<<ComboboxSelected>>", lambda e: self.student_search_books())

        columns = ("ISBN", "Title", "Author", "Genre", "Status", "Copies")
        self.student_tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode='browse')
        for col in columns:
            self.student_tree.heading(col, text=col)
            self.student_tree.column(col, minwidth=50, width=120)
        self.student_tree.pack(fill='both', expand=True, padx=10, pady=10)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)

        self.student_borrow_btn = ttk.Button(btn_frame, text="Borrow Book", command=self.student_borrow_book)
        self.student_borrow_btn.pack(side='left', padx=10)

        self.student_return_btn = ttk.Button(btn_frame, text="Return Book", command=self.student_return_book)
        self.student_return_btn.pack(side='left', padx=10)

        self.student_logout_btn = ttk.Button(btn_frame, text="Logout", command=self.logout)
        self.student_logout_btn.pack(side='left', padx=10)

    def build_student_dashboard(self):
        genres = set(book["genre"] for book in self.get_all_books())
        genre_list = ["All"] + sorted(genres)
        self.student_genre_filter['values'] = genre_list
        self.student_genre_filter.current(0)
        self.student_avail_filter.current(0)
        self.student_search_var.set("")
        self.update_student_book_list()

    def student_search_books(self):
        self.update_student_book_list()

    def update_student_book_list(self):
        search_term = self.student_search_var.get().lower()
        genre_filter = self.student_genre_var.get()
        avail_filter = self.student_avail_var.get()

        books = self.get_all_books()

        filtered = []
        for book in books:
            if search_term and search_term not in (book['title'].lower() + book['author'].lower() + book['isbn'].lower()):
                continue
            if genre_filter and genre_filter != "All" and book['genre'] != genre_filter:
                continue
            if avail_filter == "Available" and book['status'] != "Available":
                continue
            if avail_filter == "Borrowed" and book['status'] != "Borrowed":
                continue
            filtered.append(book)

        for item in self.student_tree.get_children():
            self.student_tree.delete(item)

        for book in filtered:
            self.student_tree.insert('', 'end', values=(
                book.get('isbn', ''),
                book.get('title', ''),
                book.get('author', ''),
                book.get('genre', ''),
                book.get('status', ''),
                book.get('copies', 0)
            ))

    def student_borrow_book(self):
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a book to borrow")
            return

        isbn = self.student_tree.item(selected[0])['values'][0]
        member_id = self.current_user.get('member_id')
        if self.db:
            success, msg = self.db.borrow_book(member_id, isbn)
        else:
            success, msg = self.system.borrow_book(member_id, isbn)

        if success:
            messagebox.showinfo("Success", msg)
            self.update_student_book_list()
        else:
            messagebox.showerror("Error", msg)

    def student_return_book(self):
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a book to return")
            return

        isbn = self.student_tree.item(selected[0])['values'][0]
        member_id = self.current_user.get('member_id')
        if self.db:
            success, msg = self.db.return_book(member_id, isbn)
        else:
            success, msg = self.system.return_book(member_id, isbn)

        if success:
            messagebox.showinfo("Success", msg)
            self.update_student_book_list()
        else:
            messagebox.showerror("Error", msg)

    def create_librarian_dashboard(self):
        frame = ttk.Frame(self.root)
        self.frames["LibrarianDashboard"] = frame

        self.librarian_title = ttk.Label(frame, text="Librarian Dashboard", font=("Segoe UI", 18, "bold"))
        self.librarian_title.pack(pady=10)

        search_frame = ttk.Frame(frame)
        search_frame.pack(pady=10, fill='x')

        ttk.Label(search_frame, text="Search:").pack(side='left', padx=(5,2))
        self.lib_search_var = tk.StringVar()
        self.lib_search_entry = ttk.Entry(search_frame, textvariable=self.lib_search_var)
        self.lib_search_entry.pack(side='left', padx=5)
        self.lib_search_entry.bind("<Return>", lambda e: self.librarian_search_books())

        ttk.Label(search_frame, text="Filter Genre:").pack(side='left', padx=(20,2))
        self.lib_genre_var = tk.StringVar()
        self.lib_genre_filter = ttk.Combobox(search_frame, textvariable=self.lib_genre_var, state="readonly")
        self.lib_genre_filter.pack(side='left', padx=5)
        self.lib_genre_filter.bind("<<ComboboxSelected>>", lambda e: self.librarian_search_books())

        ttk.Label(search_frame, text="Filter Availability:").pack(side='left', padx=(20,2))
        self.lib_avail_var = tk.StringVar()
        self.lib_avail_filter = ttk.Combobox(search_frame, textvariable=self.lib_avail_var, state="readonly")
        self.lib_avail_filter['values'] = ["All", "Available", "Borrowed"]
        self.lib_avail_filter.current(0)
        self.lib_avail_filter.pack(side='left', padx=5)
        self.lib_avail_filter.bind("<<ComboboxSelected>>", lambda e: self.librarian_search_books())

        columns = ("ISBN", "Title", "Author", "Genre", "Status", "Copies")
        self.lib_tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode='browse')
        for col in columns:
            self.lib_tree.heading(col, text=col)
            self.lib_tree.column(col, minwidth=50, width=120)
        self.lib_tree.pack(fill='both', expand=True, padx=10, pady=10)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)

        self.lib_borrow_btn = ttk.Button(btn_frame, text="Borrow Book", command=self.librarian_borrow_book)
        self.lib_borrow_btn.pack(side='left', padx=5)

        self.lib_return_btn = ttk.Button(btn_frame, text="Return Book", command=self.librarian_return_book)
        self.lib_return_btn.pack(side='left', padx=5)

        self.lib_add_btn = ttk.Button(btn_frame, text="Add Book", command=self.librarian_add_book)
        self.lib_add_btn.pack(side='left', padx=5)

        self.lib_remove_btn = ttk.Button(btn_frame, text="Remove Book", command=self.librarian_remove_book)
        self.lib_remove_btn.pack(side='left', padx=5)

        self.lib_logout_btn = ttk.Button(btn_frame, text="Logout", command=self.logout)
        self.lib_logout_btn.pack(side='left', padx=5)

    def build_librarian_dashboard(self):
        genres = set(book["genre"] for book in self.get_all_books())
        genre_list = ["All"] + sorted(genres)
        self.lib_genre_filter['values'] = genre_list
        self.lib_genre_filter.current(0)
        self.lib_avail_filter.current(0)
        self.lib_search_var.set("")
        self.update_librarian_book_list()

    def librarian_search_books(self):
        self.update_librarian_book_list()

    def update_librarian_book_list(self):
        search_term = self.lib_search_var.get().lower()
        genre_filter = self.lib_genre_var.get()
        avail_filter = self.lib_avail_var.get()

        books = self.get_all_books()

        filtered = []
        for book in books:
            if search_term and search_term not in (book['title'].lower() + book['author'].lower() + book['isbn'].lower()):
                continue
            if genre_filter and genre_filter != "All" and book['genre'] != genre_filter:
                continue
            if avail_filter == "Available" and book['status'] != "Available":
                continue
            if avail_filter == "Borrowed" and book['status'] != "Borrowed":
                continue
            filtered.append(book)

        for item in self.lib_tree.get_children():
            self.lib_tree.delete(item)

        for book in filtered:
            self.lib_tree.insert('', 'end', values=(
                book.get('isbn', ''),
                book.get('title', ''),
                book.get('author', ''),
                book.get('genre', ''),
                book.get('status', ''),
                book.get('copies', 0)
            ))

    def librarian_borrow_book(self):
        selected = self.lib_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a book to borrow")
            return

        isbn = self.lib_tree.item(selected[0])['values'][0]
        member_id = self.current_user.get('member_id')
        if self.db:
            success, msg = self.db.borrow_book(member_id, isbn)
        else:
            success, msg = self.system.borrow_book(member_id, isbn)

        if success:
            messagebox.showinfo("Success", msg)
            self.update_librarian_book_list()
        else:
            messagebox.showerror("Error", msg)

    def librarian_return_book(self):
        selected = self.lib_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a book to return")
            return

        isbn = self.lib_tree.item(selected[0])['values'][0]
        member_id = self.current_user.get('member_id')
        if self.db:
            success, msg = self.db.return_book(member_id, isbn)
        else:
            success, msg = self.system.return_book(member_id, isbn)

        if success:
            messagebox.showinfo("Success", msg)
            self.update_librarian_book_list()
        else:
            messagebox.showerror("Error", msg)

    def librarian_add_book(self):
        self.add_book_window = tk.Toplevel(self.root)
        self.add_book_window.title("Add New Book")
        self.add_book_window.geometry("400x400")

        self.add_book_window.configure(bg=self.librarian_colors["background"])

        fields = ['isbn', 'title', 'author', 'genre', 'status', 'copies']
        self.add_book_entries = {}
        for idx, field in enumerate(fields):
            lbl = ttk.Label(self.add_book_window, text=field.capitalize(), style='Librarian.TLabel')
            lbl.grid(row=idx, column=0, sticky='e', padx=5, pady=5)
            ent = ttk.Entry(self.add_book_window, style='Librarian.TEntry')
            ent.grid(row=idx, column=1, padx=5, pady=5)
            self.add_book_entries[field] = ent

        ttk.Button(self.add_book_window, text="Add Book", command=self.confirm_add_book, style='Librarian.TButton').grid(row=len(fields), column=0, columnspan=2, pady=15)

    def confirm_add_book(self):
        book_data = {field: entry.get() for field, entry in self.add_book_entries.items()}
        if not book_data.get('isbn') or not book_data.get('title'):
            messagebox.showerror("Error", "ISBN and Title are required")
            return
        try:
            book_data['copies'] = int(book_data.get('copies', 1))
        except ValueError:
            messagebox.showerror("Error", "Copies must be a number")
            return
        if not book_data.get('status'):
            book_data['status'] = 'Available'
        if self.db:
            success, msg = self.db.add_book(book_data)
        else:
            success = self.system.add_book(book_data)
            msg = "Book added successfully" if success else "Failed to add book"
        if success:
            messagebox.showinfo("Success", msg)
            self.add_book_window.destroy()
            self.update_librarian_book_list()
        else:
            messagebox.showerror("Error", msg)

    def librarian_remove_book(self):
        selected = self.lib_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a book to remove")
            return
        isbn = self.lib_tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", f"Remove book with ISBN {isbn}?"):
            if self.db:
                if isbn in self.db.books:
                    del self.db.books[isbn]
                    messagebox.showinfo("Removed", "Book removed successfully")
                else:
                    messagebox.showerror("Error", "Book not found")
            else:
                messagebox.showerror("Error", "Remove not supported in this backend")
            self.update_librarian_book_list()

    def create_admin_dashboard(self):
        frame = ttk.Frame(self.root)
        self.frames["AdminDashboard"] = frame

        label = ttk.Label(frame, text="Administrator Dashboard", font=("Segoe UI", 18, "bold"))
        label.pack(pady=20)
        logout_btn = ttk.Button(frame, text="Logout", command=self.logout)
        logout_btn.pack(pady=20)

        ttk.Label(frame, text="User Management:", font=("Segoe UI", 12, "bold")).pack(pady=(10, 5))
        ttk.Button(frame, text="View All Users").pack(pady=2)
        ttk.Button(frame, text="Add New User").pack(pady=2)
        ttk.Button(frame, text="Remove User").pack(pady=2)

        ttk.Label(frame, text="System Monitoring:", font=("Segoe UI", 12, "bold")).pack(pady=(10, 5))
        ttk.Button(frame, text="View Audit Logs").pack(pady=2)
        ttk.Button(frame, text="Backup Database").pack(pady=2)

    def build_admin_dashboard(self):
        pass

    def get_all_books(self):
        if self.db:
            return self.db.get_all_books()
        elif self.system:
            return self.system.get_all_books()
        return []

    def get_all_members(self):
        if self.db:
            return self.db.get_all_members()
        elif self.system:
            return self.system.get_all_members()
        return []

    def logout(self):
        self.current_user = None
        self.show_frame("Login")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    class DummyDB:
        def __init__(self):
            self.users = {
                "student1": {"password": "pass", "role": "Student", "member_id": "student1"},
                "librarian1": {"password": "pass", "role": "Librarian", "member_id": "librarian1"},
                "admin1": {"password": "pass", "role": "Administrator", "member_id": "admin1"}
            }
            self.books = {
                "978-0321765723": {"isbn": "978-0321765723", "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Classic", "status": "Available", "copies": 5},
                "978-0743273565": {"isbn": "978-0743273565", "title": "1984", "author": "George Orwell", "genre": "Dystopian", "status": "Borrowed", "copies": 0},
                "978-0451524935": {"isbn": "978-0451524935", "title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Classic", "status": "Available", "copies": 3}
            }
            self.borrowed_books = {}

        def authenticate_user(self, member_id, password):
            user = self.users.get(member_id)
            if user and user['password'] == password:
                return user
            return None

        def get_all_books(self):
            return list(self.books.values())

        def borrow_book(self, member_id, isbn):
            book = self.books.get(isbn)
            if not book:
                return False, "Book not found."
            if book['copies'] <= 0:
                return False, "No available copies of this book."

            if member_id in self.borrowed_books and isbn in self.borrowed_books[member_id]:
                return False, "You have already borrowed this copy of the book."

            book['copies'] -= 1
            if book['copies'] == 0:
                book['status'] = 'Borrowed'

            self.borrowed_books.setdefault(member_id, []).append(isbn)
            return True, f"'{book['title']}' borrowed successfully!"

        def return_book(self, member_id, isbn):
            book = self.books.get(isbn)
            if not book:
                return False, "Book not found."

            if member_id not in self.borrowed_books or isbn not in self.borrowed_books[member_id]:
                return False, "You have not borrowed this book."

            book['copies'] += 1
            if book['copies'] > 0:
                book['status'] = 'Available'

            self.borrowed_books[member_id].remove(isbn)
            if not self.borrowed_books[member_id]:
                del self.borrowed_books[member_id]

            return True, f"'{book['title']}' returned successfully!"

        def add_book(self, book_data):
            isbn = book_data.get('isbn')
            if isbn in self.books:
                return False, "Book with this ISBN already exists."
            self.books[isbn] = book_data
            return True, "Book added successfully."

        def get_all_members(self):
            return list(self.users.values())

    gui = LibraryGUI(db=DummyDB())
    gui.run()
