CREATE TABLE Students (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT
);

CREATE TABLE Quizzes (
    id INTEGER PRIMARY KEY,
    subject TEXT,
    num_questions INTEGER,
    quiz_date TEXT
);

CREATE TABLE Results (
    student_id INTEGER,
    quiz_id INTEGER,
    score INTEGER,
    FOREIGN KEY (student_id) REFERENCES Students(id),
    FOREIGN KEY (quiz_id) REFERENCES Quizzes(id),
    PRIMARY KEY (student_id, quiz_id)
);
