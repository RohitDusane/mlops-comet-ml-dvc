import os
from pathlib import Path

############# DATA INGESTION #############

RAW_DIR = Path('artifacts/raw')
CONFIG_PATH = Path('config/config.yaml')

############# DATA PROCESSING #############

PROCESSED_DIR = Path('artifacts/processed')
ANIMELIST_CSV = Path('artifacts/raw/animelist.csv')

X_TRAIN_ARRAY = os.path.join(PROCESSED_DIR, 'X_train_array.pkl')
X_TEST_ARRAY = os.path.join(PROCESSED_DIR, 'X_test_array.pkl')
Y_TRAIN = os.path.join(PROCESSED_DIR, 'y_train.pkl')
Y_TEST = os.path.join(PROCESSED_DIR, 'y_test.pkl')


ANIME_CSV = Path('artifacts/raw/anime.csv')
ANIMESYNOPSIS_CSV = Path('artifacts/raw/anime_with_synopsis.csv')

RATING_DF = os.path.join(PROCESSED_DIR, 'rating_df.csv')
ANIME_DF = os.path.join(PROCESSED_DIR, 'anime.csv')
SYNOPISIS_DF = os.path.join(PROCESSED_DIR, 'synopsos_df.csv')


USER2USER_ENCODED = Path('artifacts/processed/user2user_encoded.pkl')
USER2USER_DECODED = Path('artifacts/processed/user2user_decoded.pkl')
ANIME2ANIME_ENCODED = Path('artifacts/processed/anime2anime_encoded.pkl')
ANIME2ANIME_DECODED = Path('artifacts/processed/anime2anime_decoded.pkl')


############# MODEL TRAINING #############
MODEL_DIR = Path('artifacts/model')
WEIGHTS_DIR = Path('artifacts/weights')
MODEL_PATH = Path(MODEL_DIR, 'model.keras')
ANIME_WEIGHTS_PATH = Path(WEIGHTS_DIR, 'anime_weights.pkl')
USER_WEIGHTS_PATH = Path(WEIGHTS_DIR, 'user_weights.pkl')
CHECKPOINT_FILEPATH =  Path('artifacts/model_checkpoits/weights.weights.h5')
