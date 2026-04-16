import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Page configuration
st.set_page_config(page_title="SmartHire AI - Resume Parser", layout="wide")

def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def rank_resumes(job_description, resumes):
    # Combine job description with resumes for vectorization
    documents = [job_description] + resumes
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    # Calculate Cosine Similarity
    scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    return scores

# UI Header
st.title("🚀 SmartHire AI: Resume Ranking System")
st.markdown("Rank candidate resumes based on job descriptions using NLP.")

# Sidebar for Job Description
st.sidebar.header("Job Details")
job_description = st.sidebar.text_area("Paste the Job Description here:", height=300)

# File Uploader
uploaded_files = st.file_uploader("Upload Resumes (PDF only)", type="pdf", accept_multiple_files=True)

if st.button("Analyze & Rank") and job_description and uploaded_files:
    with st.spinner('Analyzing resumes...'):
        resume_texts = []
        file_names = []
        
        for file in uploaded_files:
            text = extract_text_from_pdf(file)
            resume_texts.append(text)
            file_names.append(file.name)
        
        # Get Ranking Scores
        scores = rank_resumes(job_description, resume_texts)
        
        # Display Results
        results = pd.DataFrame({
            "Candidate Name": file_names,
            "Match Score (%)": [round(score * 100, 2) for score in scores]
        }).sort_values(by="Match Score (%)", ascending=False)
        
        st.subheader("📊 Ranking Results")
        st.table(results)
        st.success("Analysis Complete!")

elif not job_description:
    st.info("Please provide a job description in the sidebar.")
