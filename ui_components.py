# ui_components.py
import streamlit as st
from utils import MOOD_OPTIONS
import streamlit.components.v1 as components

def show_mood_selection():
    """Display mood selection cards in a responsive grid"""
    st.markdown("""
    <style>
        .mood-selection-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            color: var(--text-primary);
        }
    </style>
    <div class="mood-selection-title">How are you feeling today?</div>
    """, unsafe_allow_html=True)
    
    # Add JavaScript for mood selection
    components.html("""
    <script>
    function selectMood(mood) {
        window.parent.postMessage({
            type: 'selectMood',
            data: mood
        }, '*');
    }
    </script>
    """, height=0)
    
    # Create mood cards in a responsive grid
    cols = st.columns(4)
    mood_keys = list(MOOD_OPTIONS.keys())
    
    for i, mood in enumerate(mood_keys):
        with cols[i % 4]:
            emoji = MOOD_OPTIONS[mood]["emoji"]
            selected = st.session_state.selected_mood == mood
            selected_class = "selected" if selected else ""
            
            st.markdown(f"""
            <div class="mood-card {selected_class}" onclick="selectMood('{mood}')">
                <div class="mood-emoji">{emoji}</div>
                <div class="mood-name">{mood}</div>
            </div>
            """, unsafe_allow_html=True)

def show_search_results(tracks):
    """Display track recommendations in a responsive grid"""
    if not tracks:
        st.warning("No tracks found for this mood.")
        return
    
    st.markdown("""
    <style>
        .results-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }
        .results-title {
            font-size: 1.5rem;
            font-weight: 600;
        }
        .results-count {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }
    </style>
    <div class="results-header">
        <div class="results-title">Recommended Tracks</div>
        <div class="results-count">{len(tracks)} songs</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display tracks in responsive grid
    st.markdown('<div class="track-grid">', unsafe_allow_html=True)
    for track in tracks:
        st.markdown(f"""
        <div class="track-card">
            <img src="{track['image']}" class="album-cover" alt="Album cover">
            <div class="track-info">
                <div class="track-name" title="{track['name']}">{track['name'][:20]}{'...' if len(track['name']) > 20 else ''}</div>
                <div class="track-artist">{track['artist'][:20]}{'...' if len(track['artist']) > 20 else ''}</div>
            </div>
            <a href="{track['url']}" target="_blank">
                <button class="play-button">Play</button>
            </a>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Now playing section
    if st.session_state.get('current_track'):
        track = st.session_state.current_track
        st.markdown(f"""
        <div class="now-playing">
            <img src="{track['image']}" class="now-playing-cover" alt="Now playing">
            <div class="now-playing-info">
                <div class="now-playing-title">{track['name'][:25]}{'...' if len(track['name']) > 25 else ''}</div>
                <div class="now-playing-artist">{track['artist'][:25]}{'...' if len(track['artist']) > 25 else ''}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)