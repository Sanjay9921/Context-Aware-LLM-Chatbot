import pandas as pd
import time
import logging
from modules.llm_testing.preprocessing import prepare_context
from modules.llm_testing.batch_processor import process_batch

def run_test_suite(df_test_suite, models, file_path, generate_answer_fn, iterations=3, delay=10):
    df_results = pd.DataFrame()

    for iteration in range(1, iterations + 1):
        
        print(f"Starting Iteration: {iteration}")

        context, metadata = prepare_context(file_path)
        logging.info(f"Chunking Metadata: {metadata}")

        df_curr_results = pd.DataFrame()
        iter_start = time.time()

        for i in range(0, len(df_test_suite), 3):
            batch_df = df_test_suite.iloc[i:i + 3]
            for model in models:
                batch_results = process_batch(batch_df, model, iteration, df_results, context, generate_answer_fn, delay)
                df_curr_results = pd.concat([df_curr_results, batch_results], ignore_index=True)

        iter_time = round(time.time() - iter_start, 2)
        logging.info(f"Iteration {iteration} completed in {iter_time}s")

        df_curr_results["preprocessing_metadata"] = [metadata] * len(df_curr_results)
        df_curr_results["iteration_time_log"] = [iter_time] * len(df_curr_results)
        df_results = pd.concat([df_results, df_curr_results], ignore_index=True)

    return df_results

def run_and_save_test_suite(df_test_suite, models, file_path, output_csv_path, generate_answer_fn, iterations=3, delay=10):
    logging.info("Test started...")
    print("The test has started.")
    df_results = run_test_suite(df_test_suite, models, file_path, generate_answer_fn, iterations, delay)
    df_results["test_case"] = df_results.index + 1
    df_results.to_csv(output_csv_path, index=False)
    logging.info(f"Saved results to {output_csv_path}")
    return df_results
