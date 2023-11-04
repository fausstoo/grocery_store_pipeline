import sys
import os

import pandas as pd

from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from src.components.create_tables import Sales
from src.components.create_tables import ProductsRecieved
from src.components.create_tables import Products
from src.components.create_tables import Transactions

from src.exception import CustomException
from src.logger import logging


from dataclasses import dataclass


# Create function to insert data periodically
@dataclass
class InsertDataConfig:
    model: type
    session: type
    csv_path: str
    batch_size: int
    primary_key_name: str
    
class InsertData:
    def __init__(self, config:InsertDataConfig):
        self.config = config
        
    def insert_data_into_table(self):
        logging.info("Data insertion started...")
        try:
                
            data = pd.read_csv(self.config.csv_path)
            total_rows = len(data)

            for start in range(0, total_rows, self.config.batch_size):
                end = start + self.config.batch_size
                batch = data[start:end]

                for index, row in batch.iterrows():
                    instance = self.config.model(**row.to_dict())
                    session = self.config.session

                    # Check if a record with the same primary key or unique constraint already exists
                    primary_key_name = self.config.primary_key_name
                    existing_record = session.query(self.config.model).filter_by(
                        **{primary_key_name: getattr(instance, primary_key_name)}
                    ).first()

                    if existing_record:
                        # Update the existing record with new data
                        for key, value in row.items():
                            setattr(existing_record, key, value)
                    else:
                        # Insert the new record
                        session.add(instance)

                self.config.session.commit()
                
        except CustomException as e:
            raise CustomException(sys,e)    
        
if __name__=="__main__":
    
    # Engine parameters
    host = '127.0.0.1'
    username = 'root'
    password = '40179589Fa$$'
    port = 3306
    database = 'grocery_store'

    # Create database URL
    db_url = f'mysql://{username}:{password}@{host}:{port}/{database}'

    # Create engine
    engine = create_engine(db_url)


    try:
        connection = engine.connect()
        
        logging.info("Connected to the database!")
        

        Session = sessionmaker(bind=engine)


        # Paths to cleaned CSV files
        sales_csv_path = './data/CSV_cleaned_tables/sales.csv'
        products_recieved_csv_path = './data/CSV_cleaned_tables/products_recieved.csv'
        products_csv_path = './data/CSV_cleaned_tables/products.csv'
        transactions_csv_path = './data/CSV_cleaned_tables/transactions.csv'

        # Inserting into Sales table
        logging.info("Inserting sales table into database...")
        try:
            sales_config = InsertDataConfig(
                model=Sales,
                session=Session(),
                csv_path=sales_csv_path,
                batch_size=100,
                primary_key_name="sales_id"
            )
            sales_insertion = InsertData(sales_config)
            sales_insertion.insert_data_into_table()
            logging.info("Sales table stored successfully")
            
        except CustomException as e:
            raise CustomException(sys, e)
        
        
        # Inserting into Products Recieved table
        logging.info("Inserting products_recieved table into database...")
        try:
            pr_config = InsertDataConfig(
                model=ProductsRecieved,
                session=Session(),
                csv_path=products_recieved_csv_path,
                batch_size=100,
                primary_key_name="purchase_id"
            )
            pr_insertion = InsertData(pr_config)
            pr_insertion.insert_data_into_table()
            logging.info("Products_recieved table stored successfully")
            
        except CustomException as e:
            raise CustomException(sys, e)    
        
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
            if 'connection' in locals():
                connection.close()
                print("Connection closed")    
                
    except CustomException as e:
        raise CustomException(sys, e)

    