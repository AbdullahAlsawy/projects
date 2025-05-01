# utils/file_utils.py

import pandas as pd

def save_to_file(data_rows, filename, file_format="csv"):
    if file_format == "xlsx":
        df = pd.DataFrame(data_rows, columns=["Product Name", "Price", "Product Link"])
        df.to_excel(filename, index=False)
    else:
        raise ValueError("Only Excel (xlsx) saving is supported here. Use csv manually in the scraper.")


# في ملف file_utils.py
from tkinter import filedialog

def choose_folder(selected_folder_var):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        selected_folder_var.set(folder_selected)

# في ملف filters.py


