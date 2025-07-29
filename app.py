import streamlit as st
import fitz  # PyMuPDF
from docx import Document
from fpdf import FPDF
import base64

st.set_page_config(page_title="Web PDF Editor", layout="wide")
st.title("📝 Web PDF Editor")

uploaded_pdf = st.file_uploader("Upload a PDF file", type="pdf")
text_area = ""

if uploaded_pdf:
    doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
    st.subheader("PDF Preview")
    for i, page in enumerate(doc):
        st.image(page.get_pixmap().get_image(), caption=f"Page {i+1}")

    text_area = "\n".join(page.get_text() for page in doc)
    edited_text = st.text_area("Edit Extracted Text", text_area, height=300)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Export to PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for line in edited_text.split('\n'):
                pdf.cell(200, 10, txt=line, ln=True)
            pdf.output("edited_output.pdf")
            with open("edited_output.pdf", "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                href = f'<a href="data:application/pdf;base64,{b64}" download="edited_output.pdf">📥 Download PDF</a>'
                st.markdown(href, unsafe_allow_html=True)

    with col2:
        if st.button("📄 Export to Word"):
            docx = Document()
            for line in edited_text.split('\n'):
                docx.add_paragraph(line)
            docx.save("edited_output.docx")
            with open("edited_output.docx", "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                href = f'<a href="data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{b64}" download="edited_output.docx">📥 Download Word</a>'
                st.markdown(href, unsafe_allow_html=True)
