import os
import sys

sys.path.append('/grocery_store_pipeline/src/')

import schedule
import time

import pandas as pd

from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from exception import CustomException
from logger import logging

# Database credentials
import db_credentials


# Import from data_ingestion.py
from components.data_ingestion import DataIngestionConfig, DataIngestion

# Import from data_transformation.py
from components.data_transformation import DataTransformationConfig, DataTransformation

# Import from create_tables.py
from components.create_tables import Sales, ProductsRecieved, Products, Transactions

# Import from data_storage.py
from components.data_storage import InsertDataConfig, InsertData


#---------------------------------------------------------------------------------
#                       DATA INGESTION CONFIGURATION                             |
#---------------------------------------------------------------------------------
config = DataIngestionConfig(
    excel_file_path="./data/Los_Puche_4.xlsm",
    tables=["sales", "products_recieved", "transactions", "products"]
)
data_ingestion = DataIngestion(config)
data = data_ingestion.read_excel_workbook()
selected_tables = data_ingestion.select_tables(data)


#---------------------------------------------------------------------------------
#                   DATA TRANSFORMATION CONFIGURATION                            |
#---------------------------------------------------------------------------------
for table_name, table_data in selected_tables.items():
    if table_name == 'sales':
        sales_df = pd.read_csv("./data/CSV_tables/sales.csv")
        sales_config = DataTransformationConfig(
            data=sales_df,
            table_name="sales",
            columns_to_drop=['product_code', 'category', 'product',
                            'unit_price', 'Precio de Costo', 'Total COGS',
                            'Ganancia Neta'],
            date_columns=['date'],
            int_columns=['qty', 'product_id'],
            float_columns=['total']
        )
        sales_transformation = DataTransformation(sales_config)
        sales_transformation.clean_data()
        cleaned_sales_t = sales_config.data
    
    elif table_name == 'products_recieved':
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
    
    elif table_name == 'products':
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
        
    else:
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
        
# Cleaned tables dict
cleaned_tables = {
    'sales': cleaned_sales_t,
    'products_recieved': cleaned_pr_t,
    'products': cleaned_products_t,
    'transactions': cleaned_transactions_t
}
#---------------------------------------------------------------------------------
#                         DATA STORAGE CONFIGURATION                             |
#---------------------------------------------------------------------------------
def run_data_pipeline():
    for table_name, table_data in cleaned_tables.items():
        # Paths to cleaned CSV files
        sales_csv_path = './data/CSV_cleaned_tables/sales.csv'
        products_recieved_csv_path = './data/CSV_cleaned_tables/products_recieved.csv'
        products_csv_path = './data/CSV_cleaned_tables/products.csv'
        transactions_csv_path = './data/CSV_cleaned_tables/transactions.csv'
        
    
        try:
            # Create a new session
            session = Session()
    
            if table_name == "sales":
                # Inserting into Sales table
                logging.info("Inserting sales table into database...")
                try:
                    sales_config = InsertDataConfig(
                        model=Sales,
                        session=Session(),
                        csv_path=sales_csv_path,
                        batch_size=1000,
                        primary_key_name="sales_id"
                    )
                    sales_insertion = InsertData(sales_config)
                    sales_insertion.insert_data_into_table()
                    logging.info("Sales table stored successfully")
                except CustomException as e:
                    raise CustomException(sys, e)
                
            elif table_name == "products_recieved": 
                # Inserting into Products Recieved table
                logging.info("Inserting products_recieved table into database...")
                try:
                    pr_config = InsertDataConfig(
                        model=ProductsRecieved,
                        session=Session(),
                        csv_path=products_recieved_csv_path,
                        batch_size=200,
                        primary_key_name="purchase_id"
                    )
                    pr_insertion = InsertData(pr_config)
                    pr_insertion.insert_data_into_table()
                    logging.info("Products_recieved table stored successfully")  
                except CustomException as e:
                    raise CustomException(sys, e)  
                  
            elif table_name == "products":    
                # Inserting into Products table
                logging.info("Inserting products table into database...")
                try:
                    products_config = InsertDataConfig(
                        model=Products,
                        session=Session(),
                        csv_path=products_csv_path,
                        batch_size=100,
                        primary_key_name="product_id"
                    )
                    products_insertion = InsertData(products_config)
                    products_insertion.insert_data_into_table()
                    logging.info("Products table stored successfully") 
                except CustomException as e:
                    raise CustomException(sys, e)    
                
            else:    
                # Inserting into Transactions table
                logging.info("Inserting transactions table into database...")
                try:    
                    transactions_config = InsertDataConfig(
                        model=Transactions,
                        session=Session(),
                        csv_path=transactions_csv_path,
                        batch_size=100,
                        primary_key_name="transaction_id"
                    )
                    transactions_insertion = InsertData(transactions_config)
                    transactions_insertion.insert_data_into_table()
                    logging.info("Transactions table stored successfully")
                except CustomException as e:
                    raise CustomException(sys, e)
        
        
        finally:
            if 'session' in locals():
                session.close()             
           


if __name__=="__main__":
#---------------------------------------------------------------------------------
#                               DATABASE CONNECTION                              |
#---------------------------------------------------------------------------------
    try:
        # Engine parameters
        host = os.environ.get('DB_HOST')
        username = os.environ.get('DB_USERNAME')
        password = os.environ.get('DB_PASSWORD')
        port = os.environ.get('DB_PORT')
        database = os.environ.get('DB_DATABASE')

        # Create database URL
        db_url = f'mysql://{username}:{password}@{host}:{port}/{database}'

        # Create engine
        engine = create_engine(db_url)
        connection = engine.connect()
        
        Session = sessionmaker(bind=engine)
        
        logging.info("Connected to the database!")

       
        run_data_pipeline()
        connection.close()
        logging.info("Connection closed")
        
        schedule.run_pending()
        time.sleep(1)    

    except CustomException as e:
        raise CustomException(sys, e)
