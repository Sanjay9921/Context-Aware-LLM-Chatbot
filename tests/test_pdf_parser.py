from modules.pdf_parser import extract_text_from_pdf

def test_pdf_extraction():
    text = extract_text_from_pdf("./sample_docs/Sanjay_Prabhu:Kunjibettu_Resume.pdf")
    assert isinstance(text, str)
    assert len(text) > 100