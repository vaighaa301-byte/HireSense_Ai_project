import re
from typing import Dict, List, Set, Tuple, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Comprehensive curated skill set organized by category
SKILL_TAXONOMY: Dict[str, List[str]] = {
    "Programming Languages": [
        "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "C", "Go",
        "Rust", "Ruby", "PHP", "Swift", "Kotlin", "R", "SQL", "HTML", "CSS",
        "Bash", "Shell", "Dart", "Scala", "Perl"
    ],
    "Frameworks & Web Technologies": [
        "React", "React.js", "Next.js", "Angular", "Vue.js", "Node.js", "Express.js",
        "Django", "Flask", "FastAPI", "Spring Boot", "ASP.NET", ".NET Core",
        "Streamlit", "Tailwind CSS", "Bootstrap", "Redux", "GraphQL", "REST API",
        "RESTful API", "Microservices"
    ],
    "Databases & Storage": [
        "PostgreSQL", "MySQL", "SQLite", "MongoDB", "Redis", "Cassandra",
        "Oracle", "Firebase", "DynamoDB", "Elasticsearch", "Neo4j", "MS SQL Server"
    ],
    "Cloud & DevOps": [
        "AWS", "Amazon Web Services", "Azure", "Google Cloud", "GCP", "Docker",
        "Kubernetes", "CI/CD", "Jenkins", "GitHub Actions", "Terraform", "Ansible",
        "Linux", "Nginx", "Apache", "Kubernetes", "Helm", "Prometheus", "Grafana"
    ],
    "AI, ML & Data Science": [
        "Machine Learning", "Deep Learning", "Artificial Intelligence", "NLP",
        "Natural Language Processing", "Computer Vision", "Generative AI", "LLM",
        "Large Language Models", "LangChain", "TensorFlow", "PyTorch", "Keras",
        "Scikit-learn", "Pandas", "NumPy", "OpenCV", "Hugging Face", "Tableau",
        "Power BI", "Data Analysis", "Data Science", "Data Engineering", "Apache Spark",
        "Hadoop"
    ],
    "Tools & Engineering Practices": [
        "Git", "GitHub", "GitLab", "Jira", "Agile", "Scrum", "TDD", "Unit Testing",
        "Integration Testing", "Postman", "Swagger", "Webpack", "Vite", "Figma",
        "Object-Oriented Programming", "OOP", "System Design", "Clean Architecture"
    ],
    "Soft Skills & Leadership": [
        "Problem Solving", "Communication", "Leadership", "Teamwork",
        "Critical Thinking", "Project Management", "Time Management",
        "Adaptability", "Collaboration", "Mentorship", "Client Management"
    ]
}

# Inverted mapping: lowercase normalized skill -> Canonical Display Name
ALL_SKILLS_MAP: Dict[str, str] = {}
for category, skills in SKILL_TAXONOMY.items():
    for skill in skills:
        ALL_SKILLS_MAP[skill.lower()] = skill


def clean_text_for_vectorization(text: str) -> str:
    """Preprocesses text for TF-IDF vectorization."""
    if not text:
        return ""
    # Normalize whitespaces and special characters, keep alphanumeric
    text = re.sub(r'[\r\n\t]+', ' ', text)
    text = re.sub(r'[^\w\s\+\#\.]', ' ', text)
    return text.lower().strip()


def extract_skills(text: str) -> Dict[str, List[str]]:
    """
    Extracts skills from text using boundary-safe regex matching against the skill taxonomy.
    
    Returns:
        Dict[str, List[str]]: Mapping of category -> detected skill canonical names.
    """
    if not text:
        return {}

    detected_by_category: Dict[str, Set[str]] = {cat: set() for cat in SKILL_TAXONOMY}
    lower_text = text.lower()

    for category, skills in SKILL_TAXONOMY.items():
        for skill in skills:
            pattern = None
            raw_skill = skill.strip()
            
            # Special regex handling for special symbols like C++, C#, .NET, C, R, Go
            if raw_skill.lower() == "c++":
                pattern = r'(?i)(?:\b|(?<=\s))c\+\+(?:\b|(?=\s|[,\.\;]))'
            elif raw_skill.lower() == "c#":
                pattern = r'(?i)(?:\b|(?<=\s))c\#(?:\b|(?=\s|[,\.\;]))'
            elif raw_skill.lower() == ".net core":
                pattern = r'(?i)\.net\s*core\b'
            elif raw_skill.lower() == "c":
                pattern = r'(?<![a-zA-Z0-9_\+\#])C(?![a-zA-Z0-9_\+\#])'
            elif raw_skill.lower() == "r":
                pattern = r'(?<![a-zA-Z0-9_\+\#])R(?![a-zA-Z0-9_\+\#])'
            elif raw_skill.lower() == "go":
                # Ensure Go language or Golang
                pattern = r'(?i)\b(golang|go\s+language)\b|(?<!\w)Go(?!\w)'
            elif raw_skill.lower() == "ci/cd":
                pattern = r'(?i)\bci[\s\/-]?cd\b'
            elif raw_skill.lower() == "react":
                pattern = r'(?i)\breact(?:\.js)?\b'
            elif raw_skill.lower() == "vue.js":
                pattern = r'(?i)\bvue(?:\.js)?\b'
            elif raw_skill.lower() == "node.js":
                pattern = r'(?i)\bnode(?:\.js)?\b'
            elif raw_skill.lower() == "express.js":
                pattern = r'(?i)\bexpress(?:\.js)?\b'
            else:
                escaped = re.escape(raw_skill)
                pattern = rf'(?i)\b{escaped}\b'

            if pattern and re.search(pattern, text):
                detected_by_category[category].add(raw_skill)

    # Convert sets to sorted lists, filter out empty categories
    return {
        cat: sorted(list(skills_set))
        for cat, skills_set in detected_by_category.items()
        if skills_set
    }


def flatten_skills(skills_by_category: Dict[str, List[str]]) -> Set[str]:
    """Flattens a category-mapped skill dictionary into a set of canonical skill names."""
    flat = set()
    for skills in skills_by_category.values():
        flat.update(skills)
    return flat


def calculate_tfidf_similarity(resume_text: str, jd_text: str) -> float:
    """
    Calculates TF-IDF and Cosine Similarity between resume text and job description.
    
    Returns:
        float: Similarity percentage from 0.0 to 100.0.
    """
    clean_resume = clean_text_for_vectorization(resume_text)
    clean_jd = clean_text_for_vectorization(jd_text)

    if not clean_resume or not clean_jd:
        return 0.0

    try:
        vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=5000
        )
        tfidf_matrix = vectorizer.fit_transform([clean_resume, clean_jd])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(float(similarity) * 100.0, 2)
    except Exception:
        return 0.0


def analyze_resume(resume_text: str, jd_text: str) -> Dict[str, Any]:
    """
    Performs full analysis:
    - Skill extraction from resume and job description
    - Matching skills, missing skills, additional strengths
    - TF-IDF Cosine Similarity
    - Skill match percentage
    - Overall ATS compatibility index
    - Actionable optimization recommendations
    """
    resume_skills_dict = extract_skills(resume_text)
    jd_skills_dict = extract_skills(jd_text)

    resume_skills_flat = flatten_skills(resume_skills_dict)
    jd_skills_flat = flatten_skills(jd_skills_dict)

    # Case-insensitive comparison mapping
    resume_lower_map = {s.lower(): s for s in resume_skills_flat}
    jd_lower_map = {s.lower(): s for s in jd_skills_flat}

    matching_keys = set(resume_lower_map.keys()) & set(jd_lower_map.keys())
    missing_keys = set(jd_lower_map.keys()) - set(resume_lower_map.keys())
    bonus_keys = set(resume_lower_map.keys()) - set(jd_lower_map.keys())

    matching_skills = sorted([jd_lower_map[k] for k in matching_keys])
    missing_skills = sorted([jd_lower_map[k] for k in missing_keys])
    bonus_skills = sorted([resume_lower_map[k] for k in bonus_keys])

    # Calculate Skill Match Score
    if len(jd_skills_flat) > 0:
        skill_match_percentage = round((len(matching_skills) / len(jd_skills_flat)) * 100.0, 2)
    else:
        # If no specific recognized skill in JD, default to 100 or neutral
        skill_match_percentage = 100.0 if len(resume_skills_flat) > 0 else 0.0

    # Calculate TF-IDF Semantic Similarity
    tfidf_score = calculate_tfidf_similarity(resume_text, jd_text)

    # Overall Match Index: Weighted 60% Skill Match + 40% TF-IDF Score
    if len(jd_skills_flat) > 0:
        overall_score = round((0.60 * skill_match_percentage) + (0.40 * tfidf_score), 2)
    else:
        overall_score = tfidf_score

    # Determine match rating and badge color
    if overall_score >= 80:
        rating = "Strong Match"
        rating_color = "#10B981" # Emerald Green
        rating_desc = "Excellent match! Your resume closely aligns with this job role."
    elif overall_score >= 60:
        rating = "Good Fit"
        rating_color = "#3B82F6" # Blue
        rating_desc = "Good candidate fit. Adding a few missing target keywords will make it exceptional."
    elif overall_score >= 40:
        rating = "Moderate Match"
        rating_color = "#F59E0B" # Amber
        rating_desc = "Moderate fit. Recommended to tailor your resume and incorporate missing essential skills."
    else:
        rating = "Low Match"
        rating_color = "#EF4444" # Red
        rating_desc = "Low alignment. Significant skill and keyword gaps detected compared to the job description."

    # Generate actionable tips
    recommendations = []
    if missing_skills:
        top_missing = missing_skills[:6]
        recommendations.append(
            f"Add relevant experience or certifications for key missing skills: **{', '.join(top_missing)}**."
        )
    if tfidf_score < 40:
        recommendations.append(
            "Mirror the phrasing, role titles, and responsibilities mentioned in the job description to improve ATS parsing."
        )
    if len(matching_skills) < 4 and len(jd_skills_flat) > 5:
        recommendations.append(
            "Highlight core project deliverables that demonstrate your competency in the required tech stack."
        )
    if len(resume_text.split()) < 150:
        recommendations.append(
            "Your resume text seems brief. Provide more detailed bullet points detailing your impact and accomplishments."
        )
    if not recommendations:
        recommendations.append("Your resume is well optimized for this role! Ensure formatting and contact info are up to date.")

    return {
        "overall_score": overall_score,
        "tfidf_score": tfidf_score,
        "skill_match_percentage": skill_match_percentage,
        "rating": rating,
        "rating_color": rating_color,
        "rating_desc": rating_desc,
        "resume_skills": resume_skills_dict,
        "jd_skills": jd_skills_dict,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "bonus_skills": bonus_skills,
        "total_resume_skills_count": len(resume_skills_flat),
        "total_jd_skills_count": len(jd_skills_flat),
        "recommendations": recommendations
    }
