### Grocery Store Pipeline

#### Table of Contents
- [Overview](#Overview)
- [Project Structure](#Project-Structure)
- [Pipeline Description](#Pipeline-Description)
- [Usage](#Usage)
- [Files Description](#Files-Description)
- [Dependencies](#Dependencies)
- [Issues & Limitations](#Issues--Limitations)
- [Run Locally](#Run-Locally)
- [License](#License)


#### **Overview**
I developed this project with the primary goal of automating my data workflow as a bookkeeper in a grocery store. The pipeline, when executed, performs a comprehensive Extract, Transform, Load (ETL) process:
1. Extraction: extracts records from each table within the Excel CRM Workbook.
2. Transformation: cleans and transforms each record according to specific business requirements.
3. Database Connection: utilizes SQLAlchemy and MySQL to connect to the local SQL database.
4. Table Creation: dynamically creates tables if they do not already exist in the database.
5. Periodic Data Storage: stores records periodically in the SQL database, ensuring data integrity by avoiding duplicates.
6. Allows customization of batch size for efficient processing on each run.
This pipeline streamlines the management of grocery store **sales data**, offering a systematic approach to handling records from extraction to storage while ensuring adaptability to evolving business needs.
 

#### **Project Structure** 
fausstoo/grocery_store_pipeline \
│ \
├── /data \
│   ├── /CSV_tables \
│   ├── /CSV_cleaned_tables \
│   └── /grocery_data.xlsm \
│ \
├── /MySQL \
│   ├── /db_credentials.py \
|   ├── /db_setup.py \
|   └── /Dockerfile \
│ \
├── /src \
│   ├── /components \
│   │   ├── /__init__.py \
│   │   ├── /create_tables.py \
│   │   ├── /data_ingestion.py \
│   │   ├── /data_transformation.py \
│   │   ├── /data_storage.py \
│   │   └── /pipeline.py \
│   ├── /__init__.py \
│   ├── /exception.py \
│   └── /login.py \
│ \
├── setup.py \
├── requirements.txt \
└── README.md 

#### **Pipeline Description** 
The pipeline involves three main stages and a script for each one: *extraction* (data_ingestion.py), *transformation* (data_transformation.py), and *storage* (data_storage.py). Each stage is orchestrated by the file *pipeline.py*.


#### **Usage** 
The presented project offers a comprehensive and modularized data pipeline designed for the ingestion, transformation, and storage of grocery store data. Its primary utility lies in the structured handling of data sourced from an Excel workbook, cleaning and transforming the data, and persisting it in a MySQL database. The usage of this project can be outlined as follows:

*Execution and Integration:*
To execute the data pipeline, users can run the pipeline.py script, which orchestrates the entire process seamlessly. The script establishes a connection to the MySQL database, executes data extraction, transformation, and storage processes, and logs relevant information for monitoring and debugging purposes.

*Setup:*
1. Install Python and MySQL on your computer.
2. Create a database in your local host.
3. Git clone the repository.
4. Create and activate a virtual environment.
5. Run 'requirements.txt'.
6. Modify the connector engine parameters under 'pipeline.py' and 'create_tables.py' according to your MySQL setup.
7. Run 'pipeline.py'.

*Customization and Adaptability:*
The modular structure of the project allows users to adapt and extend functionality according to specific requirements. Table structures, transformation logic, and database configurations can be modified to accommodate diverse datasets and use cases.

*Academic and Professional Application:*
This project serves as a valuable academic resource for students and researchers studying data engineering, data science, and database management. Its design principles adhere to best practices in data pipeline development, offering a practical example for educational purposes. \
In a professional context, this project applies to scenarios where structured data from Excel workbooks needs to be systematically processed and stored in a relational database. Industries such as retail, finance, and logistics could benefit from the project's capabilities in managing and analyzing large volumes of transactional data. \
The provided usage overview positions the project as a versatile and adaptable tool for managing and analyzing structured data in academic and professional settings.


#### **Files Description** 
1. *data_ingestion.py*
This script facilitates the extraction of records from an Excel workbook (Los_Puche_4.xlsm). It reads multiple sheets specified in the tables list using pandas. The selected tables are then exported as individual CSV files in the /data/CSV_tables directory. This script forms the initial step in the data pipeline, ensuring a structured and accessible format for subsequent data processing.

2. *data_transformation.py*
The data_transformation.py script is responsible for cleaning and transforming data extracted from CSV files. It utilizes the pandas library to handle tasks such as dropping unnecessary columns, filling NaN values, and transforming date and numeric columns. The script ensures the data is prepared in a consistent and standardized format, facilitating effective analysis and storage. Cleaned tables are then exported as CSV files in the /data/CSV_cleaned_tables directory, ready for storage in the MySQL database.

3. *create_tables.py*
Defines the structure of MySQL tables for the grocery store database using the SQLAlchemy ORM. It establishes a connection to the MySQL server, creates instances of tables (Sales, ProductsReceived, Products, Transactions), and checks for table existence before creation. The script ensures a systematic and organized database schema for efficient data storage and retrieval.

4. *data_storage.py*
The data_storage.py script handles the periodic insertion of cleaned data into corresponding MySQL tables. It leverages the SQLAlchemy ORM and the InsertData class to handle batch-wise insertion, optimizing performance. The InsertData class reads CSV files from the /data/CSV_cleaned_tables directory and efficiently inserts data into tables (Sales, ProductsReceived, Products, Transactions). The script ensures a seamless and optimized process for maintaining up-to-date records in the MySQL database.

5. *pipeline.py*
The pipeline.py script orchestrates the entire data pipeline, connecting to a MySQL database, and executing the data extraction, transformation, and storage processes. It utilizes the classes defined in data_ingestion.py, data_transformation.py, and data_storage.py to streamline the workflow. The script ensures a seamless and automated pipeline execution, handling the entire process from data extraction to storage. The connection details to the MySQL database are specified within the script, providing a comprehensive solution for managing grocery store data.

7. *exception.py*
The exception.py script defines a custom exception class, CustomException, to handle errors in the project. The error_message_detail function assists in generating detailed error messages by capturing information about the file, line number, and error message. The CustomException class enhances error reporting by providing specific details about where an error occurred in the Python script. This aids in debugging and understanding the context of encountered issues within the project.

8. *logger.py*
The logger.py script sets up logging functionality for the project using the Python logging module. It creates log files with timestamps in the /logs directory, enhancing traceability and organization. The script ensures that log messages contain essential information, including the timestamp, line number, and log level. Logging is configured to capture details about the project's execution, errors, and other relevant events. This contributes to effective debugging and monitoring throughout the development and execution phases of the project.


#### **Dependencies** 
pandas \
numpy \
matplotlib \
seaborn \
openpyxl \
mysql-connector-python \
SQLAlchemy \
schedule \
mysqlclient


#### **Issues & Limitations** 
While the current version of the pipeline provides a robust and efficient solution for automating the data workflow in a grocery store, it's essential to acknowledge certain limitations: 
1. Containerization and CI/CD:
The pipeline is not currently containerized. Future iterations of this project aim to implement containerization, making it more portable and scalable. Additionally, plans include the integration of Continuous Integration (CI) and Continuous Deployment (CD) practices using GitHub Actions. These enhancements will contribute to streamlined development, testing, and deployment processes.

2. Scalability:
As of now, the pipeline is optimized for small to medium-sized datasets. While it efficiently handles data from a local grocery store, scaling the pipeline for larger datasets or distributed environments may require further optimization.

3. Logging and Monitoring:
The logging functionality primarily captures essential information for debugging. Future improvements may involve enhancing logging capabilities and implementing monitoring features to provide insights into the pipeline's performance and health.

4. Adaptability to Diverse Data Sources:
The current version focuses on data extraction from an Excel CRM Workbook specific to the grocery store context. Future iterations may enhance the pipeline's adaptability to diverse data sources and formats.

#### **Run Locally**
ATTENTION: You will need to have installed MySQL Workbench previously along with a database named 'grocery_store'. You should configure '123456Fa$$' as your database password, otherwise, you can change freely this parameter in the Python scripts within the project folder. \
Initialize Git \
`git init`
Clone the repository \
`https://github.com/fausstoo/grocery_store_pipeline.git`
Enter to the project folder \
`cd grocery_store_pipeline`
Create conda environment \
`conda create -n <env_name> python=<python_version>`
Activate conda environment \
`conda activate /<env_name>`
Install packages \
`pip install -r requirements.txt`
Create the SQL tables\
`python src/components/create_tables.py`
Run the pipeline to store data
`python src/components/pipeline.py`

#### **License**
MIT License
