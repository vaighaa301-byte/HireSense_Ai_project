import io
from typing import Tuple, Optional
import pypdf

def extract_text_from_pdf(pdf_file) -> Tuple[str, int]:
    """
    Extracts text and page count from an uploaded PDF file or path using pypdf.
    
    Args:
        pdf_file: A Streamlit UploadedFile object, file-like object, or file path.
        
    Returns:
        Tuple[str, int]: (extracted_text, page_count)
    """
    try:
        # If it's bytes or UploadedFile, read into BytesIO if needed
        if hasattr(pdf_file, "read"):
            # Ensure file pointer is at the beginning
            pdf_file.seek(0)
            reader = pypdf.PdfReader(pdf_file)
        elif isinstance(pdf_file, (str, bytes)):
            reader = pypdf.PdfReader(pdf_file)
        else:
            raise ValueError("Unsupported PDF input type.")

        page_count = len(reader.pages)
        extracted_pages = []

        for idx, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                extracted_pages.append(text)

        full_text = "\n\n".join(extracted_pages).strip()
        
        # Clean up unnecessary multiple blank lines while preserving structure
        lines = [line.strip() for line in full_text.splitlines() if line.strip()]
        cleaned_text = "\n".join(lines)
        
        return cleaned_text, page_count
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF: {str(e)}")
