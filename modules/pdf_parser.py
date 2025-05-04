# modules/pdf_parser.py

import fitz  # PyMuPDF

def extract_text_from_pdf(uploaded_file):
    """
    Extracts all text from a PDF file-like object.
    
    Args:
        uploaded_file: A file-like object from Streamlit file uploader.
    
    Returns:
        str: The extracted text.
    """
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text