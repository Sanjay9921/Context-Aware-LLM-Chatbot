import os
from dotenv import load_dotenv # environment variables

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
MODEL_NAME = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"