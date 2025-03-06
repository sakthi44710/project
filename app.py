from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key

def get_career_recommendation(data):
    skills = data.get('skills', '').lower()
    interests = data.get('interests', '').lower()
    education = data.get('education', '').lower()

    if 'programming' in skills or 'coding' in interests:
        career = "Software Developer"
        skills_needed = ["Python", "JavaScript", "Problem Solving"]
        market_trend = "High demand in tech industry"
        career_path = [
            "Learn programming basics (e.g., Python, JavaScript)",
            "Build small projects (e.g., web apps, games)",
            "Secure an internship or junior developer role",
            "Advance to mid-level or specialize (e.g., AI, backend)"
        ]
    elif 'writing' in skills or 'communication' in interests:
        if 'marketing' in interests:
            career = "Digital Marketing Specialist"
            skills_needed = ["SEO", "Content Creation", "Analytics"]
            market_trend = "Growing demand due to online business expansion"
            career_path = [
                "Learn digital marketing basics (SEO, Google Analytics)",
                "Create a portfolio of marketing campaigns",
                "Gain experience through freelance or agency work",
                "Lead marketing strategies for a company"
            ]
        else:
            career = "Content Writer"
            skills_needed = ["SEO", "Grammar", "Creativity"]
            market_trend = "Stable demand in digital content creation"
            career_path = [
                "Master writing and editing skills",
                "Build a portfolio of articles or blogs",
                "Freelance or join a content team",
                "Become a senior writer or editor"
            ]
    elif 'design' in skills or 'art' in interests:
        if 'graphic' in skills or 'ui' in interests:
            career = "UI/UX Designer"
            skills_needed = ["Figma", "Adobe XD", "User Research"]
            market_trend = "Rising need for user-friendly digital interfaces"
            career_path = [
                "Learn design tools (Figma, Adobe XD)",
                "Study user experience principles",
                "Create mockups and prototypes",
                "Work as a UI/UX designer in tech or freelance"
            ]
        else:
            career = "Graphic Designer"
            skills_needed = ["Photoshop", "Illustrator", "Creativity"]
            market_trend = "Consistent demand in advertising and media"
            career_path = [
                "Learn graphic design software (Photoshop, Illustrator)",
                "Build a portfolio of designs",
                "Freelance or join a design agency",
                "Specialize in branding or multimedia"
            ]
    elif 'data' in skills or 'analysis' in interests:
        if 'statistics' in skills or 'math' in education:
            career = "Data Scientist"
            skills_needed = ["Python", "R", "Machine Learning"]
            market_trend = "Booming field with applications in all industries"
            career_path = [
                "Learn data science tools (Python, R)",
                "Master statistics and machine learning",
                "Work on real-world data projects",
                "Become a lead data scientist or researcher"
            ]
        else:
            career = "Data Analyst"
            skills_needed = ["Excel", "SQL", "Data Visualization"]
            market_trend = "High demand in business intelligence"
            career_path = [
                "Learn Excel and SQL basics",
                "Practice data visualization (e.g., Tableau)",
                "Analyze data for a company or client",
                "Advance to senior analyst or BI roles"
            ]
    elif 'teaching' in skills or 'education' in interests:
        career = "Educator/Trainer"
        skills_needed = ["Communication", "Subject Expertise", "Patience"]
        market_trend = "Steady demand in schools and corporate training"
        career_path = [
            "Gain subject expertise or certification",
            "Practice teaching or mentoring",
            "Secure a teaching or training position",
            "Lead educational programs or institutions"
        ]
    else:
        career = "Career Explorer"
        skills_needed = ["Adaptability", "Learning Agility", "Curiosity"]
        market_trend = "Explore various fields to find your passion"
        career_path = [
            "Explore different skills and interests",
            "Try internships or short courses",
            "Identify a field that excites you",
            "Pursue a specific career path"
        ]

    return {
        "career": career,
        "skills_needed": skills_needed,
        "market_trend": market_trend,
        "career_path": career_path
    }

def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return {}

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
    if not profile:
        return redirect(url_for('home'))
    recommendation = get_career_recommendation(profile)
    return render_template('dashboard.html', profile=profile, recommendation=recommendation)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)