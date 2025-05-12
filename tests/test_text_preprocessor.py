from modules.text_preprocessor import chunk_text

def test_chunk_text():
    dummy = "This is a sentence. " * 200
    chunks = chunk_text(dummy, chunk_size=500, overlap=100)
    
    assert isinstance(chunks, list)
    assert all(isinstance(chunk, str) for chunk in chunks)
    assert len(chunks) > 1
