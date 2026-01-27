from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import random

app = Flask(__name__)
app.secret_key = "secure_mock_ai_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ------------------ MODELS ------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))

class InterviewSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    score = db.Column(db.Integer)
    result = db.Column(db.String(100))

# ------------------ QUESTIONS DB ------------------

QUESTIONS = {
    "python": [
        "What is Python?",
        "Explain list vs tuple.",
        "What is OOP?",
        "Explain decorators.",
        "What is multithreading?"
    ],
    "java": [
        "What is JVM?",
        "Explain OOP concepts.",
        "What is inheritance?",
        "What is exception handling?",
        "Difference between JDK and JRE?"
    ],
    "hr": [
        "Tell me about yourself.",
        "Why should we hire you?",
        "What are your strengths?",
        "What are your weaknesses?",
        "Where do you see yourself in 5 years?"
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

        user = User(name=name,email=email,password=password)
        db.session.add(user)
        db.session.commit()
        return redirect("/")

    return render_template("register.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password,password):
        session['user'] = user.id
        return redirect("/dashboard")
    return "Invalid Login"

# -------- DASHBOARD --------

@app.route("/dashboard")
def dashboard():
    if 'user' not in session:
        return redirect("/")
    return render_template("dashboard.html")

# -------- INTERVIEW ENGINE --------

@app.route("/start_interview", methods=["POST"])
def start_interview():
    domain = request.form['domain']
    questions = random.sample(QUESTIONS[domain], 5)
    session['questions'] = questions
    session['answers'] = []
    session['q_index'] = 0
    return redirect("/interview")

@app.route("/interview", methods=["GET","POST"])
def interview():
    if request.method == "POST":
        ans = request.form['answer']
        session['answers'].append(ans)
        session['q_index'] += 1

    q_index = session['q_index']
    questions = session['questions']

    if q_index >= len(questions):
        return redirect("/result")

    return render_template("interview.html", question=questions[q_index])

# -------- RESULT ENGINE --------

@app.route("/result")
def result():
    answers = session['answers']

    # Simple AI Scoring Logic (Rule-based placeholder)
    score = 0
    for ans in answers:
        if len(ans.split()) > 8:
            score += 20
        else:
            score += 10

    result_text = "Excellent" if score >= 80 else "Good" if score >= 60 else "Needs Improvement"

    session_db = InterviewSession(
        user_id=session['user'],
        score=score,
        result=result_text
    )

    db.session.add(session_db)
    db.session.commit()

    return render_template("result.html", score=score, result=result_text)

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
