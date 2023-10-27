import sys
import os

sys.path.append('../../data')

from dataclasses import dataclass

from src.exception import CustomeException
from src.logger import logging

import pandas as pd

@dataclass
class DataIngestionConfig:
    excel_file_path: str
    tables: list

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def read_excel_workbook(self):
        # Read all sheets from the Excel workbook
        excel_data = pd.read_excel(self.config.excel_file_path, sheet_name=None)
        return excel_data

    def select_tables(self, excel_data):
        selected_tables = {}
        for table_name in self.config.tables:
            if table_name in excel_data:
                # Assuming 'table_name' is the sheet name
                selected_tables[table_name] = excel_data[table_name]
            else:
                print(f"Sheet '{table_name}' not found in the Excel workbook.")
        return selected_tables
 
    
    
    # Usage Example
if __name__ == "__main__":
    config = DataIngestionConfig(excel_file_path="./data/Los_Puche_4.xlsm", tables=[
        "sales", "products_recieved", "transactions", "general", "products"
    ])
    data_ingestion = DataIngestion(config)

    excel_data = data_ingestion.read_excel_workbook()
    selected_tables = data_ingestion.select_tables(excel_data)

    for table_name, table_data in selected_tables.items():
        print(f"Table Name: {table_name}")
        print(table_data.head())