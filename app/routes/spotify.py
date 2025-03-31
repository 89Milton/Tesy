from flask import Blueprint, redirect, request, session, url_for, jsonify
import spotipy
from app.utils.spotify import create_spotify_oauth, get_user_top_tracks, get_track_audio_features, analyze_music_taste

spotify_bp = Blueprint('spotify', __name__)

@spotify_bp.route('/login')
def login():
    """Redirect to Spotify login page"""
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@spotify_bp.route('/callback')
def callback():
    """Handle Spotify callback"""
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)

    if not token_info:
        return redirect(url_for('index'))

    session['token_info'] = token_info
    return redirect(url_for('index'))

@spotify_bp.route('/logout')
def logout():
    """Logout from Spotify"""
    session.clear()
    return redirect(url_for('index'))

@spotify_bp.route('/get-user-taste')
def get_user_taste():
    """Get user's music taste analysis"""
    if 'token_info' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    token_info = session['token_info']
    sp = spotipy.Spotify(auth=token_info['access_token'])

    # Get user's top tracks
    tracks = get_user_top_tracks(sp)
    if not tracks:
        return jsonify({'error': 'No tracks found'}), 404

    # Get track IDs
    track_ids = [track['id'] for track in tracks]

    # Get audio features
    features = get_track_audio_features(sp, track_ids)

    # Analyze music taste
    analysis = analyze_music_taste(tracks, features)
    if not analysis:
        return jsonify({'error': 'Could not analyze music taste'}), 500

    return jsonify(analysis) 