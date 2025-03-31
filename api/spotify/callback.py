from http.server import BaseHTTPRequestHandler
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from urllib.parse import parse_qs, urlparse, quote

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Get query parameters
            query_components = parse_qs(urlparse(self.path).query)
            code = query_components.get('code', [None])[0]

            if not code:
                raise ValueError("No code provided")

            # Get Spotify credentials
            client_id = os.getenv('SPOTIFY_CLIENT_ID')
            client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
            
            if not client_id or not client_secret:
                raise ValueError("Missing Spotify credentials")
            
            # Use custom domain if available, otherwise fallback to Vercel URL
            base_url = os.getenv('CUSTOM_DOMAIN', os.getenv('VERCEL_URL', 'http://localhost:3000'))
            if base_url.startswith('http'):
                redirect_uri = f"{base_url}/api/spotify/callback"
            else:
                redirect_uri = f"https://{base_url}/api/spotify/callback"

            # Log the redirect URI for debugging
            print(f"Using redirect URI: {redirect_uri}")

            # Create Spotify OAuth object
            sp_oauth = SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope='user-read-private user-read-email user-top-read user-read-recently-played user-read-currently-playing',
                cache_path=None
            )

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

            # Redirect to frontend with data
            frontend_url = f"{base_url}/api/templates/index.html"
            encoded_data = quote(str(response))
            redirect_url = f"{frontend_url}?data={encoded_data}"

            self.send_response(302)
            self.send_header('Location', redirect_url)
            self.end_headers()

        except Exception as e:
            print(f"Error in callback handler: {str(e)}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_message = f'{{"error": "Callback failed: {str(e)}"}}'
            self.wfile.write(error_message.encode()) 