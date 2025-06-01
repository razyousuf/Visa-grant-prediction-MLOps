from google.cloud import bigquery
from airflow.models import Variable
import pymongo
import pandas as pd
import os

def main():
    # Read credentials from Airflow variables
    mongodb_db = Variable.get("DB_NAME")
    mongodb_coll_name = Variable.get("COLLECTION_NAME")

    gcp_key_path = Variable.get("GCP_KEY_PATH")
    project_id = Variable.get("GCP_PROJECT_ID")
    dataset_id = Variable.get("BQ_DATASET")
    table_id = Variable.get("BQ_TABLE")
    mongodb_uri = Variable.get("MONGODB_CREDENTIAL")

    # Set Google credentials for BigQuery
    print("Connecting to BigQuery...")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcp_key_path

    # MongoDB connection
    print("Connecting to MongoDB...")
    client = pymongo.MongoClient(mongodb_uri)
    db = client[mongodb_db]
    collection = db[mongodb_coll_name]

    # Convert collection to DataFrame
    print("Converting collection to DataFrame...")
    df = pd.DataFrame(list(collection.find()))
    if df.empty:
        print("No data found in MongoDB.")
        return
    if "_id" in df.columns:
        df.drop(columns=["_id"], inplace=True)

    # BigQuery client and table ref
    print("Uploading to BigQuery...")
    bq_client = bigquery.Client()
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    # Load DataFrame to BigQuery
    job = bq_client.load_table_from_dataframe(df, table_ref)
    job.result()

    print("Upload complete.")
