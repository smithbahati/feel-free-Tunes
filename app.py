import streamlit as st
from spotify_integration import authenticate_spotify, get_tracks_by_mood, create_playlist
import streamlit.components.v1 as components

# Set page config
st.set_page_config(
    page_title="FeelFreeTunes",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'selected_mood' not in st.session_state:
    st.session_state.selected_mood = None
if 'view' not in st.session_state:
    st.session_state.view = "mood_selection"
if 'tracks' not in st.session_state:
    st.session_state.tracks = []
if 'current_track' not in st.session_state:
    st.session_state.current_track = None
if 'playlist_url' not in st.session_state:
    st.session_state.playlist_url = None
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True  # Default to dark mode

# Initialize Spotify
sp = authenticate_spotify()

# Theme toggle function
def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

# Load CSS based on current theme
def load_css():
    theme = "dark" if st.session_state.dark_mode else "light"
    with open(f"styles-{theme}.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# App header with theme toggle
header_col1, header_col2 = st.columns([5, 1])
with header_col1:
    st.markdown("""
    <div class="app-header">
        <div class="app-title">FeelFreeTunes</div>
        <div class="app-subtitle">Music that matches your mood</div>
    </div>
    """, unsafe_allow_html=True)
with header_col2:
    theme_icon = "🌙" if st.session_state.dark_mode else "☀️"
    if st.button(theme_icon, key="theme_toggle"):
        toggle_theme()
        st.rerun()

# Mood Selection View
if st.session_state.view == "mood_selection":
    st.markdown("### Select Your Mood")
    
    cols = st.columns(4)
    moods = ["Happy", "Sad", "Energetic", "Relaxed", "Melancholic", "Romantic", "Nostalgic", "Focused"]
    
    for i, mood in enumerate(moods):
        with cols[i % 4]:
            if st.button(f"{mood}", key=f"mood_{mood}", use_container_width=True):
                st.session_state.selected_mood = mood
                st.session_state.view = "search_results"
                with st.spinner(f"Finding {mood} songs..."):
                    st.session_state.tracks = get_tracks_by_mood(sp, mood)
                    if st.session_state.tracks:
                        st.session_state.playlist_url = create_playlist(
                            sp, 
                            sp.me()['id'], 
                            st.session_state.selected_mood, 
                            st.session_state.tracks
                        )
                st.rerun()

# Search Results View
elif st.session_state.view == "search_results":
    if st.button("← Back to Mood Selection"):
        st.session_state.view = "mood_selection"
        st.rerun()
    
    st.markdown(f"""
    <div class="search-header">
        <div class="results-title">Results for {st.session_state.selected_mood}</div>
        <div class="results-count">{len(st.session_state.tracks)} tracks</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.tracks:
        # Upper row
        cols = st.columns(5)
        for i, track in enumerate(st.session_state.tracks[:5]):
            with cols[i]:
                st.markdown(f"""
                <div class="track-card">
                    <img src="{track['image']}" class="album-cover" alt="Album cover">
                    <div class="track-info">
                        <div class="track-name" title="{track['name']}">{track['name'][:20]}{'...' if len(track['name']) > 20 else ''}</div>
                        <div class="track-artist">{track['artist'][:20]}{'...' if len(track['artist']) > 20 else ''}</div>
                    </div>
                    <a href="{track['url']}" target="_blank" class="play-link">
                        <button class="play-button">Play</button>
                    </a>
                </div>
                """, unsafe_allow_html=True)
        
        # Middle row
        cols = st.columns(5)
        for i, track in enumerate(st.session_state.tracks[5:10]):
            with cols[i]:
                st.markdown(f"""
                <div class="track-card">
                    <img src="{track['image']}" class="album-cover" alt="Album cover">
                    <div class="track-info">
                        <div class="track-name" title="{track['name']}">{track['name'][:20]}{'...' if len(track['name']) > 20 else ''}</div>
                        <div class="track-artist">{track['artist'][:20]}{'...' if len(track['artist']) > 20 else ''}</div>
                    </div>
                    <a href="{track['url']}" target="_blank" class="play-link">
                        <button class="play-button">Play</button>
                    </a>
                </div>
                """, unsafe_allow_html=True)
        
        # Lower row
        if len(st.session_state.tracks) > 10:
            cols = st.columns(5)
            for i, track in enumerate(st.session_state.tracks[10:15]):
                with cols[i]:
                    st.markdown(f"""
                    <div class="track-card">
                        <img src="{track['image']}" class="album-cover" alt="Album cover">
                        <div class="track-info">
                            <div class="track-name" title="{track['name']}">{track['name'][:20]}{'...' if len(track['name']) > 20 else ''}</div>
                            <div class="track-artist">{track['artist'][:20]}{'...' if len(track['artist']) > 20 else ''}</div>
                        </div>
                        <a href="{track['url']}" target="_blank" class="play-link">
                            <button class="play-button">Play</button>
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Now playing section
    if st.session_state.playlist_url:
        st.markdown(f"""
        <div class="now-playing">
            <div class="now-playing-info">
                <div class="now-playing-title">{st.session_state.selected_mood} Playlist</div>
                <div class="now-playing-artist">Various Artists</div>
            </div>
            <div class="now-playing-actions">
                <a href="{st.session_state.playlist_url}" target="_blank" class="now-playing-link">
                    <button class="now-playing-button">Playlist</button>
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)