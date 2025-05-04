import streamlit as st
import fitz
from modules.pdf_parser import extract_text_from_pdf
from modules.text_preprocessor import preprocess_text
from modules.qa_engine import generate_answer

st.set_page_config(page_title="Context Aware PDF Chatbot", layout="wide")
st.title("Chat with your PDF :)")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    chunks = preprocess_text(text)
    full_context = "\n".join(chunks[:15])  # Limit for prompt

    st.success("PDF processed. Ask your questions!")

    user_question = st.text_input("Ask a question about the document:")

    if user_question:
        with st.spinner("Generating answer..."):
            answer = generate_answer(full_context, user_question)
        st.markdown("** Answer:**")
        st.write(answer)