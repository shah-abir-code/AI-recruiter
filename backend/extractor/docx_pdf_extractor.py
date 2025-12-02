# backend/extractor/docx_pdf_extractor.py
import os, docx
from pdfminer.high_level import extract_text as pdf_extract

def extract_docx(path_or_bytes):
    if isinstance(path_or_bytes, (bytes, bytearray)):
        tmp = "/tmp/temp_resume.docx"
        with open(tmp, "wb") as f:
            f.write(path_or_bytes)
        path = tmp
    else:
        path = path_or_bytes
    doc = docx.Document(path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_pdf(path_or_bytes):
    try:
        if isinstance(path_or_bytes, (bytes, bytearray)):
            tmp = "/tmp/temp_resume.pdf"
            with open(tmp, "wb") as f:
                f.write(path_or_bytes)
            return pdf_extract(tmp)
        else:
            return pdf_extract(path_or_bytes)
    except Exception:
        return ""

def extract_text_from_file(uploaded):
    if isinstance(uploaded, str) and os.path.exists(uploaded):
        fn = uploaded.lower()
        if fn.endswith(".pdf"):
            return extract_pdf(uploaded)
        elif fn.endswith(".docx"):
            return extract_docx(uploaded)
        else:
            return open(uploaded, errors="ignore").read()
    else:
        raw = uploaded.read()
        name = getattr(uploaded, "name", "")
        ln = name.lower() if name else ""
        if ln.endswith(".pdf"):
            return extract_pdf(raw)
        elif ln.endswith(".docx"):
            return extract_docx(raw)
        else:
            try:
                return raw.decode("utf-8", errors="ignore")
            except:
                return ""
