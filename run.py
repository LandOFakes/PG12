import sqlite3
from app import app  # Import the Flask app

def initialize_database():
    conn = sqlite3.connect('hw13.db')
    cursor = conn.cursor()

    # Create tables (execute the SQL from schema.sql)
    with open('schema.sql', 'r') as f:
        cursor.executescript(f.read())

    # Insert initial data
    cursor.execute("INSERT INTO Students (first_name, last_name) VALUES (?, ?)", ('John', 'Smith'))
    cursor.execute("INSERT INTO Quizzes (subject, num_questions, quiz_date) VALUES (?, ?, ?)", ('Python Basics', 5, '2015-02-05'))  # Store date as YYYY-MM-DD
    cursor.execute("INSERT INTO Results (student_id, quiz_id, score) VALUES (?, ?, ?)", (1, 1, 85))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_database()  # Initialize the database
    app.run(debug=True)     # Then run the Flask app
