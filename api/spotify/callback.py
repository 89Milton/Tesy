from http.server import BaseHTTPRequestHandler
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from urllib.parse import parse_qs, urlparse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Get query parameters
        query_components = parse_qs(urlparse(self.path).query)
        code = query_components.get('code', [None])[0]

        if not code:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(str('{"error": "No code provided"}').encode())
            return

        # Get Spotify credentials
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        
        # Use the production URL if available, otherwise use localhost
        base_url = os.getenv('VERCEL_URL', 'http://localhost:3000')
        if base_url.startswith('http'):
            redirect_uri = f"{base_url}/api/spotify/callback"
        else:
            redirect_uri = f"https://{base_url}/api/spotify/callback"

        # Create Spotify OAuth object
        sp_oauth = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope='user-read-private user-read-email user-top-read user-read-recently-played user-read-currently-playing',
            cache_path=None
        )

        try:
            # Get access token
            token_info = sp_oauth.get_access_token(code)
            
            # Create Spotify client
            sp = spotipy.Spotify(auth=token_info['access_token'])
            
            # Get user's top tracks
            results = sp.current_user_top_tracks(limit=10, time_range='medium_term')
            tracks = results['items']

            # Get audio features for tracks
            track_ids = [track['id'] for track in tracks]
            features = sp.audio_features(track_ids)

            # Prepare response
            response = {
                'tracks': tracks,
                'features': features
            }

            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(str(response).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(str(f'{{"error": "{str(e)}"}}').encode()) 