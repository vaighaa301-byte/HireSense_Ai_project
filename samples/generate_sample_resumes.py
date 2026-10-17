import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pdf(filename: str, title: str, content: list):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    styles = getSampleStyleSheet()

    # Custom styles
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1E293B'),
        fontName='Helvetica-Bold'
    )
    
    subhead_style = ParagraphStyle(
        'SubheadStyle',
        parent=styles['Heading2'],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#2563EB'),
        fontName='Helvetica-Bold',
        spaceBefore=8,
        spaceAfter=4
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155'),
        fontName='Helvetica'
    )

    story = []
    story.append(Paragraph(title, header_style))
    story.append(Spacer(1, 10))

    for item_type, text in content:
        if item_type == 'subhead':
            story.append(Paragraph(text, subhead_style))
        elif item_type == 'body':
            story.append(Paragraph(text, body_style))
        elif item_type == 'bullet':
            story.append(Paragraph(f"• {text}", body_style))
        story.append(Spacer(1, 4))

    doc.build(story)
    print(f"Generated: {filename}")

if __name__ == "__main__":
    os.makedirs("samples", exist_ok=True)

    # 1. Python Full Stack Developer Resume
    resume_python = [
        ('body', '<b>Email:</b> rahul.sharma@example.com | <b>Phone:</b> +91 98765 43210 | <b>LinkedIn:</b> linkedin.com/in/rahulsharma | <b>GitHub:</b> github.com/rahuldev'),
        ('subhead', 'PROFESSIONAL SUMMARY'),
        ('body', 'Experienced Full Stack Python Developer with 4+ years of expertise in architecting scalable web applications, designing RESTful APIs, and implementing automated CI/CD pipelines. Proficient in Python, Django, FastAPI, React, and AWS cloud services.'),
        ('subhead', 'TECHNICAL SKILLS'),
        ('bullet', '<b>Languages:</b> Python, JavaScript, TypeScript, SQL, HTML, CSS'),
        ('bullet', '<b>Frameworks & Web:</b> Django, FastAPI, Flask, React, Next.js, REST API, Tailwind CSS'),
        ('bullet', '<b>Databases:</b> PostgreSQL, MySQL, Redis, SQLite'),
        ('bullet', '<b>Cloud & DevOps:</b> Docker, Kubernetes, AWS, CI/CD, GitHub Actions, Linux'),
        ('bullet', '<b>Tools & Practices:</b> Git, GitHub, Jira, Agile, Scrum, Unit Testing, TDD'),
        ('bullet', '<b>Soft Skills:</b> Problem Solving, Teamwork, Communication, Mentorship'),
        ('subhead', 'WORK EXPERIENCE'),
        ('body', '<b>Senior Software Engineer</b> | NexaTech Solutions (2022 - Present)'),
        ('bullet', 'Engineered high-throughput RESTful microservices using Python and FastAPI, serving over 1.5M monthly active users.'),
        ('bullet', 'Designed modular frontend components with React, TypeScript, and Tailwind CSS, improving page load speed by 35%.'),
        ('bullet', 'Automated deployment workflows using Docker, GitHub Actions, and AWS ECS with zero downtime.'),
        ('bullet', 'Optimized complex PostgreSQL queries and Redis caching layers, reducing API latency by 42%.'),
        ('body', '<b>Full Stack Developer</b> | CloudVibe Technologies (2020 - 2022)'),
        ('bullet', 'Built enterprise SaaS dashboard using Django, PostgreSQL, and React.'),
        ('bullet', 'Implemented automated unit testing with 88% code coverage and integrated CI/CD pipelines.'),
        ('subhead', 'EDUCATION'),
        ('body', 'Bachelor of Technology in Computer Science | Kerala Technological University (2016 - 2020)')
    ]
    generate_pdf("samples/sample_resume_python_dev.pdf", "Rahul Sharma - Senior Python Full Stack Developer", resume_python)

    # 2. Data Scientist & Machine Learning Resume
    resume_ds = [
        ('body', '<b>Email:</b> ananya.nair@example.com | <b>Phone:</b> +91 98450 12345 | <b>Location:</b> Bengaluru, India | <b>GitHub:</b> github.com/ananyanair-ai'),
        ('subhead', 'PROFESSIONAL SUMMARY'),
        ('body', 'Data Scientist and AI Engineer with 3+ years experience developing Machine Learning models, NLP pipelines, and deep learning architectures. Skilled in Python, Scikit-learn, PyTorch, LangChain, and Streamlit dashboard prototyping.'),
        ('subhead', 'CORE COMPETENCIES & SKILLS'),
        ('bullet', '<b>Languages & Tools:</b> Python, SQL, R, Git, Linux, Docker'),
        ('bullet', '<b>AI & Machine Learning:</b> Scikit-learn, TensorFlow, PyTorch, Deep Learning, Machine Learning, NLP, Generative AI, LLM, LangChain'),
        ('bullet', '<b>Data Analytics:</b> Pandas, NumPy, Data Analysis, Data Science, Tableau, Power BI'),
        ('bullet', '<b>Cloud & Deployment:</b> AWS, Google Cloud (GCP), Streamlit, FastAPI, Docker'),
        ('bullet', '<b>Soft Skills:</b> Critical Thinking, Problem Solving, Agile Collaboration, Communication'),
        ('subhead', 'WORK EXPERIENCE'),
        ('body', '<b>Machine Learning Engineer</b> | AI Horizons Lab (2022 - Present)'),
        ('bullet', 'Designed and trained NLP classification and summarization pipelines using PyTorch and Hugging Face transformers.'),
        ('bullet', 'Built interactive data exploration prototypes using Streamlit and Pandas for executive stakeholders.'),
        ('bullet', 'Developed predictive churn models using Scikit-learn, boosting customer retention by 18%.'),
        ('bullet', 'Deployed scalable model inference APIs using FastAPI and Docker containers on AWS.'),
        ('body', '<b>Data Analyst</b> | Insight Data Systems (2021 - 2022)'),
        ('bullet', 'Conducted comprehensive statistical analysis and built Power BI dashboards analyzing 500k+ customer transactions.'),
        ('bullet', 'Authored automated SQL ETL queries to extract and transform database pipelines in PostgreSQL.'),
        ('subhead', 'EDUCATION'),
        ('body', 'B.Tech in Artificial Intelligence & Data Science | KTU (2017 - 2021)')
    ]
    generate_pdf("samples/sample_resume_data_scientist.pdf", "Ananya Nair - Data Scientist & AI Engineer", resume_ds)
