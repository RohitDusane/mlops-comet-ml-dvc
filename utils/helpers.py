import pandas as pd
import numpy as np
import joblib

from config.path_config import *
from src.logger import logging
from src.exception import CustomException

############ 1. GET ANIME FRAME ############

def getAnimeFrame(anime, path_anime_df):
    anime_df = pd.read_csv(path_anime_df)
    if isinstance(anime, int):
        # Check if anime_id exists in the DataFrame
        result = anime_df[anime_df.anime_id == anime]
    elif isinstance(anime, str):
        # Check if anime name exists in the DataFrame
        result = anime_df[anime_df.eng_version == anime]
    else:
        raise ValueError("Invalid anime type. Expected int (anime_id) or str (anime name).")

    # Check if the DataFrame is empty
    if result.empty:
        logging.warning(f"No matching anime found for '{anime}' in the DataFrame.")
        return result  # Return empty DataFrame to handle downstream gracefully
    
    return result

    
############ 2. GET SYNOPSIS ############

# retunr Synopsis for anime_id or Anime_name
def getSynopsis(anime,path_synopsis_df):
    synopsis_df = pd.read_csv(path_synopsis_df)
    if isinstance(anime,int):
        return synopsis_df[synopsis_df.MAL_ID == anime].sypnopsis.values[0]
    if isinstance(anime, str):
        return synopsis_df[synopsis_df.Name == anime].sypnopsis.values[0]
    

############ 3. CONTENT RECOMMEDATION ############
def find_similar_animes(name, 
                        path_anime_weights,
                        path_anime2anime_encoded,
                        path_anime2anime_decoded,
                        path_anime_df,
                        path_synopsis_df,
                        n=10,
                        return_dist=False, 
                        neg=False):
    try:
        # Read the files
        anime_weights = joblib.load(path_anime_weights)
        anime2anime_encoded = joblib.load(path_anime2anime_encoded)
        anime2anime_decoded = joblib.load(path_anime2anime_decoded)

        # Get the index of the anime based on its name
        anime_frame = getAnimeFrame(name, path_anime_df)
        
        # Check if the anime frame is empty
        if anime_frame.empty:
            raise ValueError(f"Anime '{name}' not found in the dataset.")

        index = anime_frame.anime_id.values[0]  # Get anime ID
        encoded_index = anime2anime_encoded.get(index)  # Get encoded index

        if encoded_index is None:
            raise ValueError(f"Encoded index for anime '{name}' not found.")

        # Get the embeddings (weights)
        weights = anime_weights

        # Compute the similarity (dot product between weights)
        dists = np.dot(weights, weights[encoded_index])  # Compute the cosine similarity
        sorted_dists = np.argsort(dists)  # Sort distances (ascending)

        n = n + 1  # To exclude the query anime itself from results

        if neg:
            closest = sorted_dists[:n]  # Return the farthest anime
        else:
            closest = sorted_dists[-n:]  # Return the closest anime

        logging.info(f"Anime closest to {name}:")

        if return_dist:
            return dists, closest

        SimilarityArr = []

        # Loop through the closest anime and gather metadata
        for close in closest:
            decoded_id = anime2anime_decoded.get(close)

            if decoded_id is None:
                continue  # Skip if no valid decoded ID

            # Fetch metadata for each similar anime
            anime_frame = getAnimeFrame(decoded_id, path_anime_df)
            if anime_frame.empty:
                continue  # Skip if no data for this anime
            
            anime_name = anime_frame.eng_version.values[0]
            genre = anime_frame.Genres.values[0]
            synopsis = getSynopsis(decoded_id, path_synopsis_df)
            similarity = dists[close]

            SimilarityArr.append({
                'anime_id': decoded_id,
                'name': anime_name,
                'similarity': similarity,
                'genre': genre,
                'synopsis': synopsis
            })

        # Create a DataFrame with results and sort by similarity
        Frame = pd.DataFrame(SimilarityArr).sort_values(by='similarity', ascending=False)
        # Exclude the original anime and drop the 'anime_id' column
        return Frame[Frame.anime_id != index].drop(['anime_id'], axis=1)

    except Exception as e:
        logging.error(f"Error: {e}")
        return None



############ 4. FIND SIMILAR USERS ############
def find_similar_users(item_input , path_user_weights , 
                       path_user2user_encoded , path_user2user_decoded, 
                       n=10 , return_dist=False,neg=False):
    try:
        # Load files
        user_weights = joblib.load(path_user_weights)
        user2user_decoded = joblib.load(path_user2user_decoded)
        user2user_encoded = joblib.load(path_user2user_encoded)
        index=item_input
        encoded_index = user2user_encoded.get(index)

        weights = user_weights

        dists = np.dot(weights,weights[encoded_index])
        sorted_dists = np.argsort(dists)

        n=n+1

        if neg:
            closest = sorted_dists[:n]
        else:
            closest = sorted_dists[-n:]
            

        if return_dist:
            return dists,closest
        
        SimilarityArr = []

        for close in closest:
            similarity = dists[close]

            if isinstance(item_input,int):
                decoded_id = user2user_decoded.get(close)
                SimilarityArr.append({
                    "similar_users" : decoded_id,
                    "similarity" : similarity
                })
        similar_users = pd.DataFrame(SimilarityArr).sort_values(by="similarity",ascending=False)
        similar_users = similar_users[similar_users.similar_users != item_input]
        return similar_users
    except Exception as e:
        print("Error Occured",e)

        
############ 5. USERS PREFERENCES ############
def get_user_preferences(user_id , path_rating_df , path_anime_df ,plot=False):

    rating_df = pd.read_csv(path_rating_df)
    anime_df =pd.read_csv(path_anime_df)

    animes_watched_by_user = rating_df[rating_df.user_id == user_id]

    user_rating_percentile = np.percentile(animes_watched_by_user.rating , 75)

    animes_watched_by_user = animes_watched_by_user[animes_watched_by_user.rating >= user_rating_percentile]

    top_animes_user = (
        animes_watched_by_user.sort_values(by="rating" , ascending=False).anime_id.values
    )

    anime_df_rows = anime_df[anime_df["anime_id"].isin(top_animes_user)]
    anime_df_rows = anime_df_rows[["eng_version","Genres"]]

    return anime_df_rows

############ 6. GET USERS RECCOMENDATION ############
def get_user_recommendations(similar_users , user_pref ,
                             path_anime_df , path_synopsis_df, path_rating_df, n=10):
    
    # anime_df = pd.read_csv(path_anime_df)
    # synopsis_df = pd.read_csv(path_synopsis_df)
    # rating_df = pd.read_csv(path_rating_df)

    recommended_animes = []
    anime_list = []

    for user_id in similar_users.similar_users.values:
        pref_list = get_user_preferences(int(user_id) , path_rating_df, path_anime_df)

        pref_list = pref_list[~pref_list.eng_version.isin(user_pref.eng_version.values)]

        if not pref_list.empty:
            anime_list.append(pref_list.eng_version.values)

    if anime_list:
            anime_list = pd.DataFrame(anime_list)

            sorted_list = pd.DataFrame(pd.Series(anime_list.values.ravel()).value_counts()).head(n)

            for i,anime_name in enumerate(sorted_list.index):
                n_user_pref = sorted_list[sorted_list.index == anime_name].values[0][0]

                if isinstance(anime_name,str):
                    frame = getAnimeFrame(anime_name,path_anime_df)
                    anime_id = frame.anime_id.values[0]
                    genre = frame.Genres.values[0]
                    synopsis = getSynopsis(int(anime_id),path_synopsis_df)

                    recommended_animes.append({
                        "n" : n_user_pref,
                        "anime_name" : anime_name,
                        "Genres" : genre,
                        "Synopsis": synopsis
                    })
    return pd.DataFrame(recommended_animes).head(n)


