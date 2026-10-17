# 🎯 HireSense AI — Intelligent Resume Analyzer & ATS Scorer

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-TF--IDF-F7931E.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**HireSense AI** is an advanced, AI-powered Resume Analyzer and ATS (Applicant Tracking System) compatibility scoring tool. It compares candidate resumes against job descriptions, computes semantic content similarity using **TF-IDF & Cosine Similarity**, categorizes matching and missing skills, and provides actionable recommendations to optimize resumes for recruitment filters.

---

## ✨ Key Features

- 📄 **PDF Text Extraction**: Extracts text and structure seamlessly from single and multi-page PDF resumes using `pypdf`.
- 🔍 **Skill Detection & Categorization**: Identifies technical skills, frameworks, databases, cloud tools, and soft skills using custom regex pattern matching across 7+ domains.
- 📐 **Semantic Cosine Similarity**: Uses Scikit-learn's **TF-IDF Vectorizer** (with n-gram analysis and English stop-word filtering) to compute textual alignment.
- 🎯 **ATS Compatibility Index**: Delivers a weighted compatibility score combining skill match rate and content alignment.
- 🟢 **Skill Gap Analysis**:
  - **Matching Skills**: Highlights shared qualifications in emerald badges.
  - **Missing Skills**: Clearly flags requirements from the job description missing in the resume.
  - **Bonus Strengths**: Recognizes additional profile competencies.
- 💡 **Actionable Optimization Tips**: Gives targeted advice on what keywords, projects, or formatting adjustments to make.
- 📥 **Export Analysis Report**: Download a text report of the compatibility evaluation for offline review.
- 🧪 **Pre-loaded Test Data**: Comes with sample job descriptions and ready-to-test PDF resumes.

---

## 🏗️ Project Architecture

```
HireSense_Ai_project/
│
├── app.py                      # Main Streamlit web application
├── requirements.txt            # Project dependencies
├── .gitignore                  # Git ignore rules (venv, cache, etc.)
├── README.md                   # Complete documentation
│
├── utils/                      # Modular utility packages
│   ├── __init__.py
│   ├── extractor.py            # PDF text extraction module (pypdf)
│   └── analyzer.py             # Skill extraction, TF-IDF cosine similarity & scoring
│
└── samples/                    # Sample test data & generators
    ├── sample_data.py          # Sample Job Descriptions (Full Stack, Data Science, DevOps, React)
    ├── generate_sample_resumes.py # Script to generate sample PDF resumes
    ├── sample_resume_python_dev.pdf
    └── sample_resume_data_scientist.pdf
```

---

## 🚀 Quickstart Guide (Local Setup)

### 1. Clone or Open the Repository
```bash
git clone https://github.com/<your-username>/HireSense_Ai_project.git
cd HireSense_Ai_project
```

### 2. Create and Activate Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```
The app will automatically launch in your browser at: `http://localhost:8501`.

---

## 🧪 Testing the Project

1. Open the running app at `http://localhost:8501`.
2. In **Step 1 (Upload Resume)**, upload a PDF resume. You can use the sample resumes provided in `samples/sample_resume_python_dev.pdf` or `samples/sample_resume_data_scientist.pdf`.
3. In **Step 2 (Job Description)**, select one of the built-in presets (e.g., *"Python Full Stack Developer"* or *"Data Scientist & AI / ML Engineer"*), or paste your own job posting.
4. Click **✨ Analyze Compatibility & Skills**.
5. Review the **ATS Compatibility score**, **Matching Skills**, **Missing Skills**, and **Recommendations**.
6. Click **📥 Download Analysis Report** to export the findings.

---

## 📦 How to Publish on GitHub

Follow these steps to upload your project to GitHub:

### Step 1: Initialize Git
```bash
git init
```

### Step 2: Add Files & Make Initial Commit
```bash
git add .
git commit -m "Initial commit: HireSense AI Resume Analyzer"
```

### Step 3: Create a New GitHub Repository
1. Go to [github.com/new](https://github.com/new).
2. Repository name: `HireSense_Ai_project` (or `hiresense-ai`).
3. Set visibility to **Public**.
4. Leave **"Initialize this repository with a README" unchecked** (since we already have one).
5. Click **Create repository**.

### Step 4: Link and Push to GitHub
```bash
git branch -M main
git remote add origin https://github.com/<YOUR-GITHUB-USERNAME>/HireSense_Ai_project.git
git push -u origin main
```

---

## 🌐 How to Deploy on Streamlit Community Cloud (Free)

Deploy your live web application in less than 2 minutes:

1. Push your code to GitHub (as shown above).
2. Go to **[share.streamlit.io](https://share.streamlit.io/)** and sign in with your GitHub account.
3. Click **"New app"**.
4. Select:
   - **Repository**: `<YOUR-GITHUB-USERNAME>/HireSense_Ai_project`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click **"Deploy!"**.
6. Your live demo link (e.g., `https://hiresense-ai.streamlit.app`) will be active and shareable worldwide!

---

## 🛠️ Tech Stack

- **Frontend & Web Framework**: [Streamlit](https://streamlit.io/)
- **Text & PDF Processing**: [pypdf](https://pypi.org/project/pypdf/)
- **Machine Learning & NLP**: [scikit-learn](https://scikit-learn.org/) (TF-IDF Vectorizer, Cosine Similarity)
- **Programming Language**: Python 3.10+

---

## 📄 License
This project is open-source and licensed under the [MIT License](LICENSE).
