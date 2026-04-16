import streamlit as st
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import re


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



if st.button("🚀 Rank Resumes"):
    if jd and uploaded_files:
        with st.spinner("Analyzing Technical Skills..."):
            # 1. Define a list of technical skills to look for
            # You can expand this list as much as you want!
            tech_library = ["python", "java", "sql", "html", "css", "javascript", "machine learning", "dsa", "nlp", "aws", "react"]
            
            # 2. Extract keywords from JD (The "Base")
            jd_content = jd.lower()
            required_skills = [skill for skill in tech_library if re.search(rf"\b{skill}\b", jd_content)]
            
            if not required_skills:
                st.warning("No standard tech skills found in JD. Try adding words like 'Python' or 'Java'.")
                # Fallback to your old TF-IDF logic here if you want
            else:
                results_data = []

                for file in uploaded_files:
                    resume_text = extract_text_from_pdf(file).lower()
                    
                    # 3. Match Resume against the Required Skills
                    found_skills = [skill for skill in required_skills if re.search(rf"\b{skill}\b", resume_text)]
                    
                    # 4. Calculation: (Matches / Total Required) * 100
                    match_percent = (len(found_skills) / len(required_skills)) * 100
                    
                    results_data.append({
                        "Candidate Name": file.name,
                        "Match Percentage (%)": round(match_percent, 2),
                        "Skills Matched": ", ".join(found_skills)
                    })

                # 5. Display Table
                results_df = pd.DataFrame(results_data).sort_values(by="Match Percentage (%)", ascending=False)
                st.success(f"Matching based on {len(required_skills)} identified skills.")
                st.table(results_df)

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
