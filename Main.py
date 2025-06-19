import os
from sentence_transformers import SentenceTransformer, util
from utils.parser import extract_text_from_pdf
import pandas as pd

def rank_resumes(job_desc_path, resumes_folder):
    # Load job description text
    with open(job_desc_path, 'r', encoding='utf-8') as f:
        job_desc = f.read()

    # Load and process resumes
    resume_texts = {}
    for file in os.listdir(resumes_folder):
        if file.endswith(".pdf"):
            path = os.path.join(resumes_folder, file)
            resume_texts[file] = extract_text_from_pdf(path)

    # BERT model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    job_embedding = model.encode(job_desc, convert_to_tensor=True)

    # Compute similarity
    scores = []
    for name, text in resume_texts.items():
        embedding = model.encode(text, convert_to_tensor=True)
        score = util.cos_sim(job_embedding, embedding).item()
        scores.append({'Resume': name, 'Score': round(score, 4)})

    # Sort and save
    ranked = sorted(scores, key=lambda x: x['Score'], reverse=True)
    df = pd.DataFrame(ranked)
    df.to_csv('hr_report.csv', index=False)

    return ranked
