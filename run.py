import sqlite3
import os  # Import the os module
from app import app

def initialize_database():
    if not os.path.exists('hw13.db'):  # Check if the file exists
        conn = sqlite3.connect('hw13.db')
        cursor = conn.cursor()

        # Create tables
        with open('schema.sql', 'r') as f:
            cursor.executescript(f.read())

        # Initial data
        cursor.execute("INSERT INTO Students (first_name, last_name) VALUES (?, ?)", ('John', 'Smith'))
        cursor.execute("INSERT INTO Quizzes (subject, num_questions, quiz_date) VALUES (?, ?, ?)", ('Python Basics', 5, '2015-02-05'))
        cursor.execute("INSERT INTO Results (student_id, quiz_id, score) VALUES (?, ?, ?)", (1, 1, 85))

        conn.commit()
        conn.close()

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
