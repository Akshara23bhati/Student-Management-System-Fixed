"""
DATABASE MANAGEMENT MODULE
Handles all database operations for the Student Management System
"""

import sqlite3
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    This class handles all database operations including:
    - Creating database and tables
    - Adding, updating, deleting, and searching students
    - Fetching all student records
    """

    def __init__(self, db_name="student_database.db"):
        """
        Initialize the database connection and create tables if they don't exist

        Args:
            db_name (str): Name of the database file
        """
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.connect_database()
        self.create_table()

    def connect_database(self):
        """
        Establish connection to SQLite database
        Creates new database if it doesn't exist
        """
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            logger.info("✓ Database connection successful")
        except sqlite3.Error as e:
            logger.error(f"✗ Database connection error: {e}")
            raise

    def create_table(self):
        """
        Create the 'students' table if it doesn't exist
        """
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                course TEXT NOT NULL,
                contact TEXT NOT NULL,
                email TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            self.cursor.execute(create_table_query)
            self.connection.commit()
            logger.info("✓ Students table created/verified successfully")
        except sqlite3.Error as e:
            logger.error(f"✗ Table creation error: {e}")
            raise

    def add_student(self, name, age, gender, course, contact, email):
        """
        Add a new student record to the database

        Args:
            name (str): Student's name
            age (int): Student's age
            gender (str): Student's gender
            course (str): Course enrolled
            contact (str): Contact number
            email (str): Email address

        Returns:
            tuple: (bool, str) - (success status, message)
        """
        try:
            insert_query = """
            INSERT INTO students (name, age, gender, course, contact, email)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(insert_query, (name, age, gender, course, contact, email))
            self.connection.commit()
            return True, "Student added successfully"
        except sqlite3.Error as e:
            logger.error(f"✗ Error adding student: {e}")
            return False, f"Error adding student: {e}"

    def get_all_students(self):
        """
        Fetch all student records from database

        Returns:
            list: List of tuples containing all student records
        """
        try:
            select_query = "SELECT * FROM students ORDER BY student_id DESC"
            self.cursor.execute(select_query)
            students = self.cursor.fetchall()
            return students
        except sqlite3.Error as e:
            logger.error(f"✗ Error fetching students: {e}")
            return []

    def search_student(self, search_term):
        """
        Search for students by name, email, or contact number

        Args:
            search_term (str): The search keyword

        Returns:
            list: List of matching student records
        """
        try:
            search_query = """
            SELECT * FROM students 
            WHERE name LIKE ? OR email LIKE ? OR contact LIKE ? OR student_id = ?
            """
            term = f"%{search_term}%"
            try:
                student_id = int(search_term)
            except ValueError:
                student_id = -1

            self.cursor.execute(search_query, (term, term, term, student_id))
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            logger.error(f"✗ Error searching student: {e}")
            return []

    def update_student(self, student_id, name, age, gender, course, contact, email):
        """
        Update an existing student's record

        Args:
            student_id (int): ID of student to update
            name (str): Updated name
            age (int): Updated age
            gender (str): Updated gender
            course (str): Updated course
            contact (str): Updated contact
            email (str): Updated email

        Returns:
            tuple: (bool, str) - (success status, message)
        """
        try:
            update_query = """
            UPDATE students 
            SET name=?, age=?, gender=?, course=?, contact=?, email=?
            WHERE student_id=?
            """
            self.cursor.execute(update_query, (name, age, gender, course, contact, email, student_id))
            self.connection.commit()
            return True, "Student updated successfully"
        except sqlite3.Error as e:
            logger.error(f"✗ Error updating student: {e}")
            return False, f"Error updating student: {e}"

    def delete_student(self, student_id):
        """
        Delete a student record from database

        Args:
            student_id (int): ID of student to delete

        Returns:
            tuple: (bool, str) - (success status, message)
        """
        try:
            delete_query = "DELETE FROM students WHERE student_id=?"
            self.cursor.execute(delete_query, (student_id,))
            self.connection.commit()
            return True, "Student deleted successfully"
        except sqlite3.Error as e:
            logger.error(f"✗ Error deleting student: {e}")
            return False, f"Error deleting student: {e}"

    def close_connection(self):
        """Close the database connection"""
        try:
            if self.connection:
                self.connection.close()
                logger.info("✓ Database connection closed")
        except sqlite3.Error as e:
            logger.error(f"✗ Error closing connection: {e}")
