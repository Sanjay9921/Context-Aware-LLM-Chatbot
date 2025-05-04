# Context Aware LLM Chatbot

# 1. Project Overview

1. Lets users upload a PDF.
2. Uses spaCy to analyze the text.
3. Sends a question + context to the Together AI API (using the open-source Mistral 7B Instruct model).
4. Gets an intelligent, context-aware answer back.
5. Displays the answer in a Streamlit web app.

# 2. Tech Stack

1. Together AI API: https://api.together.xyz/
* Collects questions and context and sends it to the open source LLM model
2. Streamlit: https://share.streamlit.io/new
*  Mistral 7B Instruct mode: Open source LLM model
3. Python Modules
* spaCy: Analyses the text
4. NetworkX