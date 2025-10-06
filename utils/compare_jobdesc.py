from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def clean_text(text):
    return re.sub(r'[^a-zA-Z ]', '', text.lower())

def compare_resume_with_job(resume_text, job_desc):
    docs = [clean_text(resume_text), clean_text(job_desc)]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform(docs)
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0] * 100

    resume_words = set(docs[0].split())
    job_words = set(docs[1].split())
    common = list(resume_words & job_words)
    return score, common[:10]
