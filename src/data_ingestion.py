import os
import sys
import pandas as pd
# import numpy as np
from pathlib import Path
from src.logger import logging
from src.exception import CustomException
from config.path_config import *
from utils.common_functions import read_yaml
from google.cloud import storage

class DataIngestion:
    def __init__(self, config):
        self.config = config['data_ingestion']
        self.bucket_name = self.config['bucket_name']
        self.bucket_file_names = self.config['bucket_file_names']
        self.nrows_data = self.config['nrows_data']

        # os.makedirs(RAW_DIR, exist_ok=True)
        self.raw_dir = Path(RAW_DIR)
        self.raw_dir.mkdir(parents=True, exist_ok=True)

        logging.info(f"Data Ingestion Initialized for bucket: {self.bucket_name}")

    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)

            # we willuse selective data around 5M datapoints instead of 70M rows
            for file_name in self.bucket_file_names:
                file_path = self.raw_dir / file_name
                # file_path = os.path.join(RAW_DIR, file_name)
                logging.info(f"Starting download for file: {file_name} to {file_path}")

                # Selective Data Ingestion for 'animelist.csv'
                if file_name == 'animelist.csv':
                    blob = bucket.blob(file_name)
                    blob.download_to_filename(file_path)
                    logging.info(f"Downloaded {file_name}. Now processing only the first 5M rows.")
                    data = pd.read_csv(file_path, nrows=self.nrows_data)
                    data.to_csv(file_path, index=False)
                else:
                    blob = bucket.blob(file_name)
                    blob.download_to_filename(file_path)
                    logging.info(f"Downloaded small file: {file_name}")

        except Exception as e:
            logging.error(f"Error in downloading data from GCP: {str(e)}")
            raise CustomException(f"Error downloading data from GCP: {str(e)}", e)
        

    def data_ingestion_run(self):
        try:
            logging.info("Starting Data Ingestion process...")
            self.download_csv_from_gcp()
            logging.info("Data Ingestion Completed Successfully.")
        except CustomException as e:
            logging.error(f"Custom Exception occurred during Data Ingestion: {str(e)}")
        finally:
            logging.info("DATA INGESTION STEP DONE")

if __name__ =='__main__':
    config = read_yaml(CONFIG_PATH)
    data_ingestion_obj = DataIngestion(config=config)
    data_ingestion_obj.data_ingestion_run()
