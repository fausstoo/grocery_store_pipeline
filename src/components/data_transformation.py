import os
import sys

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
    columns_to_drop: list
    date_columns: list
    int_columns: list
    float_columns: list

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        
        
    def clean_data(self):
        self.drop_columns()
        self.transform_date_columns()
        self.transform_numeric_columns()
        self.fill_na_values()
            
    def drop_columns(self):
        for col in self.config.columns_to_drop:
            if col in self.config.data.columns:
                self.config.data.drop(col, axis=1, inplace=True)

    def transform_date_columns(self):
        for col in self.config.date_columns:
            if col in self.config.data.columns:
                self.config.data[col] = pd.to_datetime(self.config.data[col], format='%Y-%m-%d')

    def transform_numeric_columns(self):
        for col in self.config.int_columns:
            if col in self.config.data.columns:
                self.config.data[col] = self.config.data[col].astype(int)
        for col in self.config.float_columns:
            if col in self.config.data.columns:
                self.config.data[col] = self.config.data[col].astype(float)
                
    def fill_na_values(self):
        # Fill NaN values in 'platform' column
        platform_col = 'platform'
        if platform_col in self.config.data.columns:
            self.config.data[platform_col] = self.config.data[platform_col].fillna("")

        # Fill NaN values in 'detail' column
        detail_col = 'detail'
        if detail_col in self.config.data.columns:
            self.config.data[detail_col] = self.config.data[detail_col].fillna("")
            
            
            
if __name__ == "__main__":
    # SALES table
    sales_df = pd.read_csv("/data/CSV_tables/sales.csv")
    
    sales_config = DataTransformationConfig(
        data=sales_df,
        columns_to_drop=['product_code', 'category', 'product', 'unit_price', 'Precio de Costo', 'Total COGS', 'Ganancia Neta'],
        date_columns=['date'],
        int_columns=['qty', 'product_id'],
        float_columns=['total']
    )

    sales_transformation = DataTransformation(sales_config)
    sales_transformation.clean_data()
    
    # Print or examine the cleaned data
    print(sales_config.data.head())
    
    # PRODUCTS RECIEVED table
    
    pr_df = pd.read_csv("/data/CSV_tables/products_recieved.csv")
    pr_config = DataTransformationConfig(
        data=pr_df,
        columns_to_drop=['product', 'category'],
        date_columns=['date'],
        int_columns=['qty','product_id','purchase_id'],
        float_columns=['total']
    )    

    pr_transformation = DataTransformation(pr_config)
    pr_transformation.clean_data()
    
    # Print or examine the cleaned data
    print(pr_config.data.head())
    
    # TRANSACTIONS
    tr_df = pd.read_csv("/data/CSV_tables/transactions.csv")
    
    tr_config = DataTransformationConfig(
        data=tr_df,
        columns_to_drop=[],
        date_columns=['date'],
        int_columns=[],
        float_columns=['total']
    )
    
    tr_transformation = DataTransformation(tr_config)
    tr_transformation.clean_data()
    
    # Print or examine the cleaned data
    print(tr_config.data.head())