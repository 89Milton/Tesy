from http.server import BaseHTTPRequestHandler
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from urllib.parse import urlencode

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Get Spotify credentials from environment variables
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

        # Generate authorization URL
        auth_url = sp_oauth.get_authorize_url()

        # Redirect to Spotify login
        self.send_response(302)
        self.send_header('Location', auth_url)
        self.end_headers() 