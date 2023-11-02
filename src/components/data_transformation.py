import os
import sys

sys.path.append('/data/')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from src.logger import logging
from src.exception import CustomException


from dataclasses import dataclass

@dataclass
class DataTransformationConfig:
    data: pd.DataFrame
    table_name: str
    columns_to_drop: list
    date_columns: list
    int_columns: list
    float_columns: list

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.csv_folder = "./data/CSV_cleaned_tables"
        
    
    def clean_data(self):
        logging.info("Data cleaning started...")
        
        logging.info("Removing unnecessary columns...")
        self.drop_columns()
        
        logging.info("Filling NaN values...")
        self.fill_na_values()
        
        logging.info("Removing remaining NaN values...")
        self.drop_na()
        
        logging.info("Transforming 'date' column...")
        self.transform_date_columns()
        
        logging.info("Transforming numeric columns...")
        self.transform_numeric_columns()
        
        logging.info("Exporting cleaned tables...")
        self.export_cleaned_tables_as_csv()
              
    def fill_na_values(self):
        try:    
            # Fill NaN values in 'platform' column
            platform_col = 'platform'
            if platform_col in self.config.data.columns:
                self.config.data[platform_col] = self.config.data[platform_col].fillna(" ")
                logging.info("NaN values on 'platform' successfully filled")
            # Fill NaN values in 'detail' column
            detail_col = 'detail'
            if detail_col in self.config.data.columns:
                self.config.data[detail_col] = self.config.data[detail_col].fillna(" ")
                logging.info("NaN values on 'detail' successfully filled")        
        except CustomException as e:
            raise CustomException(sys, e)
                    
    def drop_na(self):
        try:    
            self.config.data.dropna(subset=self.config.data.columns, inplace=True)
        except CustomException as e:
            raise CustomException(sys, e)
                        
    def drop_columns(self):
        try:
            for col in self.config.columns_to_drop:
                if col in self.config.data.columns:
                    self.config.data.drop(col, axis=1, inplace=True)
        except CustomException as e:
            raise CustomException(sys, e)
        
    def transform_date_columns(self):
        try:
            for col in self.config.date_columns:
                if col in self.config.data.columns:
                    self.config.data[col] = self.config.data[col].str.split(' ').str[0]
                    self.config.data[col] = pd.to_datetime(self.config.data[col], format='%Y-%m-%d')
        except CustomException as e:
            raise CustomException(sys, e)
        
    def transform_numeric_columns(self):
        try:
            for col in self.config.int_columns:
                if col in self.config.data.columns:
                    self.config.data[col] = self.config.data[col].astype(int)
            for col in self.config.float_columns:
                if col in self.config.data.columns:
                    self.config.data[col] = self.config.data[col].astype(float)
        except CustomException as e:
            raise CustomException(sys, e)
        
    def export_cleaned_tables_as_csv(self):
        try:
            logging.info("Exporting tables...")
            table_name = self.config.table_name
            # Create folder if it doesn't exist
            os.makedirs(self.csv_folder, exist_ok=True)  
            
            table_csv_path = os.path.join(self.csv_folder, f"{table_name}.csv")
            self.config.data.to_csv(table_csv_path, index=False)
            
            logging.info(f"Exported '{table_name}' as CSV to '{table_csv_path}'")
            logging.info("Table exported as CSV.")
            
        except Exception as e:
            raise CustomException(e, sys)           
            
            
if __name__ == "__main__":
    
    # SALES table
    sales_df = pd.read_csv("./data/CSV_tables/sales.csv")
    sales_config = DataTransformationConfig(
        data=sales_df,
        table_name="sales",
        columns_to_drop=['product_code', 'category', 'product', 'unit_price', 'Precio de Costo', 'Total COGS', 'Ganancia Neta'],
        date_columns=['date'],
        int_columns=['qty', 'product_id'],
        float_columns=['total']
    )

    sales_transformation = DataTransformation(sales_config)
    sales_transformation.clean_data()
    cleaned_sales_t = sales_config.data
    
    # Print or examine the cleaned data
    print(cleaned_sales_t.head())
    
    # PRODUCTS RECIEVED table
    pr_df = pd.read_csv("./data/CSV_tables/products_recieved.csv")
    pr_config = DataTransformationConfig(
        data=pr_df,
        table_name="products_recieved",
        columns_to_drop=['product', 'category'],
        date_columns=['date'],
        int_columns=['qty','product_id','purchase_id'],
        float_columns=['unit_cost', 'unit_price', 'total']
    )    

    pr_transformation = DataTransformation(pr_config)
    pr_transformation.clean_data()
    cleaned_pr_t = pr_config.data
    
    # Print or examine the cleaned data
    print(cleaned_pr_t.head())
    
    # PRODUCTS table
    products_df = pd.read_csv("./data/CSV_tables/products.csv")
    products_config = DataTransformationConfig(
        data=products_df,
        table_name="products",
        columns_to_drop=['product_code'],
        date_columns=[],
        int_columns=[],
        float_columns=['unit_cost', 'unit_price']
    )
    
    products_transformation = DataTransformation(products_config)
    products_transformation.clean_data()
    cleaned_products_t = products_config.data
    
    # Print or examine the cleaned data
    print(cleaned_products_t.head())
    
    # TRANSACTIONS table
    tr_df = pd.read_csv("./data/CSV_tables/transactions.csv")
    tr_config = DataTransformationConfig(
        data=tr_df,
        table_name="transactions",
        columns_to_drop=[],
        date_columns=['date'],
        int_columns=[],
        float_columns=['total']
    )
    
    tr_transformation = DataTransformation(tr_config)
    tr_transformation.clean_data()
    cleaned_transactions_t = tr_config.data
    
    # Print or examine the cleaned data
    print(cleaned_transactions_t.head())
    
    # Tables dict
    selected_tables = {
        'sales': cleaned_sales_t,
        'products_recieved': cleaned_pr_t,
        'products': cleaned_products_t,
        'transactions': cleaned_transactions_t
    }
    
    
    