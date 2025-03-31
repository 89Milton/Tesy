import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

# Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:5000/callback'

# Spotify scopes we need
SCOPES = [
    'user-read-private',
    'user-read-email',
    'user-top-read',
    'user-read-recently-played',
    'user-read-currently-playing'
]

def create_spotify_oauth():
    """Create Spotify OAuth object"""
    return SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=' '.join(SCOPES),
        cache_path=None  # We'll handle token caching ourselves
    )

def get_user_top_tracks(sp, limit=10):
    """Get user's top tracks"""
    try:
        results = sp.current_user_top_tracks(limit=limit, time_range='medium_term')
        return results['items']
    except Exception as e:
        print(f"Error getting top tracks: {e}")
        return []

def get_track_audio_features(sp, track_ids):
    """Get audio features for multiple tracks"""
    try:
        features = sp.audio_features(track_ids)
        return features
    except Exception as e:
        print(f"Error getting audio features: {e}")
        return []

def analyze_music_taste(tracks, features):
    """Analyze music taste based on tracks and their audio features"""
    if not tracks or not features:
        return None

    # Calculate average audio features
    avg_features = {
        'danceability': 0,
        'energy': 0,
        'valence': 0,
        'acousticness': 0,
        'instrumentalness': 0
    }

    for feature in features:
        if feature:  # Some features might be None
            for key in avg_features:
                avg_features[key] += feature.get(key, 0)

    # Calculate averages
    num_features = len(features)
    for key in avg_features:
        avg_features[key] /= num_features

    return {
        'tracks': tracks,
        'features': avg_features
    } 