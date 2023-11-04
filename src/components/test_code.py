
import os
import sys

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from src.logger import logging
from src.exception import CustomException
from src.components.data_transformation import DataTransformationConfig
from src.components.data_transformation import DataTransformation


sales_df = pd.read_csv("./../../data/CSV_cleaned_tables/transactions.csv")

sales_df.isna().sum()

# Configuration for transforming the 'sales' table
sales_transformation_config = DataTransformationConfig(
    data=sales_df,
    columns_to_drop=[
        'product_code', 'category', 'product', 'unit_price', 'Precio de Costo',
        'Total COGS', 'Ganancia Neta'
    ],
    date_columns=['date'],
    int_columns=['qty', 'product_id'],
    float_columns=['total']
)

# DataTransformation instance
sales_transformation = DataTransformation(sales_transformation_config)

# Clean and transform the 'sales' table
sales_transformation.clean_data()

# Show cleaned 'sales' table
sales_transformation_config.data.info()





#-------------------------------------------------------------------------

pr_df = pd.read_csv("./../../data/CSV_tables/products_recieved.csv")


# Configuration for transforming 'products_recieved' table
pr_config = DataTransformationConfig(
    data=pr_df,
    columns_to_drop=[
        'product',
        'category'
    ],
    date_columns=['date'],
    int_columns=[
        'qty',
        'product_id',
        'purchase_id'
    ],
    float_columns=['total']
)

# 'products_recieved' transformation instance
pr_transformation = DataTransformation(pr_config)

# Clean and transform 'products_recieved' table
pr_transformation.clean_data()

# Show cleaned 'products_recieved' table
pr_config.data.info()


#-------------------------------------------------------------------------



tr_df = pd.read_csv("./../../data/CSV_tables/transactions.csv")

# Configuration for transforming 'transactions' table
tr_config = DataTransformationConfig(
    data=tr_df,
    date_columns=['date'],
    float_columns=['total'],
    columns_to_drop=[],
    int_columns=[]
)

# 'transactions' transformation instance
tr_transformation = DataTransformation(tr_config)

# Clean and trasnform 'transactions' table
tr_transformation.clean_data()

# Show cleaned 'transactions' table
tr_config.data.info()