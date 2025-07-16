from flask import Flask, render_template, url_for
import os
from dotenv import load_dotenv
from peewee import *

load_dotenv()

app = Flask(__name__)

# Creating a Database 
mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306
)

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
    {"name": "Photography", "image": "img/photoHobby.jpg", "description": "Exploring the world through a lens, capturing moments from landscapes to portraits."},
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

if __name__ == '__main__':
    app.run(debug=True)
