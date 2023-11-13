# Use a slim image as a base
FROM python:3.11-slim 

WORKDIR /grocery_store_pipeline

COPY . .

RUN apt-get update && apt-get install -y \
  default-libmysqlclient-dev \
  pkg-config \
  gcc \
  pkg-config \
  && rm -rf /var/lib/apt/lists/*
  
RUN pip install -r /grocery_store_pipeline/requirements.txt

# CMD ["python", "/grocery_store_pipeline/src/components/pipeline.py"]
