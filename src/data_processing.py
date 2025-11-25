import os
import pandas as pd
import numpy as np
import joblib
import sys
from src.logger import logging
from src.exception import CustomException
from config.path_config import *
# from sklearn.model_selection import train_test_split

# DATA PREPROCESSING

class DataProcessor:
    def __init__(self, input_file, output_dir):
        self.input_file = input_file
        self.output_dir = output_dir

        # we want self.rating_df, Xtrain, Xtest, y_train, ytest, 
        # anime_df, user2user_encodig/decoding, anime2animeencoding/decoding

        self.rating_df = None
        self.anime_df = None
        self.X_train_array = None
        self.X_test_array = None
        self.y_train = None
        self.y_test = None

        self.user2user_encoded = {}
        self.user2user_decoded = {}
        self.anime2anime_encoded = {}
        self.anime2anime_decoded = {}

        # Create output dir
        os.makedirs(self.output_dir, exist_ok=True)
        logging.info('Data Processing Intitalized!!!')

    def load_data(self, usecols):
        try:
            self.rating_df = pd.read_csv(self.input_file, low_memory=True,usecols=usecols)
            logging.info('Data loaded successfully for processing')
        except Exception as e:
            raise CustomException("Failed to load data",sys)
        
    # def filter_users(self, min_rating=400):
    #     try:
    #         n_rating = self.rating_df['user_id'].value_counts()
    #         self.rating_df = self.rating_df[self.rating_df['user_id'].isin(n_rating[n_rating>=400].index)].copy()
    #         logging.info("Filtered users sucesfully...")
    #         logging.info(f"Filtered out users with fewer than {min_rating} ratings. Remaining users: {self.rating_df['user_id'].nunique()}")
    #     except Exception as e:
    #         logging.error(f"Error in filter_users: {str(e)}")
    #         raise CustomException("Failed to filter users based on rating threshold.", sys)
        
    def filter_users(self, min_rating=400):
        try:
            user_counts = self.rating_df.groupby('user_id').size()
            self.rating_df = self.rating_df[self.rating_df['user_id'].isin(user_counts[user_counts >= min_rating].index)].copy()
            logging.info(f"Filtered out users with fewer than {min_rating} ratings. Remaining users: {self.rating_df['user_id'].nunique()}")
        except Exception as e:
            logging.error(f"Error in filter_users: {str(e)}")
            raise CustomException("Failed to filter users based on rating threshold.", sys)

        
    def scale_ratings(self):
        try:
            min_rating = min(self.rating_df['rating'])
            max_rating = max(self.rating_df['rating'])

            self.rating_df['rating'] = self.rating_df['rating'].apply(lambda x: (x-min_rating)/(max_rating-min_rating)).values.astype(np.float64)
            logging.info('Scaled data successfuly...')
        except Exception as e:
            raise CustomException("Failed to Scale data",sys)
        
    def encode_data(self):
        try:
            # USERS
            user_ids = self.rating_df['user_id'].unique().tolist()
            self.user2user_encoded = { x : i for i,x in enumerate(user_ids)}
            self.user2user_decoded = { i : x for i,x in enumerate(user_ids)}
            self.rating_df['user'] = self.rating_df['user_id'].map(self.user2user_encoded)

            # ANIME
            anime_ids = self.rating_df['anime_id'].unique().tolist()
            self.anime2anime_encoded = {x : i for i,x in enumerate(anime_ids)}
            self.anime2anime_decoded = {i : x for i,x in enumerate(anime_ids)}
            self.rating_df['anime'] = self.rating_df['anime_id'].map(self.anime2anime_encoded)

            logging.info('USERS and ANIME Encodig data successfuly...')

        except Exception as e:
            raise CustomException("Failed to Encode data",sys)
        

    def split_data(self, test_size=1000, random_state=24):
        try:
            self.rating_df = self.rating_df.sample(frac=1, random_state=43).reset_index(drop=True)
            X = self.rating_df[['user', 'anime']].values
            y = self.rating_df['rating']

            train_indices = self.rating_df.shape[0] - test_size

            X_train, X_test, y_train, y_test = (
                                                X[:train_indices],
                                                X[train_indices:],
                                                y[:train_indices],
                                                y[train_indices :],
                                            )
            
            self.X_train_array = [X_train[:, 0], X_train[:, 1]]
            self.X_test_array = [X_test[:, 0], X_test[:, 1]]

            self.y_train = y_train
            self.y_test = y_test
            logging.info('Data splitted successfully...')
        except Exception as e:
            raise CustomException("Failed to Split data",sys)
        
    def save_artifacts(self):
        try:
            artifacts = {
                'user2user_encoded' : self.user2user_encoded,
                'user2user_decoded' : self.user2user_decoded,
                'anime2anime_encoded' : self.anime2anime_encoded,
                'anime2anime_decoded' : self.anime2anime_decoded,
            }

            for name, data in artifacts.items():
                joblib.dump(data, os.path.join(self.output_dir, f"{name}.pkl"))
                logging.info(f"{name} saved sucesfully in processed directory")

            joblib.dump(self.X_train_array, X_TRAIN_ARRAY)
            joblib.dump(self.X_test_array, X_TEST_ARRAY)
            joblib.dump(self.y_train, Y_TRAIN)
            joblib.dump(self.y_test, Y_TEST)

            self.rating_df.to_csv(RATING_DF, index = False)
            logging.info('All the training/testing data and rating_df is saved')
        except Exception as e:
            raise CustomException("Failed to save artifacts data",sys)
        
    def process_anime_data(self):
        try:
            anime_df = pd.read_csv(ANIME_CSV)
            cols = ["MAL_ID","Name","Genres","sypnopsis"]
            synopsis_df = pd.read_csv(ANIMESYNOPSIS_CSV, usecols=cols)

            anime_df = anime_df.replace('Unknown', np.nan)

            def getAnimeName(anime_id):
                try:
                    name = anime_df[anime_df.anime_id == anime_id].eng_version.values[0]
                    if name is np.nan:
                        name = anime_df[anime_df.anime_id == anime_id].Name.values[0]
                except Exception as e:
                    logging.error(f"Error fetching anime name for anime_id: {anime_id} - {str(e)}")
                return name

            
            anime_df["anime_id"] = anime_df["MAL_ID"]
            anime_df["eng_version"] = anime_df["English name"]
            anime_df["eng_version"] = anime_df.anime_id.apply(lambda x:getAnimeName(x))

            # Sort the anime df by score with descending order

            anime_df.sort_values(by=["Score"],
                        inplace=True,
                        ascending=False,
                        kind="quicksort",
                        na_position="last")
            
            anime_df = anime_df[["anime_id" , "eng_version","Score","Genres","Episodes","Type","Premiered","Members"]]

            # def getSynopsis(anime,anime_df):
            #     if isinstance(anime,int):
            #         return synopsis_df[synopsis_df.MAL_ID == anime].sypnopsis.values[0]
            #     if isinstance(anime, str):
            #         return synopsis_df[synopsis_df.Name == anime].sypnopsis.values[0]

            # anime_df.to_csv(ANIME_DF, index=False)
            # synopsis_df.to_csv(SYNOPISIS_DF, index=False)
            logging.info("ANIME_DF AND SYNOPSIS_Df saved sucesfullyy...")
        except Exception as e:
            raise CustomException("Failed to save animje and anime_synopsis data",sys)
        
    
    def processor_run(self):
        try:
            self.load_data(usecols=['user_id','anime_id', 'rating'])
            self.filter_users()
            self.scale_ratings()
            self.encode_data()
            self.split_data()
            self.save_artifacts()
            self.process_anime_data()
            logging.info('Data Processing Pipleine run successfully...')
        except Exception as e:
            raise CustomException("Failed to run data processing",sys)
        

# Test pipleine
if __name__=='__main__':
    data_processor_obj = DataProcessor(ANIMELIST_CSV, PROCESSED_DIR)
    data_processor_obj.processor_run()