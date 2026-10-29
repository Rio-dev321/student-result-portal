import streamlit as st
import pdfplumber
import pandas as pd

st.set_page_config(
    page_title="Imran Public School",
    page_icon="🎓",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background-color: #101010;
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🎓 Imran Public School")
st.subheader("Student Result Portal")

st.write("Upload the school result PDF to check student results.")

pdf_file = st.file_uploader(
    "Upload Result PDF",
    type=["pdf"]
)

if pdf_file:
    records = []

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()

            for table in tables:
                for row in table:
                    if row and len(row) >= 5:
                        records.append(row)

    if records:
        df = pd.DataFrame(records)
        df = df.dropna(how="all")

        st.success("PDF data loaded!")

        search = st.text_input(
            "Enter student name or roll number"
        )

        if search:
            mask = df.astype(str).apply(
                lambda col: col.str.contains(
                    search, case=False, na=False
                )
            ).any(axis=1)

            result = df[mask]

            if not result.empty:
                st.subheader("Your Result")
                st.dataframe(result, use_container_width=True)
            else:
                st.warning("No matching result found.")
    else:
        st.warning(
            "Table data could not be extracted from this PDF."
        )
