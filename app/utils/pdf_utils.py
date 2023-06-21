from PyPDF2 import PdfReader


def get_pdf_text(pdf_docs):
    """
    Extracts text from PDF documents.

    Args:
        pdf_docs (list): List of uploaded PDF documents.

    Returns:
        str: Concatenated text from all the PDF documents.
    """
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text
