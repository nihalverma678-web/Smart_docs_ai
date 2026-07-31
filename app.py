import streamlit as st

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="SmartDocs AI",
    page_icon="📄",
    layout="wide"
)

# -------------------- SIDEBAR --------------------
st.sidebar.header("📤 Upload Documents")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF files (Max 10MB each)",
    type=["pdf"],
    accept_multiple_files=True,
    help="You can upload multiple PDF documents. Only .pdf files are allowed."
)

# -------------------- MAIN HEADER --------------------
st.title("📄 SmartDocs AI")
st.markdown(
    """
    **SmartDocs AI** helps you upload and process PDF documents efficiently.

    ### How to use this app:
    1. Upload one or more PDF files using the sidebar.
    2. Ensure each file is under **10MB**.
    3. Click **Process Documents** to start processing.
    """
)

st.markdown("---")

# -------------------- FILE VALIDATION --------------------
MAX_FILE_SIZE_MB = 10
valid_files = []
errors = []

if uploaded_files:
    for file in uploaded_files:
        file_size_mb = file.size / (1024 * 1024)

        if not file.name.lower().endswith(".pdf"):
            errors.append(f"❌ {file.name}: Invalid file type")
        elif file_size_mb > MAX_FILE_SIZE_MB:
            errors.append(f"❌ {file.name}: File size exceeds 10MB")
        else:
            valid_files.append((file, round(file_size_mb, 2)))

# -------------------- FILE COUNT --------------------
st.markdown(f"### 📊 Files Uploaded: **{len(uploaded_files) if uploaded_files else 0}**")

# -------------------- DISPLAY FILE DETAILS --------------------
if valid_files:
    st.subheader("📁 Uploaded File Details")
    for idx, (file, size) in enumerate(valid_files, start=1):
        st.markdown(f"**{idx}. {file.name}** — {size} MB")

# -------------------- DISPLAY ERRORS --------------------
for error in errors:
    st.error(error)

# -------------------- PROCESS BUTTON --------------------
st.markdown("---")

if st.button("🚀 Process Documents", help="Click to process the uploaded PDF files"):
    if not uploaded_files:
        st.error("Please upload at least one PDF file before processing.")
    elif errors:
        st.error("Fix the errors above before processing.")
    else:
        st.success(f"✅ {len(valid_files)} document(s) processed successfully!")

# -------------------- FOOTER --------------------
st.markdown(
    """
    <hr style="margin-top:40px;">
    <center><small>SmartDocs AI © 2026 | Document Intelligence Platform</small></center>
    """,
    unsafe_allow_html=True
)
streamlit run frontend/app.py