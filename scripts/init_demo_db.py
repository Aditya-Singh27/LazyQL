import sqlite3
from pathlib import Path


# Find the root directory of our project
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Location where our SQLite database will be stored
DATABASE_PATH = PROJECT_ROOT / "database" / "company.db"


def create_database():
    # Connect to SQLite database
    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()   # allow pyhton to send sql commands to DB

    # Create departments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            location TEXT NOT NULL
        )
    """)

    # Create employees table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            salary INTEGER NOT NULL,
            joining_date TEXT NOT NULL
        )
    """)

    # Insert departments
    cursor.executemany("""
        INSERT OR IGNORE INTO departments
        (id, name, location)
        VALUES (?, ?, ?)
    """, [
        (1, "IT", "Delhi"),
        (2, "HR", "Mumbai"),
        (3, "Finance", "Bangalore"),
        (4, "Marketing", "Pune"),
    ])

    # Insert employees
    cursor.executemany("""
        INSERT OR IGNORE INTO employees
        (id, name, department, salary, joining_date)
        VALUES (?, ?, ?, ?, ?)
    """, [
        (1, "Aditya", "IT", 1200000, "2024-07-01"),
        (2, "Rahul", "HR", 800000, "2023-05-15"),
        (3, "Aman", "IT", 1500000, "2022-03-10"),
        (4, "Priya", "Finance", 1100000, "2024-01-20"),
        (5, "Neha", "Marketing", 950000, "2023-11-05"),
        (6, "Rohit", "IT", 1300000, "2021-08-12"),
        (7, "Sneha", "HR", 900000, "2024-02-18"),
        (8, "Vikas", "Finance", 1250000, "2022-09-25"),
    ])

    # Save changes
    connection.commit()

    # Close database connection
    connection.close()

    print("Database created successfully!")
    print(f"Location: {DATABASE_PATH}")


if __name__ == "__main__":
    create_database()