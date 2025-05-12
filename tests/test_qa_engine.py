from modules.qa_engine import query_model

def test_response_and_latency():
    prompt = "I am a recruiter looking for a data engineer professional"
    model = "meta-llama/Meta-Llama-3-70B-Instruct-Turbo"
    response, latency = query_model(prompt, model)
    
    assert isinstance(response, str)
    assert "Paris" in response
    assert latency < 10  # Acceptable latency