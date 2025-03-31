import spotipy
from spotipy.oauth2 import SpotifyOAuth

def authenticate_spotify():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id="52c56ae18ac346a3868bdb537c313f53",
        client_secret="a5df4992dcd34222b17cff6151d47510",
        redirect_uri="http://127.0.0.1:8888",
        scope="playlist-modify-public user-read-private"
    ))

def get_tracks_by_mood(sp, mood, limit=15):
    mood_genres = {
        "Happy": "pop",
        "Sad": "acoustic",
        "Energetic": "electronic",
        "Relaxed": "jazz",
        "Melancholic": "indie",
        "Romantic": "r&b",
        "Nostalgic": "indie",
        "Focused": "instrumental"
    }
    
    try:
        results = sp.search(q=f"genre:{mood_genres[mood]}", type="track", limit=limit)
        return [{
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "url": track["external_urls"]["spotify"],
            "image": track["album"]["images"][0]["url"] if track["album"]["images"] else None,
            "uri": track["uri"]
        } for track in results["tracks"]["items"]]
    except Exception as e:
        print(f"Error fetching tracks: {e}")
        return []

def create_playlist(sp, user_id, mood, tracks):
    try:
        playlist = sp.user_playlist_create(
            user=user_id,
            name=f"{mood} Mood Playlist",
            public=True,
            description=f"Automatically generated {mood} mood playlist"
        )
        
        track_uris = [track['uri'] for track in tracks]
        sp.playlist_add_items(playlist['id'], track_uris)
        
        return playlist['external_urls']['spotify']
    except Exception as e:
        print(f"Error creating playlist: {e}")
        return None