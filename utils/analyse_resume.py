import re
import spacy

nlp = spacy.load("en_core_web_sm")

def analyse_resume(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    # Predefined skill pattern
    skills = re.findall(r'\b(Python|Java|SQL|Excel|C\+\+|TensorFlow|AWS|Docker|JavaScript)\b', text, re.I)
    
    return {
        "word_count": len(text.split()),
        "entities_found": entities[:50],  # Limit to first 50 for display
        "skills_found": list(set(skills))
    }
