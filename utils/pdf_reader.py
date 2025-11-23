import PyPDF2

def extract_text_from_pdf(file_path: str) -> str:
    text = ""

    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)

            for page in reader.pages:
                text += page.extract_text() or ""

        return text

    except Exception as e:
        print(f"PDF extraction error: {e}")
        return ""
