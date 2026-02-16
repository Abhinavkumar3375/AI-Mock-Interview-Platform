from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import random

app = Flask(__name__)
app.secret_key = "secure_mock_ai_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# hello every one

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))

class InterviewSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    domain = db.Column(db.String(50))
    score = db.Column(db.Integer)
    total_questions = db.Column(db.Integer)
    result = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

# ------------------ MCQ QUESTIONS DATABASE ----------
MCQ_QUESTIONS = {
    "python": [
        {
            "question": "Which of the following is used to define a block of code in Python?",
            "options": ["Curly braces {}", "Indentation", "Parentheses ()", "Square brackets []"],
            "correct": 1
        },
        {
            "question": "What is the output of: print(type([]))?",
            "options": ["<class 'tuple'>", "<class 'list'>", "<class 'dict'>", "<class 'set'>"],
            "correct": 1
        },
        {
            "question": "Which keyword is used to create a function in Python?",
            "options": ["function", "def", "func", "define"],
            "correct": 1
        },
        {
            "question": "What does the 'self' keyword represent in Python class methods?",
            "options": ["The class itself", "The instance of the class", "A global variable", "A static method"],
            "correct": 1
        },
        {
            "question": "Which of these is NOT a valid Python data type?",
            "options": ["list", "tuple", "array", "dictionary"],
            "correct": 2
        },
        {
            "question": "What is the correct way to create a dictionary in Python?",
            "options": ["dict = []", "dict = {}", "dict = ()", "dict = <>"],
            "correct": 1
        },
        {
            "question": "Which method is used to add an element to a list?",
            "options": ["add()", "append()", "insert()", "push()"],
            "correct": 1
        },
        {
            "question": "What is the output of: bool('')?",
            "options": ["True", "False", "None", "Error"],
            "correct": 1
        },
        {
            "question": "Which module is used for regular expressions in Python?",
            "options": ["regex", "re", "regexp", "expression"],
            "correct": 1
        },
        {
            "question": "What does the 'with' statement do in Python?",
            "options": ["Creates a loop", "Handles exceptions", "Manages context and resources", "Defines a function"],
            "correct": 2
        },
        {
            "question": "Which of these is a mutable data type in Python?",
            "options": ["tuple", "string", "list", "integer"],
            "correct": 2
        },
        {
            "question": "What is the purpose of __init__ method in Python classes?",
            "options": ["To delete objects", "To initialize object attributes", "To print objects", "To copy objects"],
            "correct": 1
        },
        {
            "question": "Which operator is used for floor division in Python?",
            "options": ["/", "//", "%", "**"],
            "correct": 1
        },
        {
            "question": "What is a lambda function in Python?",
            "options": ["A named function", "An anonymous function", "A class method", "A built-in function"],
            "correct": 1
        },
        {
            "question": "Which of these is used to handle exceptions in Python?",
            "options": ["try-catch", "try-except", "catch-throw", "error-handle"],
            "correct": 1
        }
    ],
    "java": [
        {
            "question": "Which of these is NOT a Java access modifier?",
            "options": ["public", "private", "protected", "package"],
            "correct": 3
        },
        {
            "question": "What is the parent class of all classes in Java?",
            "options": ["System", "Object", "Class", "Main"],
            "correct": 1
        },
        {
            "question": "Which keyword is used to inherit a class in Java?",
            "options": ["implements", "inherits", "extends", "super"],
            "correct": 2
        },
        {
            "question": "What is the size of int data type in Java?",
            "options": ["8 bits", "16 bits", "32 bits", "64 bits"],
            "correct": 2
        },
        {
            "question": "Which of these is a marker interface in Java?",
            "options": ["Runnable", "Serializable", "Comparable", "Cloneable"],
            "correct": 1
        },
        {
            "question": "What does JVM stand for?",
            "options": ["Java Virtual Machine", "Java Variable Method", "Java Visual Machine", "Java Version Manager"],
            "correct": 0
        },
        {
            "question": "Which method is called when an object is created in Java?",
            "options": ["main()", "start()", "constructor", "init()"],
            "correct": 2
        },
        {
            "question": "What is the default value of a boolean variable in Java?",
            "options": ["true", "false", "null", "0"],
            "correct": 1
        },
        {
            "question": "Which collection class allows you to grow arrays in Java?",
            "options": ["Array", "ArrayList", "HashSet", "LinkedList"],
            "correct": 1
        },
        {
            "question": "What is polymorphism in Java?",
            "options": ["Having multiple constructors", "Ability to take many forms", "Inheriting properties", "Encapsulating data"],
            "correct": 1
        },
        {
            "question": "Which keyword is used to prevent method overriding?",
            "options": ["static", "final", "const", "sealed"],
            "correct": 1
        },
        {
            "question": "What is the difference between '==' and 'equals()' in Java?",
            "options": ["No difference", "== compares references, equals() compares values", "== is faster", "equals() is deprecated"],
            "correct": 1
        },
        {
            "question": "Which package contains the Scanner class?",
            "options": ["java.io", "java.util", "java.lang", "java.scanner"],
            "correct": 1
        },
        {
            "question": "What is encapsulation in OOP?",
            "options": ["Hiding implementation details", "Code reusability", "Multiple inheritance", "Runtime binding"],
            "correct": 0
        },
        {
            "question": "Which exception is thrown when dividing by zero?",
            "options": ["NullPointerException", "ArithmeticException", "NumberFormatException", "DivideByZeroException"],
            "correct": 1
        }
    ],
    "javascript": [
        {
            "question": "Which company developed JavaScript?",
            "options": ["Microsoft", "Netscape", "Google", "Mozilla"],
            "correct": 1
        },
        {
            "question": "What is the correct way to declare a variable in modern JavaScript?",
            "options": ["var x = 5", "let x = 5", "Both var and let", "declare x = 5"],
            "correct": 2
        },
        {
            "question": "Which method is used to parse a string to an integer?",
            "options": ["parseInt()", "parseInteger()", "toInt()", "convertInt()"],
            "correct": 0
        },
        {
            "question": "What does DOM stand for?",
            "options": ["Document Object Model", "Data Object Model", "Document Oriented Model", "Display Object Management"],
            "correct": 0
        },
        {
            "question": "Which symbol is used for comments in JavaScript?",
            "options": ["<!-- -->", "/* */", "//", "Both // and /* */"],
            "correct": 3
        },
        {
            "question": "What is the output of: typeof null?",
            "options": ["null", "object", "undefined", "number"],
            "correct": 1
        },
        {
            "question": "Which method removes the last element from an array?",
            "options": ["pop()", "push()", "shift()", "unshift()"],
            "correct": 0
        },
        {
            "question": "What is a closure in JavaScript?",
            "options": ["A function with no parameters", "A function that returns another function", "A function that has access to outer function variables", "A built-in method"],
            "correct": 2
        },
        {
            "question": "Which of these is NOT a JavaScript framework/library?",
            "options": ["React", "Angular", "Django", "Vue"],
            "correct": 2
        },
        {
            "question": "What does JSON stand for?",
            "options": ["JavaScript Object Notation", "Java Standard Object Notation", "JavaScript Oriented Network", "Java Serialized Object Notation"],
            "correct": 0
        },
        {
            "question": "Which method is used to add elements to the beginning of an array?",
            "options": ["push()", "pop()", "unshift()", "shift()"],
            "correct": 2
        },
        {
            "question": "What is the purpose of 'use strict' in JavaScript?",
            "options": ["Improves performance", "Enables strict mode for error checking", "Compresses code", "Adds security"],
            "correct": 1
        },
        {
            "question": "Which operator is used to compare both value and type?",
            "options": ["==", "===", "!=", "!=="],
            "correct": 1
        },
        {
            "question": "What is an arrow function in ES6?",
            "options": ["A function that points to objects", "A shorter syntax for writing functions", "A function for arrays only", "A deprecated feature"],
            "correct": 1
        },
        {
            "question": "Which method is used to iterate over array elements?",
            "options": ["loop()", "forEach()", "iterate()", "each()"],
            "correct": 1
        }
    ],
    "database": [
        {
            "question": "What does SQL stand for?",
            "options": ["Structured Query Language", "Simple Query Language", "Standard Question Language", "Sequential Query Language"],
            "correct": 0
        },
        {
            "question": "Which command is used to retrieve data from a database?",
            "options": ["GET", "SELECT", "RETRIEVE", "FETCH"],
            "correct": 1
        },
        {
            "question": "What is a primary key?",
            "options": ["A key used for encryption", "A unique identifier for a record", "The first column in a table", "A foreign key reference"],
            "correct": 1
        },
        {
            "question": "Which SQL clause is used to filter results?",
            "options": ["FILTER", "WHERE", "HAVING", "WHEN"],
            "correct": 1
        },
        {
            "question": "What does ACID stand for in databases?",
            "options": ["Atomicity, Consistency, Isolation, Durability", "Access, Control, Integration, Data", "Automatic, Consistent, Independent, Direct", "None of the above"],
            "correct": 0
        },
        {
            "question": "Which type of JOIN returns all records from both tables?",
            "options": ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN"],
            "correct": 3
        },
        {
            "question": "What is normalization in databases?",
            "options": ["Making data normal", "Organizing data to reduce redundancy", "Encrypting data", "Backing up data"],
            "correct": 1
        },
        {
            "question": "Which command is used to add new records to a table?",
            "options": ["ADD", "INSERT", "CREATE", "UPDATE"],
            "correct": 1
        },
        {
            "question": "What is an index in a database?",
            "options": ["A table of contents", "A data structure that improves query speed", "A backup copy", "A foreign key"],
            "correct": 1
        },
        {
            "question": "Which is NOT a type of NoSQL database?",
            "options": ["Document", "Key-Value", "Relational", "Graph"],
            "correct": 2
        },
        {
            "question": "What does DDL stand for?",
            "options": ["Data Definition Language", "Database Description Language", "Data Display Language", "Direct Data Language"],
            "correct": 0
        },
        {
            "question": "Which constraint ensures that a column cannot have NULL values?",
            "options": ["UNIQUE", "CHECK", "NOT NULL", "PRIMARY KEY"],
            "correct": 2
        },
        {
            "question": "What is a foreign key?",
            "options": ["A key from another country", "A link between two tables", "An encrypted key", "A duplicate key"],
            "correct": 1
        },
        {
            "question": "Which command is used to modify existing records?",
            "options": ["MODIFY", "CHANGE", "UPDATE", "ALTER"],
            "correct": 2
        },
        {
            "question": "What is a stored procedure?",
            "options": ["A saved query", "A precompiled SQL code that can be executed", "A backup method", "A data type"],
            "correct": 1
        }
    ],
    "hr": [
        {
            "question": "What is the most important quality for teamwork?",
            "options": ["Individual brilliance", "Communication and collaboration", "Working independently", "Competing with teammates"],
            "correct": 1
        },
        {
            "question": "How do you handle constructive criticism?",
            "options": ["Ignore it", "Get defensive", "Listen and learn from it", "Argue against it"],
            "correct": 2
        },
        {
            "question": "What motivates you most at work?",
            "options": ["Only salary", "Challenges and growth opportunities", "Easy tasks", "Minimal responsibility"],
            "correct": 1
        },
        {
            "question": "How do you prioritize tasks when you have multiple deadlines?",
            "options": ["Do easiest tasks first", "Do hardest tasks first", "Assess urgency and importance", "Work randomly"],
            "correct": 2
        },
        {
            "question": "What would you do if you disagreed with your manager?",
            "options": ["Stay silent", "Complain to colleagues", "Respectfully discuss concerns", "Quit immediately"],
            "correct": 2
        },
        {
            "question": "How do you handle stress and pressure?",
            "options": ["Avoid it completely", "Break down and panic", "Use time management and stay organized", "Procrastinate"],
            "correct": 2
        },
        {
            "question": "Why are you interested in this position?",
            "options": ["Just need any job", "Matches my skills and career goals", "High salary only", "Close to home"],
            "correct": 1
        },
        {
            "question": "How do you handle failure?",
            "options": ["Blame others", "Give up", "Learn from it and improve", "Deny it happened"],
            "correct": 2
        },
        {
            "question": "What is your greatest professional strength?",
            "options": ["Being punctual", "Problem-solving and adaptability", "Following orders only", "Avoiding challenges"],
            "correct": 1
        },
        {
            "question": "How do you stay updated with industry trends?",
            "options": ["I don't", "Only during interviews", "Regular learning and networking", "Wait for training"],
            "correct": 2
        },
        {
            "question": "What would you do if assigned a task you've never done before?",
            "options": ["Refuse it", "Fake knowledge", "Research, ask questions, and learn", "Do it incorrectly"],
            "correct": 2
        },
        {
            "question": "How do you contribute to a positive work environment?",
            "options": ["Keep to myself", "Gossip about others", "Be supportive and respectful", "Create conflicts"],
            "correct": 2
        },
        {
            "question": "What do you consider when accepting a job offer?",
            "options": ["Only salary", "Growth, culture, and learning opportunities", "Just the title", "Location only"],
            "correct": 1
        },
        {
            "question": "How do you balance work and personal life?",
            "options": ["Work 24/7", "Only focus on personal life", "Set boundaries and manage time effectively", "Ignore personal life"],
            "correct": 2
        },
        {
            "question": "What does professional development mean to you?",
            "options": ["Getting promotions only", "Continuous learning and skill improvement", "Doing minimum work", "Waiting for opportunities"],
            "correct": 1
        }
    ]
}

# ------------------ ROUTES ------------------
@app.route("/")
def home():
    return render_template("login.html")

# -------- AUTH --------
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "Email already registered. Please login."
        
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect("/")
    return render_template("register.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    
    if user and check_password_hash(user.password, password):
        session['user'] = user.id
        session['user_name'] = user.name
        return redirect("/dashboard")
    return "Invalid Login Credentials"

# -------- DASHBOARD --------
@app.route("/dashboard")
def dashboard():
    if 'user' not in session:
        return redirect("/")
    
    # Get user's past interview sessions
    past_sessions = InterviewSession.query.filter_by(user_id=session['user']).order_by(InterviewSession.timestamp.desc()).limit(5).all()
    
    return render_template("dashboard.html", 
                         user_name=session.get('user_name'),
                         past_sessions=past_sessions)

# -------- INTERVIEW ENGINE --------
@app.route("/start_interview", methods=["POST"])
def start_interview():
    domain = request.form['domain']
    
    if domain not in MCQ_QUESTIONS:
        return "Invalid domain selected"
    
    # Select 10 random questions from the domain
    all_questions = MCQ_QUESTIONS[domain]
    selected_questions = random.sample(all_questions, min(10, len(all_questions)))
    
    session['domain'] = domain
    session['questions'] = selected_questions
    session['user_answers'] = []
    session['q_index'] = 0
    
    return redirect("/interview")

@app.route("/interview", methods=["GET", "POST"])
def interview():
    if 'user' not in session:
        return redirect("/")
    
    if 'questions' not in session:
        return redirect("/dashboard")
    
    if request.method == "POST":
        # Store the user's answer
        answer = int(request.form.get('answer', -1))
        session['user_answers'].append(answer)
        session['q_index'] += 1
        session.modified = True
    
    q_index = session['q_index']
    questions = session['questions']
    
    # Check if interview is complete
    if q_index >= len(questions):
        return redirect("/result")
    
    current_question = questions[q_index]
    
    return render_template("interview.html", 
                         question=current_question['question'],
                         options=current_question['options'],
                         q_number=q_index + 1,
                         total_questions=len(questions))

# -------- RESULT ENGINE --------
@app.route("/result")
def result():
    if 'user' not in session or 'questions' not in session:
        return redirect("/dashboard")
    
    questions = session['questions']
    user_answers = session['user_answers']
    
    # Calculate score
    correct_count = 0
    for i, question in enumerate(questions):
        if i < len(user_answers) and user_answers[i] == question['correct']:
            correct_count += 1
    
    total_questions = len(questions)
    score = (correct_count / total_questions) * 100
    
    # Determine result category
    if score >= 80:
        result_text = "Excellent"
    elif score >= 60:
        result_text = "Good"
    elif score >= 40:
        result_text = "Average"
    else:
        result_text = "Needs Improvement"
    
    # Save to database
    session_db = InterviewSession(
        user_id=session['user'],
        domain=session['domain'],
        score=int(score),
        total_questions=total_questions,
        result=result_text
    )
    db.session.add(session_db)
    db.session.commit()
    
    # Clear session data
    session.pop('questions', None)
    session.pop('user_answers', None)
    session.pop('q_index', None)
    session.pop('domain', None)
    
    return render_template("result.html", 
                         score=int(score),
                         correct=correct_count,
                         total=total_questions,
                         result=result_text)

# -------- LOGOUT --------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ------------------ RUN ------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)





