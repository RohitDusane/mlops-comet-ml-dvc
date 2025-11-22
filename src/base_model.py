# MODEL ARCHITECTURE

import tensorflow
from tensorflow.keras import layers
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Activation, BatchNormalization,Input,Embedding,Dot,Dense,Flatten
from tensorflow.keras.regularizers import l2
from wordcloud import WordCloud

from utils.common_functions import read_yaml
from src.logger import logging
from src.exception import CustomException

class BaseModel:
    def __init__(self, config_path):
        try:
            self.config = read_yaml(config_path)
            logging.info("Loaded configuration from config.yaml")
        except Exception as e:
            raise CustomException("Error loading configuration",e)
        
    # Create a tensorflow model 
    def RecommenderNet(self, n_users, n_anime):
        try:
            embedding_size = self.config['model']['embedding_size']

            user = Input(name='user', shape=[1])

            user_embedding = Embedding(name='user_embedding', 
                                    input_dim = n_users,
                                    output_dim = embedding_size,
                                    embeddings_regularizer=l2(1e-5))(user)
            anime = Input(name='anime', shape=[1])
            anime_embedding = Embedding(name='anime_embedding', 
                                    input_dim = n_anime,
                                    output_dim = embedding_size,
                                    embeddings_regularizer=l2(1e-5))(anime)
            
            # DOT Layer - dot product ---- similarity
            x = Dot(name='dot_product',
                    normalize = True,
                    axes = 2)([user_embedding, anime_embedding])
            
            # Flatten all output --- 128 dimenation vector into 1 dimensional
            x = Flatten()(x)

            # Dense, BatchNormaliztion, Activatio
            x = Dense(1, kernel_initializer='he_normal')(x)
            x = BatchNormalization()(x)
            x = Activation('sigmoid')(x)

            # make a model Layer
            model = Model(inputs=[user, anime], outputs=x)
            model.compile(
                loss = self.config["model"]["loss"],
                optimizer = self.config["model"]["optimizer"],
                metrics = self.config["model"]["metrics"]
            )
            logging.info("Model created succesfully....")
            return model
        except Exception as e:
            logging.error(f"Error occurfed during model architecture {e}")
            raise CustomException("Failed to create model",e)



