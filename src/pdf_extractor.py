from pypdf import PdfReader
import io


def extract_text_from_pdf(file_obj):


    
    try:
        # Read the uploaded file bytes into a PdfReader
        if isinstance(file_obj, bytes):
            pdf_reader = PdfReader(io.BytesIO(file_obj))

        else:

            # Assuming file-like object 
            pdf_reader = PdfReader(file_obj)
        num_pages = len(pdf_reader.pages)


        # Extract text from each page
        extracted_text = []
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            if page_text:
                extracted_text.append(page_text)

        # Combine all pages into one text document
        full_text = "\n".join(extracted_text)

        # Check if any text was actually extracted
        if not full_text.strip():
            return "", num_pages

        return full_text, num_pages

    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return "", 0
