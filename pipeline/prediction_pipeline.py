import logging
from collections import defaultdict
from config.path_config import *
from utils.helpers import *

# Set up logging
logging.basicConfig(level=logging.INFO)

def hybrid_recommendation(user_id, user_weight=0.5, content_weight=0.5):
    try:
        # --- User Recommendation ---
        similar_users = find_similar_users(user_id, USER_WEIGHTS_PATH, USER2USER_ENCODED, USER2USER_DECODED)
        user_pref = get_user_preferences(user_id, RATING_DF, ANIME_DF)
        user_recommended_animes = get_user_recommendations(similar_users, user_pref, ANIME_DF, SYNOPISIS_DF, RATING_DF)
        
        user_recommended_anime_list = user_recommended_animes["anime_name"].tolist()
        logging.info(f"User-based recommended animes: {user_recommended_anime_list}")
        
        # --- Content-Based Recommendation ---
        content_recommended_animes = set()  # Using a set to avoid duplicates
        
        for anime in user_recommended_anime_list:
            similar_animes = find_similar_animes(anime, ANIME_WEIGHTS_PATH, ANIME2ANIME_ENCODED, ANIME2ANIME_DECODED, ANIME_DF, SYNOPISIS_DF)
            
            if similar_animes is not None and not similar_animes.empty:
                content_recommended_animes.update(similar_animes["name"].tolist())  # Use update() to add unique items
            else:
                logging.warning(f"No similar anime found for {anime}")
        
        # --- Combine Scores ---
        combined_scores = defaultdict(float)  # Default to 0 for any anime

        # Add user-based scores
        for anime in user_recommended_anime_list:
            combined_scores[anime] += user_weight

        # Add content-based scores
        for anime in content_recommended_animes:
            combined_scores[anime] += content_weight

        # Sort by combined score in descending order and return top 10
        sorted_animes = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Return top 10 anime recommendations
        top_recommendations = [anime for anime, score in sorted_animes[:10]]
        logging.info(f"Top 10 recommendations: {top_recommendations}")
        
        return top_recommendations
    
    except Exception as e:
        logging.error(f"An error occurred during the recommendation process: {str(e)}")
        return []

