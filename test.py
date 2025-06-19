from mistralai import Mistral
import os
from dotenv import load_dotenv

def process_pdf_ocr(file_path: str):
    """
    Uploads a PDF file to Mistral, processes it with OCR, and returns the OCR response.

    Args:
        file_path (str): The path to the PDF file to be processed.

    Returns:
        dict: The OCR response from Mistral.
    """
    load_dotenv()
    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)

    file_name = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        uploaded_pdf = client.files.upload(
            file={
                "file_name": file_name,
                "content": f,
            },
            purpose="ocr"
        )

    signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id)

    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": signed_url.url,
        },
        include_image_base64=True
    )

    return ocr_response

# Example usage:
# response = process_pdf_ocr("AASZX2206288.pdf")
# print(response)