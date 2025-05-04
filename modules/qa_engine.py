import requests
from config.settings import TOGETHER_API_KEY, MODEL_NAME

def generate_answer(context, question):
    prompt = f"""You are an assistant. Use the context below to answer the question:

Context:
{context}

Question:
{question}

Answer:"""

    response = requests.post(
        "https://api.together.xyz/v1/chat/completions",
        headers={"Authorization": f"Bearer {TOGETHER_API_KEY}"},
        json={
            "model": MODEL_NAME,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        },
    )

    result = response.json()
    return result['choices'][0]['message']['content'].strip()