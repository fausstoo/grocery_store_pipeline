import sys
import os

sys.path.append('./src/')
sys.path.append('./data/')

import pandas as pd

from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

from exception import CustomException
from logger import logging
# import db_credentials

# Engine parameters
host = os.environ['DB_HOST']
username = os.environ['DB_USERNAME']
password = os.environ['DB_PASSWORD']
port = int(os.environ['DB_PORT'])
database = os.environ['DB_DATABASE']

# Create database URL
db_url = f'mysql://{username}:{password}@{host}:{port}/{database}'

# Create engine
engine = create_engine(db_url)

# Create declarative base for the model
Base = declarative_base()

try:
    connection = engine.connect()
    
    logging.info("Connected to MySQL database!")


    class Sales(Base):
        __tablename__ = 'sales' 
        sales_id = Column(Integer, primary_key=True)
        invoice_number = Column(Integer)
        date = Column(Date)
        employee = Column(String(16))
        payment_type = Column(String(16))
        platform = Column(String(16))
        qty = Column(Integer)
        total = Column(Float)
        product_id = Column(Integer)

    class ProductsRecieved(Base):
        __tablename__ = 'products_recieved' 
        purchase_id = Column(Integer, primary_key=True)
        invoice_number = Column(Integer)
        date = Column(Date)
        employee = Column(String(16))
        account = Column(String(16))
        platform = Column(String(16))
        unit_cost = Column(Float)
        qty = Column(Integer)
        unit_price = Column(Float)
        total = Column(Float)
        product_id = Column(Integer)
        
    class Products(Base):
        __tablename__ = 'products' 
        product = Column(String(66))
        category = Column(String(16))
        unit_cost = Column(Float)
        unit_price = Column(Float)
        product_id = Column(Integer, primary_key=True)
        
    class Transactions(Base):
        __tablename__ = 'transactions' 
        transaction_id = Column(Integer, primary_key=True)
        date = Column(Date)
        account = Column(String(16))
        transaction_type = Column(String(16))
        category = Column(String(16))
        detail =Column(String(24))
        total = Column(Float)
            
    # Create the tables in the database
   # Base.metadata.create_all(engine)

    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

except CustomException as e:
    raise CustomException(sys, e)
