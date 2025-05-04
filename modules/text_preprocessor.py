# modules/text_preprocessor.py

import spacy

nlp = spacy.load("en_core_web_sm")
    
def preprocess_text(text):
    doc = nlp(text)
    chunks = [(ent.text, ent.label_) for ent in doc.ents]
    return chunks