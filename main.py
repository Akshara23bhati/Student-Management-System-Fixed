"""
MAIN APPLICATION ENTRY POINT
Student Data Management System
"""

import tkinter as tk
from student_management_gui import StudentManagementGUI


def main():
    """
    Main function to start the application
    """
    root = tk.Tk()
    app = StudentManagementGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
