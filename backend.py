# Step-by-Step Solution: PDF Text Extraction Backend

import fitz  # PyMuPDF
import pdfplumber
import os


class PDFProcessor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)

    def get_pdf_metadata(self):
        """Extract page count, title, and author"""
        try:
            with fitz.open(self.file_path) as doc:
                metadata = doc.metadata
                return {
                    "file_name": self.file_name,
                    "total_pages": doc.page_count,
                    "title": metadata.get("title"),
                    "author": metadata.get("author")
                }
        except Exception as e:
            raise RuntimeError(f"Metadata extraction failed: {e}")

    def extract_text_pymupdf(self):
        """Primary extraction using PyMuPDF"""
        try:
            doc = fitz.open(self.file_path)

            if doc.needs_pass:
                raise RuntimeError("PDF is password protected")

            extracted_text = {}
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                text = page.get_text().strip()
                extracted_text[page_num + 1] = text

            if not any(extracted_text.values()):
                raise RuntimeError("PDF contains no extractable text")

            return {
                "file_name": self.file_name,
                "total_pages": doc.page_count,
                "pages": extracted_text
            }

        except Exception as e:
            print(f"PyMuPDF failed: {e}")
            return self.extract_text_pdfplumber()

    def extract_text_pdfplumber(self):
        """Fallback extraction using pdfplumber"""
        try:
            extracted_text = {}
            with pdfplumber.open(self.file_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text() or ""
                    extracted_text[i + 1] = text.strip()

            if not any(extracted_text.values()):
                raise RuntimeError("PDF contains no extractable text")

            return {
                "file_name": self.file_name,
                "total_pages": len(extracted_text),
                "pages": extracted_text
            }

        except Exception as e:
            raise RuntimeError(f"PDF extraction failed completely: {e}")
        from backend.pdf_processor import PDFProcessor

pdf_files = [
    "tests/sample_pdfs/simple_text.pdf",
    "tests/sample_pdfs/multi_column.pdf",
    "tests/sample_pdfs/complex_format.pdf"
]

for pdf in pdf_files:
    print("\n" + "=" * 60)
    print(f"Processing: {pdf}")
    print("=" * 60)

    try:
        processor = PDFProcessor(pdf)

        metadata = processor.get_pdf_metadata()
        print("Metadata:")
        for k, v in metadata.items():
            print(f"  {k}: {v}")

        result = processor.extract_text_pymupdf()
        print("\nExtracted Text:")
        for page, text in result["pages"].items():
            print(f"\n--- Page {page} ---")
            print(text[:1000])  # limit output

    except Exception as e:
        print(f"Error: {e}")
       
         