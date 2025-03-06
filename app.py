from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key

# Simulated Grok AI function (replace with actual API call in production)
def get_career_recommendation(data):
    skills = data.get('skills', '').lower()
    interests = data.get('interests', '').lower()
    education = data.get('education', '').lower()

    # Simple logic for demo purposes
    if 'programming' in skills or 'coding' in interests:
        career = "Software Developer"
        skills_needed = ["Python", "JavaScript", "Problem Solving"]
        market_trend = "High demand in tech industry"
    elif 'writing' in skills or 'communication' in interests:
        career = "Content Writer"
        skills_needed = ["SEO", "Grammar", "Creativity"]
        market_trend = "Growing demand in digital marketing"
    else:
        career = "General Analyst"
        skills_needed = ["Data Analysis", "Critical Thinking"]
        market_trend = "Stable demand across industries"

    return {
        "career": career,
        "skills_needed": skills_needed,
        "market_trend": market_trend
    }

# Load users from JSON file
def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return {}

# Save users to JSON file
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users:
            return "Username already exists"
        users[username] = {'password': password, 'profile': {}}
        save_users(users)
        session['username'] = username
        return redirect(url_for('home'))
    return render_template('signup.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        data = {
            'skills': request.form['skills'],
            'interests': request.form['interests'],
            'education': request.form['education']
        }
        users = load_users()
        users[session['username']]['profile'] = data
        save_users(users)
        return redirect(url_for('dashboard'))
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    users = load_users()
    profile = users[session['username']]['profile']
    recommendation = get_career_recommendation(profile)
    return render_template('dashboard.html', profile=profile, recommendation=recommendation)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)