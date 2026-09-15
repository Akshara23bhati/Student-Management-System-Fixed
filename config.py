"""
CONFIGURATION FILE
This file contains all configurable constants for the application
Change these values to customize the application behavior
"""

# ===== DATABASE CONFIGURATION =====
DATABASE_NAME = "student_database.db"
DATABASE_TABLE = "students"

# ===== GUI CONFIGURATION =====
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
WINDOW_TITLE = "Student Data Management System"
WINDOW_RESIZABLE = False

# ===== STYLE CONFIGURATION =====
DEFAULT_FONT = ('Arial', 10)
HEADING_FONT = ('Arial', 10, 'bold')
TITLE_FONT = ('Arial', 14, 'bold')

# ===== VALIDATION CONFIGURATION =====
MIN_AGE = 5
MAX_AGE = 100
MIN_CONTACT_LENGTH = 10
MAX_CONTACT_LENGTH = 15

# ===== COURSES AVAILABLE =====
AVAILABLE_COURSES = ['Python', 'Java', 'Web Dev', 'Data Science', 'C++', 'Other']

# ===== GENDER OPTIONS =====
GENDER_OPTIONS = ['Male', 'Female', 'Other']

# ===== MESSAGES =====
SUCCESS_ADD = "Student '{}' added successfully!"
SUCCESS_UPDATE = "Student record updated successfully!"
SUCCESS_DELETE = "Student deleted successfully!"
SUCCESS_EXPORT = "Data exported successfully! File: {}"

ERROR_EMPTY_FIELDS = "Please fill in all fields!"
ERROR_INVALID_AGE = "Age must be between {} and {}!"
ERROR_INVALID_CONTACT = "Contact must be {}-{} digits!"
ERROR_INVALID_EMAIL = "Please enter a valid email address!"
ERROR_NO_SELECTION = "Please select a student to {}!"
ERROR_ADD_FAILED = "Failed to add student. Please try again!"
ERROR_UPDATE_FAILED = "Failed to update student. Please try again!"
ERROR_DELETE_FAILED = "Failed to delete student. Please try again!"
ERROR_EXPORT_FAILED = "Failed to export data: {}"

# ===== TABLE CONFIGURATION =====
TABLE_COLUMNS = ['ID', 'Name', 'Age', 'Gender', 'Course', 'Contact', 'Email', 'Date']
COLUMN_WIDTHS = {
    'ID': 70,
    'Name': 120,
    'Age': 50,
    'Gender': 70,
    'Course': 100,
    'Contact': 100,
    'Email': 150,
    'Date': 120
}
