import os
from flask import Flask, render_template, url_for
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# --- Your Portfolio Data ---

# Work Experience Data
work_experiences = [
    {
        "timeframe": "Present",
        "title": "Washington State University",
        "role": "Lead Researcher",
        "description": "Conducting advanced research focused on machine learning and Bayesian optimization, with multiple research papers currently under review. Working under the guidance of Dr. Janardhan Rao Doppa, contributing to innovations in test-driven code generation and program synthesis using LLMs."
    },
    {
        "timeframe": "May 2023 – August 2023",
        "title": "UC Berkeley & United States Department of Agriculture (USDA)",
        "role": "Summer Research Intern (Lead)",
        "description": "Developed deep/machine learning models to estimate the prevalence of chronic wasting disease (CWD) in wild cervid populations. Conducted real-time location analysis using National Satellite Imagery data, achieving 96.4% accuracy in disease detection."
    },
    {
        "timeframe": "September 2021 – January 2023",
        "title": "Defense Research & Development Organization (DRDO) - Amity",
        "role": "Researcher and Lead Developer (Internship)",
        "description": "Selected as the only undergraduate to work on AI-based human identification in low-accuracy conditions. Created a comprehensive dataset of human skeletal features and utilized prescriptive analysis with an ML model."
    },
    {
        "timeframe": "September 2021 – February 2022",
        "title": "Microsoft",
        "role": "Internal Technology Intern - Future Ready",
        "description": "Gained in-depth understanding of Azure, Machine Learning, AI, and Computer Vision tools. Developed an AI-enabled Windows application to detect improper body postures during exercise."
    }
]

# Education History Data
education_history = [
    {
        "degree": "Master of Science in Computer Science",
        "university": "Washington State University",
        "year": "Expected 2025",
        "details": "Thesis-based program with a focus on Machine Learning and AI. CGPA: 3.9"
    },
    {
        "degree": "Bachelor of Science in Computer Application",
        "university": "Amity University",
        "year": "2022",
        "details": "Completed with a CGPA of 3.8, focusing on core computer science principles."
    }
]

# Hobbies Data
hobbies_list = [
    {
        "name": "Photography",
        "image": "img/photoHobby.jpg",
        "description": "Exploring the world through a lens, capturing moments from landscapes to portraits."
    },
    {
        "name": "Hiking",
        "image": "img/hiking.jpeg",
        "description": "I enjoy hiking through nature trails, discovering new paths and scenic views."
    },
    {
        "name": "Reading",
        "image": "img/reading.jpeg",
        "description": "Diving into books on technology, science fiction, and history to broaden my perspective."
    }
]


@app.route('/')
def index():
    """
    Renders the main page with all portfolio sections.
    """
    return render_template(
        'index.html',
        title="Shlok Tomar's Portfolio",
        url=os.getenv("URL"),
        work=work_experiences,
        education=education_history,
        hobbies=hobbies_list
    )

if __name__ == '__main__':
    app.run(debug=True)