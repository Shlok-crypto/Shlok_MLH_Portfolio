import os
from dotenv import load_dotenv
from peewee import *
import datetime
from flask import Flask, render_template, url_for, request
from playhouse.shortcuts import model_to_dict
import re
from flask import abort
load_dotenv()
# ---- Add these lines for debugging ----
print("DATABASE:", os.getenv("MYSQL_DATABASE"))
print("USER:", os.getenv("MYSQL_USER"))
print("PASSWORD:", os.getenv("MYSQL_PASSWORD"))
print("HOST:", os.getenv("MYSQL_HOST"))
# ------------------------------------
app = Flask(__name__)

# Creating a Database 
mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306
)

# ---- Creating a ORM model called TimelinePost -----
if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)

else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

# Connect to the database and create the table
mydb.connect()
mydb.create_tables([TimelinePost])

print(mydb)

# --- Your Portfolio Data (No changes needed here) ---
work_experiences = [
    {"timeframe": "Present", "title": "Washington State University", "role": "Lead Researcher", "description": "Conducting advanced research focused on machine learning and Bayesian optimization..."},
    {"timeframe": "May 2023 – August 2023", "title": "UC Berkeley & United States Department of Agriculture (USDA)", "role": "Summer Research Intern (Lead)", "description": "Developed deep/machine learning models to estimate the prevalence of chronic wasting disease..."},
    {"timeframe": "September 2021 – January 2023", "title": "Defense Research & Development Organization (DRDO) - Amity", "role": "Researcher and Lead Developer (Internship)", "description": "Selected as the only undergraduate to work on AI-based human identification..."},
    {"timeframe": "September 2021 – February 2022", "title": "Microsoft", "role": "Internal Technology Intern - Future Ready", "description": "Gained in-depth understanding of Azure, Machine Learning, AI, and Computer Vision tools..."}
]

education_history = [
    {"degree": "Master of Science in Computer Science", "university": "Washington State University", "year": "Expected 2025", "details": "Thesis-based program with a focus on Machine Learning and AI. CGPA: 3.9"},
    {"degree": "Bachelor of Science in Computer Application", "university": "Amity University", "year": "2022", "details": "Completed with a CGPA of 3.8, focusing on core computer science principles."}
]

hobbies_list = [
    {"name": "Photo", "image": "img/photoHobby.jpg", "description": "Exploring the world through a lens, capturing moments from landscapes to portraits."},
    {"name": "Hiking", "image": "img/hiking.jpeg", "description": "I enjoy hiking through nature trails, discovering new paths and scenic views."},
    {"name": "Reading", "image": "img/reading.jpeg", "description": "Diving into books on technology, science fiction, and history to broaden my perspective."}
]

# --- Routes for your website ---

@app.route('/')
def index():
    """Renders the main page with all sections except hobbies."""
    return render_template(
        'index.html',
        title="Shlok Tomar's Portfolio",
        url=os.getenv("URL"),
        work=work_experiences,
        education=education_history
    )

@app.route('/hobbies')
def hobbies():
    """Renders the new page dedicated to hobbies."""
    return render_template(
        'hobbies.html',
        title="My Hobbies",
        url=os.getenv("URL"),
        hobbies=hobbies_list
    )

@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline")


#API Functionality
@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('content')

    if not name:
        return "Invalid name", 400
    if not content:
        return "Invalid content", 400
    if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Invalid email", 400

    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)



@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        "timeline_posts": [
            model_to_dict(post)
            for post in
    TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post/<int:post_id>', methods=['DELETE'])
def delete_time_line_post(post_id):
    try:
        post = TimelinePost.get(TimelinePost.id == post_id)
        post.delete_instance()
        return {"status": "success", "message": "Post deleted successfully."}, 200
    except TimelinePost.DoesNotExist:
        return {"status": "error", "message": "Post not found."}, 404

if __name__ == '__main__':
    app.run(debug=True)
