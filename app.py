import streamlit as st
import fitz
import re


# -----------------------------
# Skill Database
# -----------------------------

SKILLS = [
    "python",
    "java",
    "c++",
    "sql",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "numpy",
    "pandas",
    "tensorflow",
    "pytorch",
    "html",
    "css",
    "javascript",
    "react",
    "node.js",
    "git",
    "github",
    "docker",
    "aws",
    "linux",
    "mongodb",
    "mysql"
]


# -----------------------------
# Extract Text From PDF
# -----------------------------

def extract_pdf_text(uploaded_file):

    text = ""

    document = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    for page in document:
        text += page.get_text()

    return text



# -----------------------------
# Extract Email
# -----------------------------

def extract_email(text):

    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    email = re.findall(email_pattern, text)

    if email:
        return email[0]

    return "Not Found"



# -----------------------------
# Extract Phone Number
# -----------------------------

def extract_phone(text):

    phone_pattern = r'\b\d{10}\b'

    phone = re.findall(phone_pattern, text)

    if phone:
        return phone[0]

    return "Not Found"



# -----------------------------
# Extract Name
# -----------------------------

def extract_name(text):

    lines = text.split("\n")

    for line in lines[:5]:

        if len(line.split()) <= 4 and line.strip() != "":
            return line.strip()

    return "Not Found"



# -----------------------------
# Find Skills
# -----------------------------

def find_skills(text):

    found = []

    text = text.lower()

    for skill in SKILLS:

        if skill in text:
            found.append(skill)

    return found



# -----------------------------
# Compare Resume and Job
# -----------------------------

def skill_analysis(resume_skills, job_skills):

    matched = []

    missing = []


    for skill in job_skills:

        if skill in resume_skills:
            matched.append(skill)

        else:
            missing.append(skill)


    if len(job_skills) > 0:

        score = (len(matched) / len(job_skills)) * 100

    else:

        score = 0


    return matched, missing, score



# -----------------------------
# Streamlit UI
# -----------------------------

st.set_page_config(
    page_title="AI Resume Parser",
    page_icon="📄",
    layout="wide"
)


st.title("📄 AI Resume Parser & Skill Gap Analyzer")

st.write(
    "Upload your resume and compare it with a job description to find skill gaps."
)



# Upload Resume

resume_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)



# Job Description

job_description = st.text_area(
    "Paste Job Description"
)



if st.button("Analyze Resume"):


    if resume_file is not None and job_description != "":


        # Extract Resume Text

        resume_text = extract_pdf_text(resume_file)


        # Personal Details

        name = extract_name(resume_text)

        email = extract_email(resume_text)

        phone = extract_phone(resume_text)



        # Skills

        resume_skills = find_skills(resume_text)

        job_skills = find_skills(job_description)



        matched, missing, score = skill_analysis(
            resume_skills,
            job_skills
        )



        st.success("Analysis Completed")



        # Personal Information

        st.subheader("👤 Candidate Information")

        col1, col2, col3 = st.columns(3)


        with col1:
            st.write("Name")
            st.info(name)


        with col2:
            st.write("Email")
            st.info(email)


        with col3:
            st.write("Phone")
            st.info(phone)



        # Score

        st.subheader("📊 Resume Match Score")

        st.progress(int(score))

        st.write(
            f"Match Percentage: {score:.2f}%"
        )



        # Skills

        col1, col2 = st.columns(2)


        with col1:

            st.subheader("✅ Matched Skills")

            if matched:

                for skill in matched:
                    st.success(skill)

            else:

                st.warning("No matching skills found")



        with col2:

            st.subheader("❌ Missing Skills")

            if missing:

                for skill in missing:
                    st.error(skill)

            else:

                st.success("No skill gaps found")



        # Recommendation

        st.subheader("💡 Recommendations")


        if missing:

            st.write(
                "You should improve these skills:"
            )

            for skill in missing:

                st.write(
                    "- Learn " + skill
                )

        else:

            st.write(
                "Your resume matches the job requirements well."
            )



        # Resume Text Preview

        with st.expander("View Extracted Resume Text"):

            st.write(resume_text)



    else:

        st.warning(
            "Please upload resume PDF and enter job description."
        )