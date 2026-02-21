import PyPDF2
from docx import Document
import io

def extract_text_from_pdf(file_bytes):
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file_bytes):
    doc = Document(io.BytesIO(file_bytes))
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def extract_text(file_item):
    """
    file_item is a Streamlit UploadedFile object or similar.
    """
    filename = file_item.name
    content = file_item.read()
    if filename.endswith('.pdf'):
        return extract_text_from_pdf(content)
    elif filename.endswith('.docx'):
        return extract_text_from_docx(content)
    elif filename.endswith('.txt'):
        return content.decode('utf-8', errors='ignore')
    else:
        return "Unsupported file format"
