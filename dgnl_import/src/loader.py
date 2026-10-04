import pandas as pd
import openpyxl
import os

class DataLoader:
    def __init__(self, inputs_dir="inputs"):
        self.inputs_dir = inputs_dir

    def load_excel(self, filename, sheet_name=None):
        """
        Loads an excel file from inputs directory.
        """
        file_path = os.path.join(self.inputs_dir, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file not found at: {file_path}")
            
        # Using openpyxl read-only mode to load sheet metadata or pandas for dataframes
        if sheet_name:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
        else:
            df = pd.read_excel(file_path)
        return df

    def list_input_files(self):
        """
        Lists all available input files.
        """
        return os.listdir(self.inputs_dir)

if __name__ == "__main__":
    loader = DataLoader()
    print("Available inputs:", loader.list_input_files())
