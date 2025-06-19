from flask import Flask, render_template, request, redirect, send_file
import os
from resume_ranker import rank_resumes  

app = Flask(__name__)
UPLOAD_FOLDER = 'resumes'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        job_desc = request.form['job_desc']
        with open('job_description.txt', 'w') as f:
            f.write(job_desc)

      
        files = request.files.getlist('resumes')
        for file in files:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

        # Run ranking logic
        results = rank_resumes('job_description.txt', UPLOAD_FOLDER)

        return render_template('results.html', results=results)

    return render_template('index.html')

@app.route('/download')
def download():
    return send_file('hr_report.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
