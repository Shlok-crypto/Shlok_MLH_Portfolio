import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    work_experiences = [
        {"role": "Software Engineer Intern", "company": "Company A", "duration": "Summer 2024"},
        {"role": "Junior Developer", "company": "Company B", "duration": "2022 - 2023"}
    ]
    return render_template('index.html', experiences=work_experiences)
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)