# 1. Libraries
## 1.1 Own Modules
from modules.pdf_parser import extract_text_from_static_pdf
from modules.text_preprocessor import preprocess_text
from modules.qa_engine import generate_answer
from config.settings import TOGETHER_API_KEY, MODEL_NAME_1, MODEL_NAME_2, MODEL_NAME_3, MODEL_NAME_4

## 1.2 Python modules
import streamlit as st # Streamlit
import fitz # Chunking
import openpyxl # Excel
import pandas as pd # Testing
from typing import Union, IO
import requests
import time
import json
import logging # Logging
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity # Variation Score
import ast # Cleaning expected keywords

# 2. Setup
## 2.1 File Name
file_path_1 = "C:/Users/sanja/Desktop/Github 2025/Context-Aware-LLM-Chatbot/tests/sample_docs/Databricks_Prompt_Engineering_Steps.pdf"
file_path_2 = "C:/Users/sanja/Desktop/Github 2025/Context-Aware-LLM-Chatbot/tests/sample_docs/Databricks_RAG_Steps.pdf"

## 2.2 Cosine Score setup
# Load once globally
embedder = SentenceTransformer('all-MiniLM-L6-v2')

## 2.3 Models
models = [MODEL_NAME_1, MODEL_NAME_2, MODEL_NAME_3]

## 2.4 Test Suite Dataframe
df_test_suite_1 = pd.read_excel("./tests/test_suite.xlsx", sheet_name="Test1", engine="openpyxl")
df_test_suite_2 = pd.read_excel("./tests/test_suite.xlsx", sheet_name="Test2", engine="openpyxl")

# 3. Functions
## Cleaning Keywords
def clean_expected_keywords_list(raw_keywords):
    cleaned = []
    for kw in raw_keywords:
        if isinstance(kw, tuple):
            # Take first element if tuple
            kw = kw[0]
        # Convert to string just in case, and strip whitespace
        cleaned.append(str(kw).strip())
    return cleaned


## 3.1 Cosine Similarity
def semantic_similarity(text1: str, text2: str) -> float:
    embeddings = embedder.encode([text1, text2])
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return round(similarity, 4)


## 3.2 Metadata Testing: Chunking, Token Size
def prepare_context(file_path, num_chunks=15):
    start = time.time()
    text = extract_text_from_static_pdf(file_path)
    chunks = preprocess_text(text)
    end = time.time()

    context = "\n".join(chunks[:num_chunks])
    metadata = {
        "chunking_time_s": round(end - start, 2),
        "total_chunks": len(chunks),
        "total_characters": len(text)
    }
    return context, metadata


## 3.3 Generate/Score Response
def generate_and_score_response(prompt, model, expected_keywords, reference_response=None, context=None):
    import time
    start = time.time()
    response = generate_answer(context, prompt, model)
    end = time.time()

    response_time = round(end - start, 2)

    # Default fallback values
    consistency_score = "N/A"
    similarity_score = "N/A"
    matched_keywords = []

    try:
        if isinstance(expected_keywords, str):
            import ast
            expected_keywords = ast.literal_eval(expected_keywords)

        expected_keywords = [str(kw).strip().lower() for kw in expected_keywords]

        matched_keywords = [kw for kw in expected_keywords if kw in response.lower()]
        consistency_score = round(len(matched_keywords) / len(expected_keywords), 2) if expected_keywords else 0.0

        if reference_response:
            similarity_score = round(semantic_similarity(response, reference_response), 2)
        else:
            similarity_score = 1.0  # for baseline

    except Exception as e:
        print(f"Error during scoring: {e}")

    return {
        "prompt": prompt,
        "response": response,
        "response_time_s": response_time,
        "matched_keywords": matched_keywords,
        "consistency_score": consistency_score,
        "similarity_score": similarity_score
    }

## 3.4 Batch Processing
def process_batch(batch_df, model, iteration, results_df, context, delay=10):
    baseline_row = batch_df.iloc[0]
    variation_rows = batch_df.iloc[1:3]

    prompt_baseline = baseline_row["question"]
    expected_keywords = baseline_row["expected_keywords"]

    if isinstance(expected_keywords, str):
        # maybe parse if string representation of list
        try:
            expected_keywords = ast.literal_eval(expected_keywords)
        except Exception:
            expected_keywords = [expected_keywords]
    elif not isinstance(expected_keywords, list):
        expected_keywords = [expected_keywords]

    expected_keywords = clean_expected_keywords_list(expected_keywords)

    # Baseline
    result = generate_and_score_response(prompt_baseline, model, expected_keywords, context=context)
    result.update({
        "iteration": iteration,
        "model": model,
        "question_category": "baseline",
        "question_number": 1
    })
    results_df = pd.concat([results_df, pd.DataFrame([result])], ignore_index=True)
    time.sleep(delay)

    # Variations
    reference_response = result["response"]
    for i, row in variation_rows.iterrows():
        variation_result = generate_and_score_response(row["question"], model, expected_keywords,
                                                       reference_response, context=context)
        variation_result.update({
            "iteration": iteration,
            "model": model,
            "question_category": f"variation{i}",
            "question_number": i
        })
        results_df = pd.concat([results_df, pd.DataFrame([variation_result])], ignore_index=True)
        time.sleep(delay)

    return results_df


## 3.5 Running Test Suite
def run_test_suite(df_test_suite, models, file_path, iterations=3, delay=10):
    df_results = pd.DataFrame()
    
    for iteration in range(1, iterations + 1):
        # 1. Data Preprocessing
        full_context, metadata = prepare_context(file_path)
        logging.info(f"Chunking Metadata: {metadata}")

        df_curr_results = pd.DataFrame()

        logging.info(f"--- Iteration {iteration} ---")
        iter_start = time.time()

        # 2. Batch Processing
        for i in range(0, len(df_test_suite), 3):
            batch_df = df_test_suite.iloc[i:i + 3]
            for model in models:
                batch_results = process_batch(batch_df, model, iteration, df_results, full_context, delay)
                df_curr_results = pd.concat([df_curr_results, batch_results], ignore_index=True)

        # 3. Add metadata to current iteration
        iter_time = round(time.time() - iter_start, 2)
        logging.info(f"Iteration {iteration} completed in {iter_time} seconds.")

        df_curr_results["preprocessing_metadata"] = [metadata] * len(df_curr_results)
        df_curr_results["iteration_time_log"] = [iter_time] * len(df_curr_results)

        # 4. Append to full results
        df_results = pd.concat([df_results, df_curr_results], ignore_index=True)

    return df_results


## 3.6 Resuable Function to save outputs
def run_and_save_test_suite(df_test_suite,models,file_path,output_csv_path,iterations=3,delay=10):
    print("Test has started...")
    # 1. Run the test suite
    df_results = run_test_suite(df_test_suite, models, file_path, iterations, delay)
    
    # 2. Add sequential test_case number (if needed)
    df_results["test_case"] = df_results.index + 1

    # 3. Save to CSV
    df_results.to_csv(output_csv_path, index=False)
    
    # 4. Log success
    logging.info(f"Test results saved to {output_csv_path}")
    
    return df_results



# 4. Test
## 4.1 Test 1 - Prompt Engineering PDF
df_results1 = run_and_save_test_suite(
    df_test_suite=df_test_suite_1,
    models=models,
    file_path=file_path_1,
    output_csv_path="./tests/results/test1.csv",
    iterations=3,
    delay=10
)

# FINAL RESULT
print("Successful!")