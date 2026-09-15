"""
STUDENT MANAGEMENT GUI MODULE
Provides the Tkinter-based user interface for the Student Management System
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv
from database_manager import DatabaseManager
from config import *


class StudentManagementGUI:
    """
    Main GUI Application Class for Student Management
    """

    def __init__(self, root):
        """
        Initialize the GUI application

        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(WINDOW_RESIZABLE, WINDOW_RESIZABLE)

        # Initialize database
        self.db = DatabaseManager()

        # Selected student ID for editing
        self.selected_student_id = None

        # Setup GUI
        self.setup_gui()
        self.load_all_students()

    def setup_gui(self):
        """
        Setup the complete GUI layout
        """
        # ===== STYLE CONFIGURATION =====
        style = ttk.Style()
        style.theme_use('clam')

        # ===== TOP FRAME - SEARCH SECTION =====
        top_frame = ttk.Frame(self.root)
        top_frame.pack(pady=10, padx=10, fill='x')

        ttk.Label(top_frame, text="🔍 Search Student:", font=HEADING_FONT).pack(side='left', padx=5)

        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        search_entry = ttk.Entry(top_frame, textvariable=self.search_var, width=30, font=DEFAULT_FONT)
        search_entry.pack(side='left', padx=5)

        ttk.Button(top_frame, text="Clear Search", command=self.clear_search).pack(side='left', padx=5)

        # ===== MIDDLE FRAME - INPUT FIELDS =====
        input_frame = ttk.LabelFrame(self.root, text="Student Information", padding=15)
        input_frame.pack(pady=10, padx=10, fill='x')

        # Row 1: Student ID and Name
        ttk.Label(input_frame, text="Student ID:", font=DEFAULT_FONT).grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.student_id_var = tk.StringVar()
        self.student_id_entry = ttk.Entry(input_frame, textvariable=self.student_id_var, width=15, state='readonly', font=DEFAULT_FONT)
        self.student_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(input_frame, text="Name:", font=DEFAULT_FONT).grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(input_frame, textvariable=self.name_var, width=20, font=DEFAULT_FONT)
        self.name_entry.grid(row=0, column=3, padx=5, pady=5, sticky='w')

        # Row 2: Age and Gender
        ttk.Label(input_frame, text="Age:", font=DEFAULT_FONT).grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.age_var = tk.StringVar()
        self.age_entry = ttk.Entry(input_frame, textvariable=self.age_var, width=15, font=DEFAULT_FONT)
        self.age_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(input_frame, text="Gender:", font=DEFAULT_FONT).grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.gender_var = tk.StringVar()
        gender_combo = ttk.Combobox(input_frame, textvariable=self.gender_var, width=17, font=DEFAULT_FONT,
                                     values=GENDER_OPTIONS, state='readonly')
        gender_combo.grid(row=1, column=3, padx=5, pady=5, sticky='w')

        # Row 3: Course and Contact
        ttk.Label(input_frame, text="Course:", font=DEFAULT_FONT).grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.course_var = tk.StringVar()
        course_combo = ttk.Combobox(input_frame, textvariable=self.course_var, width=15, font=DEFAULT_FONT,
                                     values=AVAILABLE_COURSES, state='readonly')
        course_combo.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(input_frame, text="Contact:", font=DEFAULT_FONT).grid(row=2, column=2, sticky='w', padx=5, pady=5)
        self.contact_var = tk.StringVar()
        self.contact_entry = ttk.Entry(input_frame, textvariable=self.contact_var, width=20, font=DEFAULT_FONT)
        self.contact_entry.grid(row=2, column=3, padx=5, pady=5, sticky='w')

        # Row 4: Email
        ttk.Label(input_frame, text="Email:", font=DEFAULT_FONT).grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(input_frame, textvariable=self.email_var, width=50, font=DEFAULT_FONT)
        self.email_entry.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky='w')

        # ===== BUTTON FRAME =====
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill='x', padx=10, pady=10)

        ttk.Button(button_frame, text="➕ Add Student", command=self.add_student).pack(side='left', padx=5)
        ttk.Button(button_frame, text="✏️ Update Student", command=self.update_student).pack(side='left', padx=5)
        ttk.Button(button_frame, text="🗑️ Delete Student", command=self.delete_student).pack(side='left', padx=5)
        ttk.Button(button_frame, text="🗑️ Clear Fields", command=self.clear_fields).pack(side='left', padx=5)
        ttk.Button(button_frame, text="📥 Export to CSV", command=self.export_to_csv).pack(side='left', padx=5)
        ttk.Button(button_frame, text="❌ Exit", command=self.exit_application).pack(side='left', padx=5)

        # ===== TABLE FRAME - DISPLAY RECORDS =====
        table_frame = ttk.LabelFrame(self.root, text="Student Records", padding=10)
        table_frame.pack(pady=10, padx=10, fill='both', expand=True)

        # Create Treeview (table) to display records
        columns = tuple(TABLE_COLUMNS)
        self.tree = ttk.Treeview(table_frame, columns=columns, height=15, show='headings')

        # Define column headings and widths
        for col in TABLE_COLUMNS:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=COLUMN_WIDTHS.get(col, 100))

        # Bind double-click event to load selected record
        self.tree.bind('<Double-1>', self.on_tree_select)

        # Scrollbar for table
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def load_all_students(self):
        """
        Load and display all students from database in the table
        """
        for item in self.tree.get_children():
            self.tree.delete(item)

        students = self.db.get_all_students()
        for student in students:
            self.tree.insert('', 'end', values=student)

    def add_student(self):
        """
        Add a new student to the database
        Validates all required fields before adding
        """
        name = self.name_var.get().strip()
        age = self.age_var.get().strip()
        gender = self.gender_var.get().strip()
        course = self.course_var.get().strip()
        contact = self.contact_var.get().strip()
        email = self.email_var.get().strip()

        # Validation
        if not all([name, age, gender, course, contact, email]):
            messagebox.showerror("Validation Error", ERROR_EMPTY_FIELDS)
            return

        try:
            age = int(age)
            if age < MIN_AGE or age > MAX_AGE:
                messagebox.showerror("Validation Error", ERROR_INVALID_AGE.format(MIN_AGE, MAX_AGE))
                return
        except ValueError:
            messagebox.showerror("Validation Error", "Age must be a valid number!")
            return

        if not contact.isdigit() or len(contact) < MIN_CONTACT_LENGTH or len(contact) > MAX_CONTACT_LENGTH:
            messagebox.showerror("Validation Error", ERROR_INVALID_CONTACT.format(MIN_CONTACT_LENGTH, MAX_CONTACT_LENGTH))
            return

        if '@' not in email or '.' not in email:
            messagebox.showerror("Validation Error", ERROR_INVALID_EMAIL)
            return

        # Add student to database
        success, message = self.db.add_student(name, age, gender, course, contact, email)
        if success:
            messagebox.showinfo("Success", SUCCESS_ADD.format(name))
            self.clear_fields()
            self.load_all_students()
        else:
            messagebox.showerror("Error", message)

    def on_tree_select(self, event):
        """
        Handle double-click on tree item
        Loads selected student's data into input fields for editing
        """
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = selected_item[0]
        values = self.tree.item(item, 'values')

        self.selected_student_id = values[0]
        self.student_id_var.set(values[0])
        self.name_var.set(values[1])
        self.age_var.set(values[2])
        self.gender_var.set(values[3])
        self.course_var.set(values[4])
        self.contact_var.set(values[5])
        self.email_var.set(values[6])

    def update_student(self):
        """
        Update the selected student's information
        """
        if self.selected_student_id is None:
            messagebox.showwarning("Warning", ERROR_NO_SELECTION.format("update"))
            return

        name = self.name_var.get().strip()
        age = self.age_var.get().strip()
        gender = self.gender_var.get().strip()
        course = self.course_var.get().strip()
        contact = self.contact_var.get().strip()
        email = self.email_var.get().strip()

        # Validation
        if not all([name, age, gender, course, contact, email]):
            messagebox.showerror("Validation Error", ERROR_EMPTY_FIELDS)
            return

        try:
            age = int(age)
            if age < MIN_AGE or age > MAX_AGE:
                messagebox.showerror("Validation Error", ERROR_INVALID_AGE.format(MIN_AGE, MAX_AGE))
                return
        except ValueError:
            messagebox.showerror("Validation Error", "Age must be a valid number!")
            return

        if not contact.isdigit() or len(contact) < MIN_CONTACT_LENGTH or len(contact) > MAX_CONTACT_LENGTH:
            messagebox.showerror("Validation Error", ERROR_INVALID_CONTACT.format(MIN_CONTACT_LENGTH, MAX_CONTACT_LENGTH))
            return

        if '@' not in email or '.' not in email:
            messagebox.showerror("Validation Error", ERROR_INVALID_EMAIL)
            return

        # Update in database
        success, message = self.db.update_student(self.selected_student_id, name, age, gender, course, contact, email)
        if success:
            messagebox.showinfo("Success", SUCCESS_UPDATE)
            self.clear_fields()
            self.load_all_students()
            self.selected_student_id = None
        else:
            messagebox.showerror("Error", message)

    def delete_student(self):
        """
        Delete the selected student from database
        """
        if self.selected_student_id is None:
            messagebox.showwarning("Warning", ERROR_NO_SELECTION.format("delete"))
            return

        student_name = self.name_var.get()

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{student_name}'?"):
            success, message = self.db.delete_student(self.selected_student_id)
            if success:
                messagebox.showinfo("Success", SUCCESS_DELETE)
                self.clear_fields()
                self.load_all_students()
                self.selected_student_id = None
            else:
                messagebox.showerror("Error", message)

    def clear_fields(self):
        """
        Clear all input fields and deselect any selected student
        """
        self.student_id_var.set("")
        self.name_var.set("")
        self.age_var.set("")
        self.gender_var.set("")
        self.course_var.set("")
        self.contact_var.set("")
        self.email_var.set("")
        self.selected_student_id = None

    def on_search_change(self, *args):
        """
        Handle search field changes
        Updates table to show only matching students
        """
        search_term = self.search_var.get().strip()

        for item in self.tree.get_children():
            self.tree.delete(item)

        if search_term == "":
            self.load_all_students()
        else:
            results = self.db.search_student(search_term)
            for student in results:
                self.tree.insert('', 'end', values=student)

    def clear_search(self):
        """
        Clear search field and show all students
        """
        self.search_var.set("")
        self.load_all_students()

    def export_to_csv(self):
        """
        Export all student records to a CSV file
        """
        try:
            students = self.db.get_all_students()

            if not students:
                messagebox.showwarning("Warning", "No students to export!")
                return

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"students_export_{timestamp}.csv"

            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Student ID', 'Name', 'Age', 'Gender', 'Course', 'Contact', 'Email', 'Created Date'])
                writer.writerows(students)

            messagebox.showinfo("Success", SUCCESS_EXPORT.format(filename))
        except Exception as e:
            messagebox.showerror("Error", ERROR_EXPORT_FAILED.format(str(e)))

    def exit_application(self):
        """
        Close the application and database connection
        """
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.db.close_connection()
            self.root.quit()
