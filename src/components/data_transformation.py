import os
import sys

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from src.logger import logging
from src.exception import CustomException

sales_df = pd.read_csv("./../../data/CSV_tables/sales.csv")

sales_df.info()

sales_df.head()
sales_df.tail()

sales_df.dropna(subset=['category', 'product', 'qty', 'employee', 'product_id'], inplace=True)

sales_df['platform'] = sales_df['platform'].fillna("")


sales_df.isna().sum()

sales_df['date'] = sales_df['date'].str.split(' ').str[0]

sales_df['date'] = pd.to_datetime(sales_df['date'], format='%Y-%m-%d')

sales_df['qty'] = sales_df['qty'].astype(int)
sales_df['total'] = sales_df['total'].astype(float)
sales_df['product_id'] = sales_df['product_id'].astype(int)

sales_df.drop(['product_code', 'category', 'product',
               'unit_price', 'Precio de Costo',
               'Total COGS', 'Ganancia Neta'], axis=1, inplace=True)