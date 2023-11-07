FROM python:3.11 AS build

WORKDIR /grocery_store_pipeline

COPY . .

RUN pip install -r requirements.txt

CMD ["python","/grocery_store_pipeline/src/components/pipeline.py"]