import re
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def analyse_resume(text):
    doc = nlp(text)

    skills = re.findall(
        r'\b(Python|Java|SQL|Excel|C\+\+|TensorFlow|AWS|Docker|JavaScript|React|Django|Flask)\b',
        text,
        re.I
    )

    return {
        "word_count": len(text.split()),
        "skills_found": list(set(skills))
    }
