# backend/skills/skill_extractor.py
import re
import spacy
from collections import Counter
#from spacy.lang.en.stop_words import STOP_WORDS
import en_core_web_sm

nlp = en_core_web_sm.load()
#nlp = spacy.load("en_core_web_sm")
STOPWORDS = nlp.Defaults.stop_words

def extract_keywords_from_text(text, top_n=20):
    text = (text or "").lower()
    doc = nlp(text)
    words = []
    for chunk in doc.noun_chunks:
        ch = chunk.text.strip()
        if ch not in STOPWORDS and len(ch) > 1:
            words.append(ch)
    for token in doc:
        if token.pos_ in ("NOUN","PROPN") and token.text.lower() not in STOPWORDS:
            words.append(token.text.strip())
    freq = Counter(words)
    return [k for k,v in freq.most_common(top_n)]

def extract_skills_from_resume(resume_text, global_keywords):
    text_low = (resume_text or "").lower()
    found = set()
    for skill in global_keywords:
        if re.search(r"\b" + re.escape(skill) + r"\b", text_low):
            found.add(skill)
    return sorted(list(found))
