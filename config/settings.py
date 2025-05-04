import os
from dotenv import load_dotenv # environment variables

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"