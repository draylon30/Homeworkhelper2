import streamlit as st
import fitz  # PyMuPDF
from docx import Document
from fpdf import FPDF
import base64

# === CONFIGURATION ===
st.set_page_config(
    page_title="PDF Editor",
    page_icon="📝",
    layout="wide",
)

# === STYLE ===
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .block-container {
        padding: 2rem 1rem;
    }
    h1 {
        color: #1f4e79;
    }
    .stButton button {
        background-color: #1f4e79;
        color: white;
        font-weight: bold;
        border-radius: 8px;
    }
    .stTextArea textarea {
        background-color: #fff;
        border: 1px solid #ccc;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# === TITLE ===
st.title("📝 PDF Text Editor (Web App)")
st.caption("Upload, edit, and export PDFs directly in your browser.")

# === UPLOAD FILE ===
uploaded_pdf = st.file_uploader(
    "📤 Upload your PDF file (Max: 1000 MB)", 
    type=["pdf"], 
    accept_multiple_files=False,
    label_visibility="visible"
)

# Force 1000MB max limit (Streamlit default is lower, but this forces warning for user)
MAX_MB = 1000
if uploaded_pdf and uploaded_pdf.size > MAX_MB * 1024 * 1024:
    st.error("❌ File size exceeds 1000MB limit. Please upload a smaller file.")
    uploaded_pdf = None

if uploaded_pdf:
    doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
    
    st.subheader("📄 PDF Preview")
    for i, page in enumerate(doc):
        st.image(page.get_pixmap().get_image(), caption=f"Page {i+1}", use_column_width=True)

    # Extract text
    text_area = "\n".join(page.get_text() for page in doc)
    st.subheader("✏️ Edit Text Extracted from PDF")
    edited_text = st.text_area("Make changes here:", text_area, height=300)

    st.divider()

    # === EXPORT BUTTONS ===
    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Export as PDF"):
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
        if st.button("📄 Export as Word (.docx)"):
            docx = Document()
            for line in edited_text.split('\n'):
                docx.add_paragraph(line)
            docx.save("edited_output.docx")
            with open("edited_output.docx", "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                href = f'<a href="data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{b64}" download="edited_output.docx">📥 Download Word</a>'
                st.markdown(href, unsafe_allow_html=True)
