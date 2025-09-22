import os

# Checks if folder exist 
def list_pdfs_in_folder(folder_path="contracts_to_process"):
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist. Please create it and add PDFs.")
        return []
    # extracts pdf files to array
    pdf_files = [
        f for f in os.listdir(folder_path)
        if f.lower().endswith(".pdf")
    ]

    # if no errors are found
    if not pdf_files:
        print(f"No PDF files found in '{folder_path}'. Please add some PDFs.")
    else:
        # print pdf file names
        print(f"Found {len(pdf_files)} PDF file(s) in '{folder_path}':")
        for f in pdf_files:
            print(f" - {f}")
    return pdf_files


# run file if its the main cript
if __name__ == "__main__":
    list_pdfs_in_folder()
