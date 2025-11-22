from src.logger import logging
from src.exception import CustomException
from config.path_config import *
from utils.common_functions import read_yaml
from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessor
from src.model_training import ModelTraining



if __name__ =='__main__':
    # config = read_yaml(CONFIG_PATH)
    # data_ingestion_obj = DataIngestion(config=config)
    # data_ingestion_obj.data_ingestion_run()

    data_processor_obj = DataProcessor(ANIMELIST_CSV, PROCESSED_DIR)
    data_processor_obj.processor_run()

    model_trainer = ModelTraining(PROCESSED_DIR)
    model_trainer.train_model()