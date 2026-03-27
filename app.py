import streamlit as st
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="SmartHire AI", page_icon="🤖", layout="wide")

st.title("🤖 SmartHire AI: Resume Ranking System")
st.subheader("Automated NLP Screening for Recruiters")

# 2. Function to extract text from PDF
def extract_text_from_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

# 3. Sidebar for Project Details (Great for your Viva!)
with st.sidebar:
    st.header("Project Info")
    st.markdown("**Student:** Om Prakash")
    st.markdown("**Tech Stack:** Python, NLP, Streamlit")
    st.info("This system uses TF-IDF and Cosine Similarity to rank candidates.")

# 4. Input: Job Description
st.write("---")
jd = st.text_area("📌 Paste the Job Description (JD) here:", height=150)

# 5. Input: Resume Upload
uploaded_files = st.file_uploader("📂 Upload Candidate Resumes (PDF only)", type="pdf", accept_multiple_files=True)

# 6. Logic: Processing and Ranking
if st.button("🚀 Rank Resumes"):
    if jd and uploaded_files:
        with st.spinner("AI is analyzing resumes..."):
            resume_texts = []
            filenames = []

            for file in uploaded_files:
                text = extract_text_from_pdf(file)
                resume_texts.append(text)
                filenames.append(file.name)

            # Combine JD with Resumes for Vectorization
            data = [jd] + resume_texts
            
            # Vectorization using TF-IDF
            vectorizer = TfidfVectorizer(stop_words='english')
            vectors = vectorizer.fit_transform(data)
            
            # Calculate Cosine Similarity
            # First vector is JD, the rest are resumes
            scores = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

            # 7. Results: Display in a Table
            results = pd.DataFrame({
                "Candidate Name": filenames,
                "Match Percentage (%)": [round(s * 100, 2) for s in scores]
            })

            # Sort by highest score
            results = results.sort_values(by="Match Percentage (%)", ascending=False)

            st.success("Analysis Complete!")
            st.table(results)
    else:
        st.error("Please provide both a Job Description and at least one Resume.")

st.write("---")
st.caption("Developed for MCA Minor Project - 2026")