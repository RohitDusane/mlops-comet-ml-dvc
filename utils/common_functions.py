import os
import sys
import pandas as pd

from src.logger import logging
from src.exception import CustomException
import yaml

def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'File not found!!!')
        
        with open(file_path, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
            logging.info('Successfully read the YAML file')
            return config
    except Exception as e:
        logging.error('Error while reding YAML file')
        raise CustomException('Failed to read YAML file')