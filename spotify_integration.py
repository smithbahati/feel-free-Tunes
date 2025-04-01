import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st

def authenticate_spotify():
    """Authenticate with Spotify using credentials from environment variables"""
    try:
        return spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID", st.secrets.get("SPOTIPY_CLIENT_ID")),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET", st.secrets.get("SPOTIPY_CLIENT_SECRET")),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI", st.secrets.get("SPOTIPY_REDIRECT_URI")),
            scope="playlist-modify-public user-read-private"
        ))
    except Exception as e:
        st.error(f"Spotify authentication failed: {str(e)}")
        return None

def get_tracks_by_mood(sp, mood, limit=15):
    """Get tracks based on mood with enhanced error handling"""
    mood_genres = {
        "Happy": ["pop", "happy"],
        "Sad": ["acoustic", "sad"],
        "Energetic": ["electronic", "work-out"],
        "Relaxed": ["jazz", "chill"],
        "Melancholic": ["indie", "sad"],
        "Romantic": ["r&b", "romance"],
        "Nostalgic": ["indie", "oldies"],
        "Focused": ["instrumental", "classical"]
    }
    
    if mood not in mood_genres:
        st.warning(f"Unsupported mood: {mood}")
        return []

    try:
        # Search with multiple genre keywords for better results
        query = f"genre:{' OR genre:'.join(mood_genres[mood])}"
        results = sp.search(q=query, type="track", limit=limit)
        
        tracks = []
        for track in results["tracks"]["items"]:
            try:
                tracks.append({
                    "name": track["name"],
                    "artist": track["artists"][0]["name"],
                    "url": track["external_urls"]["spotify"],
                    "image": track["album"]["images"][0]["url"] if track["album"]["images"] else None,
                    "uri": track["uri"]
                })
            except (KeyError, IndexError) as e:
                continue  # Skip malformed track entries
        
        return tracks

    except Exception as e:
        st.error(f"Error fetching tracks: {str(e)}")
        return []

def create_playlist(sp, user_id, mood, tracks):
    """Create playlist with improved metadata and error handling"""
    if not tracks:
        st.warning("No tracks to add to playlist")
        return None

    try:
        # Get current user info for playlist naming
        user_info = sp.current_user()
        display_name = user_info.get("display_name", "Your")
        
        playlist = sp.user_playlist_create(
            user=user_id,
            name=f"{mood} Mood Mix for {display_name}",
            public=True,
            description=f"Automatically generated {mood.lower()} mood playlist created with Streamlit"
        )
        
        # Add tracks in batches to avoid API limits
        track_uris = [track['uri'] for track in tracks]
        for i in range(0, len(track_uris), 100):  # Spotify allows max 100 tracks per request
            batch = track_uris[i:i+100]
            sp.playlist_add_items(playlist['id'], batch)
        
        return playlist['external_urls']['spotify']

    except Exception as e:
        st.error(f"Error creating playlist: {str(e)}")
        return None
