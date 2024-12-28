import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO

def extract_tables_from_pdf(pdf_file):
    try:
        all_tables = []
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    all_tables.append(table)
        return all_tables
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def save_tables_to_excel(tables):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for i, table in enumerate(tables):
            df = pd.DataFrame(table)
            df.to_excel(writer, sheet_name=f"Table_{i+1}", index=False, header=False)
        writer.save()
    output.seek(0)
    return output

# Streamlit App
st.title("PDF Table to Excel Converter")

# File Upload
uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_pdf:
    st.success("PDF uploaded successfully!")
    
    # Extract Tables
    st.write("Extracting tables...")
    tables = extract_tables_from_pdf(uploaded_pdf)
    
    if tables:
        st.success(f"Found {len(tables)} table(s).")
        
        # Option to download the Excel file
        excel_file = save_tables_to_excel(tables)
        st.download_button(
            label="Download Excel File",
            data=excel_file,
            file_name="extracted_tables.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("No tables found in the PDF.")
