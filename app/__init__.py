from flask import Flask, render_template

# Initialize the Flask application
app = Flask(__name__)

# --- Data for your portfolio ---

# Data for your work experience section
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
        "description": "Developed deep/machine learning models to estimate the prevalence of chronic wasting disease (CWD) in wild cervid populations. Conducted real-time location analysis using National Satellite Imagery data, achieving 96.4% accuracy in disease detection. Enhanced model efficiency by 67% on the US Government's SCI-Net High-Performance Computing System (HPC)."
    },
    {
        "timeframe": "September 2021 – January 2023",
        "title": "Defense Research & Development Organization (DRDO) - Amity",
        "role": "Researcher and Lead Developer (Internship)",
        "description": "Selected as the only undergraduate to work on AI-based human identification in low-accuracy conditions. Created a comprehensive dataset of human skeletal features, utilized prescriptive analysis with an ML model, and presented 3D visualizations of the outputs."
    },
    {
        "timeframe": "September 2021 – February 2022",
        "title": "Microsoft",
        "role": "Internal Technology Intern - Future Ready",
        "description": "Gained in-depth understanding of Azure, Machine Learning, AI, and Computer Vision tools through group projects led by Microsoft engineers. Developed an AI-enabled Windows application to detect improper body postures during exercise."
    }
]

@app.route('/')
def index():
    """Renders the main page with your bio, work, and education."""
    return render_template(
        'index.html',
        work=work_experiences,
        education=education_history
    )

@app.route('/hobbies')
def hobbies():
    """Renders the new page dedicated to hobbies."""
    return render_template('hobbies.html', hobbies=hobbies_list)

# This allows you to run the app from the command line
if __name__ == '__main__':
    app.run(debug=True)