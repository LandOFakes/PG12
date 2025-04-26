
from flask import render_template, request, redirect, url_for, session, sqlite3
from app import app  # Import the app instance
from functools import wraps


def get_db_connection():
    conn = sqlite3.connect('hw13.db')
    conn.row_factory = sqlite3.Row  #  Return rows as dictionaries
    return conn


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    students = conn.execute("SELECT id, first_name, last_name FROM Students").fetchall()
    quizzes = conn.execute("SELECT id, subject, num_questions, quiz_date FROM Quizzes").fetchall()
    conn.close()
    return render_template('dashboard.html', students=students, quizzes=quizzes)

@app.route('/student/add', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO Students (first_name, last_name) VALUES (?, ?)", (first_name, last_name))
            conn.commit()
            return redirect(url_for('dashboard'))
        except sqlite3.Error as e:
            return render_template('add_student.html', error=str(e), first_name=first_name, last_name=last_name)
        finally:
            conn.close()
    return render_template('add_student.html')

@app.route('/quiz/add', methods=['GET', 'POST'])
@login_required
def add_quiz():
    if request.method == 'POST':
        subject = request.form['subject']
        num_questions = int(request.form['num_questions'])
        quiz_date = request.form['quiz_date']
        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO Quizzes (subject, num_questions, quiz_date) VALUES (?, ?, ?)", (subject, num_questions, quiz_date))
            conn.commit()
            return redirect(url_for('dashboard'))
        except sqlite3.Error as e:
            return render_template('add_quiz.html', error=str(e), subject=subject, num_questions=num_questions, quiz_date=quiz_date)
        finally:
            conn.close()
    return render_template('add_quiz.html')

@app.route('/student/<int:student_id>')
@login_required
def student_results(student_id):
    conn = get_db_connection()
    results = conn.execute("""
        SELECT Q.subject, R.score
        FROM Results R
        JOIN Quizzes Q ON R.quiz_id = Q.id
        WHERE R.student_id = ?
    """, (student_id,)).fetchall()
    conn.close()
    return render_template('student_results.html', student_id=student_id, results=results)
