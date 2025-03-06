from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key

# Enhanced AI recommendation function
def get_career_recommendation(data):
    skills = data.get('skills', '').lower()
    interests = data.get('interests', '').lower()
    education = data.get('education', '').lower()

    # Expanded logic with multiple conditions
    if 'programming' in skills or 'coding' in interests:
        career = "Software Developer"
        skills_needed = ["Python", "JavaScript", "Problem Solving"]
        market_trend = "High demand in tech industry, especially for AI and cloud computing"
    elif 'writing' in skills or 'communication' in interests:
        if 'marketing' in interests:
            career = "Digital Marketing Specialist"
            skills_needed = ["SEO", "Content Creation", "Analytics"]
            market_trend = "Growing demand due to online business expansion"
        else:
            career = "Content Writer"
            skills_needed = ["SEO", "Grammar", "Creativity"]
            market_trend = "Stable demand in digital content creation"
    elif 'design' in skills or 'art' in interests:
        if 'graphic' in skills or 'ui' in interests:
            career = "UI/UX Designer"
            skills_needed = ["Figma", "Adobe XD", "User Research"]
            market_trend = "Rising need for user-friendly digital interfaces"
        else:
            career = "Graphic Designer"
            skills_needed = ["Photoshop", "Illustrator", "Creativity"]
            market_trend = "Consistent demand in advertising and media"
    elif 'data' in skills or 'analysis' in interests:
        if 'statistics' in skills or 'math' in education:
            career = "Data Scientist"
            skills_needed = ["Python", "R", "Machine Learning"]
            market_trend = "Booming field with applications in all industries"
        else:
            career = "Data Analyst"
            skills_needed = ["Excel", "SQL", "Data Visualization"]
            market_trend = "High demand in business intelligence"
    elif 'teaching' in skills or 'education' in interests:
        career = "Educator/Trainer"
        skills_needed = ["Communication", "Subject Expertise", "Patience"]
        market_trend = "Steady demand in schools and corporate training"
    elif 'business' in skills or 'management' in interests:
        if 'mba' in education or 'masters' in education:
            career = "Business Manager"
            skills_needed = ["Leadership", "Strategic Planning", "Finance"]
            market_trend = "Strong demand in corporate leadership roles"
        else:
            career = "Entrepreneur"
            skills_needed = ["Risk Taking", "Marketing", "Networking"]
            market_trend = "Growing opportunities with startup culture"
    elif 'health' in skills or 'medicine' in interests:
        if 'nursing' in education or 'medical' in education:
            career = "Nurse Practitioner"
            skills_needed = ["Patient Care", "Medical Knowledge", "Empathy"]
            market_trend = "Critical demand in healthcare sectors"
        else:
            career = "Healthcare Assistant"
            skills_needed = ["Basic Medical Skills", "Compassion", "Teamwork"]
            market_trend = "Stable growth in support roles"
    elif 'engineering' in skills or 'technology' in interests:
        if 'mechanical' in education:
            career = "Mechanical Engineer"
            skills_needed = ["CAD", "Thermodynamics", "Problem Solving"]
            market_trend = "Demand in manufacturing and automotive industries"
        elif 'electrical' in education:
            career = "Electrical Engineer"
            skills_needed = ["Circuit Design", "Programming", "Troubleshooting"]
            market_trend = "Growth in renewable energy and electronics"
        else:
            career = "Technical Support Specialist"
            skills_needed = ["IT Skills", "Customer Service", "Problem Solving"]
            market_trend = "Consistent need in tech support"
    elif 'sales' in skills or 'negotiation' in interests:
        career = "Sales Representative"
        skills_needed = ["Communication", "Persuasion", "CRM Tools"]
        market_trend = "Evergreen field across industries"
    elif 'music' in skills or 'performance' in interests:
        career = "Musician/Performer"
        skills_needed = ["Instrument Proficiency", "Stage Presence", "Creativity"]
        market_trend = "Niche but viable with digital platforms"
    else:
        # Default fallback for unrecognized inputs
        career = "Career Explorer"
        skills_needed = ["Adaptability", "Learning Agility", "Curiosity"]
        market_trend = "Explore various fields to find your passion"

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