import sys
import os

sys.path.append('../../data')

import pandas as pd

from dataclasses import dataclass

from src.exception import CustomException
from src.logger import logging



@dataclass
class DataIngestionConfig:
    excel_file_path: str
    tables: list

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
        self.temp_csv_folder = "./data/CSV_tables"

    def read_excel_workbook(self):
        try:
            # Read all sheets from the Excel workbook
            excel_data = pd.read_excel(self.config.excel_file_path, sheet_name=None)
            return excel_data
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def select_tables(self, excel_data):
        try:
            selected_tables = {}
            for table_name in self.config.tables:
                if table_name in excel_data:
                    # Assuming 'table_name' is the sheet name
                    selected_tables[table_name] = excel_data[table_name]
                else:
                    print(f"Sheet '{table_name}' not found in the Excel workbook.")
            return selected_tables  
            
        except Exception as e:
            raise CustomException(e, sys)
        
        
    def export_tables_as_csv(self, selected_tables):
        try:
            os.makedirs(self.temp_csv_folder, exist_ok=True)  # Create folder if it doesn't exist
            for table_name, table_data in selected_tables.items():
                table_csv_path = os.path.join(self.temp_csv_folder, f"{table_name}.csv")
                table_data.to_csv(table_csv_path, index=False)
                print(f"Exported '{table_name}' as CSV to '{table_csv_path}'")
                
        except Exception as e:
            raise CustomException(e, sys)
 
    
    
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
        
        
    # Export selected tables as CSVs
    data_ingestion.export_tables_as_csv(selected_tables)