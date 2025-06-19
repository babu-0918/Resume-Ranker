import fitz  # PyMuPDF
import os
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight and fast

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# Example usage
resume_folder = "resumes/"
resume_texts = {}

for filename in os.listdir(resume_folder):
    if filename.endswith(".pdf"):
        path = os.path.join(resume_folder, filename)
        resume_texts[filename] = extract_text_from_pdf(path)

# Now resume_texts holds each resume's text, accessible by filename
