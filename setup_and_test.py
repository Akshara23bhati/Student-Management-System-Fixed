"""
SETUP AND TESTING SCRIPT
This script:
1. Creates the database and tables
2. Adds sample student records for testing
3. Demonstrates database operations
"""

from database_manager import DatabaseManager
from datetime import datetime


def create_database():
    """
    Create database and students table
    """
    try:
        db = DatabaseManager('student_database.db')
        print("✓ Database created successfully!")
        return db
    except Exception as e:
        print(f"✗ Error creating database: {e}")
        return None


def add_sample_students(db):
    """
    Add sample student records for testing
    """
    sample_students = [
        ('Akshara Bhati', 20, 'Female', 'Python', '9876543210', 'akshara@email.com'),
        ('Rajesh Kumar', 22, 'Male', 'Java', '9765432109', 'rajesh@email.com'),
        ('Priya Singh', 19, 'Female', 'Web Dev', '9654321098', 'priya@email.com'),
        ('Arjun Patel', 21, 'Male', 'Data Science', '9543210987', 'arjun@email.com'),
        ('Sneha Sharma', 20, 'Female', 'C++', '9432109876', 'sneha@email.com'),
        ('Vikram Rao', 23, 'Male', 'Python', '9321098765', 'vikram@email.com'),
        ('Anaya Gupta', 20, 'Female', 'Web Dev', '9210987654', 'anaya@email.com'),
        ('Rohan Sinha', 22, 'Male', 'Data Science', '9109876543', 'rohan@email.com'),
    ]

    for student in sample_students:
        success, message = db.add_student(*student)
        if success:
            print(f"✓ Created demo user: {student[0]}")
        else:
            print(f"✗ Error creating user: {message}")


def display_all_students(db):
    """
    Display all students in the database
    """
    try:
        students = db.get_all_students()

        print("\n" + "="*100)
        print(f"Total Students: {len(students)}")
        print("="*100)
        print(f"{'ID':<5} {'Name':<20} {'Age':<5} {'Gender':<10} {'Course':<15} {'Contact':<12} {'Email':<30}")
        print("-"*100)

        for student in students:
            print(f"{student[0]:<5} {student[1]:<20} {student[2]:<5} {student[3]:<10} {student[4]:<15} {student[5]:<12} {student[6]:<30}")

        print("="*100 + "\n")
    except Exception as e:
        print(f"✗ Error displaying students: {e}")


def main():
    """
    Main setup and testing function
    """
    print("\n" + "="*100)
    print("STUDENT DATA MANAGEMENT SYSTEM - SETUP AND TESTING")
    print("="*100 + "\n")

    # Create database
    print("Step 1: Creating database and table...")
    db = create_database()

    if db is None:
        print("Failed to create database. Exiting...")
        return

    # Add sample students
    print("\nStep 2: Adding sample student records...")
    add_sample_students(db)

    # Display all students
    print("\nStep 3: Displaying all students...")
    display_all_students(db)

    # Close connection
    db.close_connection()

    print("✓ Setup and testing completed successfully!")
    print("You can now run 'python main.py' to start the application.\n")


if __name__ == "__main__":
    main()
