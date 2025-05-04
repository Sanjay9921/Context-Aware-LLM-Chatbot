# modules/text_preprocessor.py

import spacy

nlp = spacy.load("en_core_web_sm") # English Language

def preprocess_text(text):
    doc = nlp(text)
    chunks = [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 20]
    return chunks