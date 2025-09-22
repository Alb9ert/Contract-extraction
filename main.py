import os
import pandas as pd
from pypdf import PdfReader

FOLDER = "contracts_to_process"
OUTPUT_EXCEL = "output/contract_data.xlsx"

def list_pdfs_in_folder(folder_path=FOLDER):
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return []

    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print(f"No PDF files found in '{folder_path}'.")
    else:
        print(f"Found {len(pdf_files)} PDF file(s):")
        for f in pdf_files:
            print(f" - {f}")
    return pdf_files

def read_pdf_fields(pdf_path):
    reader = PdfReader(pdf_path)
    fields = reader.get_fields()
    data = {}

    for field_key, field in fields.items():
        question = field.get("/TU") or field.get("/T") or field_key  # Use /TU for tooltip/label if available
        value = field.get("/V")

        if isinstance(value, str):
            answer = value
        elif hasattr(value, "get_object"):
            answer = value.get_object()
        else:
            answer = str(value) if value else None

        # Store answer under field key, and keep question separately
        data[field_key] = {
            "question": question,
            "answer": answer
        }
    return data

def export_to_excel(all_data, output_path=OUTPUT_EXCEL):
    # Sørg for at mappen findes
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    combined = {}

    for filename, fields in all_data.items():
        for field_id, content in fields.items():
            question = content["question"]
            answer = content["answer"]

            if field_id not in combined:
                combined[field_id] = {"question": question}
            combined[field_id][filename] = answer

    # Konverter til DataFrame
    df = pd.DataFrame.from_dict(combined, orient="index")
    df.index.name = "Field ID"
    df = df.sort_index()

    # Gem som Excel
    df.to_excel(output_path, index=True)
    print(f"Excel file saved as '{output_path}'")


if __name__ == "__main__":
    pdf_files = list_pdfs_in_folder()
    all_data = {}

    for filename in pdf_files:
        path = os.path.join(FOLDER, filename)
        print(f"Reading: {filename}")
        data = read_pdf_fields(path)
        all_data[filename] = data

    export_to_excel(all_data)
