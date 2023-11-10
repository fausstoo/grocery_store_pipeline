import sys
import os

sys.path.append('/grocery_store_pipeline/src/')
sys.path.append('/grocery_store_pipeline/data/')

import pandas as pd

from sqlalchemy.orm import Session

from src.components.create_tables import Sales, ProductsRecieved, Products, Transactions

from src.exception import CustomException
from src.logger import logging

from dataclasses import dataclass

# Create function to insert data periodically
@dataclass
class InsertDataConfig:
    session: type
    csv_path: str
    batch_size: int
    primary_key_name: str

class InsertData:
    def __init__(self, config: InsertDataConfig):
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
                    if 'sales_id' in row:
                        # Directly reference columns of the Sales table structure
                        instance = Sales(**row.to_dict())
                    elif 'purchase_id' in row:
                        # Directly reference columns of the ProductsRecieved table structure
                        instance = ProductsRecieved(**row.to_dict())
                    elif 'product_id' in row:
                        # Directly reference columns of the Products table structure
                        instance = Products(**row.to_dict())
                    elif 'transaction_id' in row:
                        # Directly reference columns of the Transactions table structure
                        instance = Transactions(**row.to_dict())
                    else:
                        raise CustomException(sys, "Unknown table structure")

                    session = self.config.session

                    # Check if a record with the same primary key or unique constraint already exists
                    primary_key_name = self.config.primary_key_name
                    existing_record = session.query(instance.__class__).filter_by(
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
            raise CustomException(sys, e)