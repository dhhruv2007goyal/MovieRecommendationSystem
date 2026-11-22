import os
from pathlib import Path

import joblib
import pandas as pd
import requests
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
MOVIES_PATH = BASE_DIR / "movies.pkl"
SIMILARITY_PATH = BASE_DIR / "similarity_compressed.pkl"
PLACEHOLDER_POSTER = "https://placehold.co/300x450?text=Poster+unavailable"

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(rgba(10, 12, 18, .94), rgba(10, 12, 18, .96)),
        url("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=1600");
        background-size: cover;
        background-attachment: fixed;
    }
    h1 { color: #ff6262; text-align: center; }
    .subtitle { text-align: center; color: #d0d0d0; margin-bottom: 1.5rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def load_movies():
    return pd.read_pickle(MOVIES_PATH)


@st.cache_resource(show_spinner="Loading recommendation model…")
def load_similarity():
    return joblib.load(SIMILARITY_PATH)


def fetch_poster(movie_name: str) -> str:
    """Fetch a poster from OMDb when OMDB_API_KEY is configured."""
    api_key = os.getenv("OMDB_API_KEY")
    if not api_key:
        return PLACEHOLDER_POSTER
    try:
        response = requests.get(
            "https://www.omdbapi.com/",
            params={"t": movie_name, "apikey": api_key},
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()
        poster = data.get("Poster")
        if data.get("Response") == "True" and poster and poster != "N/A":
            return poster
    except (requests.RequestException, ValueError):
        pass
    return PLACEHOLDER_POSTER


def recommend(movie_name: str, movies: pd.DataFrame, similarity, count: int = 5):
    matches = movies.index[movies["original_title"] == movie_name]
    if len(matches) == 0:
        return []
    movie_index = int(matches[0])
    scores = similarity[movie_index]
    ranked_indices = sorted(
        enumerate(scores), key=lambda item: item[1], reverse=True
    )
    # Exclude the selected movie itself.
    return [movies.iloc[index]["original_title"] for index, _ in ranked_indices
            if index != movie_index][:count]


st.title("🎬 Movie Recommender")
st.markdown('<p class="subtitle">Choose a movie and discover five similar films.</p>', unsafe_allow_html=True)

try:
    movies = load_movies()
    similarity = load_similarity()
except Exception as exc:
    st.error("The saved model files could not be loaded. Make sure both .pkl files are beside app.py.")
    st.exception(exc)
    st.stop()

if similarity.shape[0] != len(movies) or similarity.shape[1] != len(movies):
    st.error("The movie data and similarity matrix do not match. Use the model files supplied together.")
    st.stop()

movie_names = movies["original_title"].dropna().tolist()
selected_movie = st.selectbox("Select a movie", movie_names)

if st.button("Recommend movies", type="primary", use_container_width=True):
    with st.spinner("Finding similar movies…"):
        recommendations = recommend(selected_movie, movies, similarity)
        if not recommendations:
            st.warning("No recommendations were found for this selection.")
        else:
            columns = st.columns(len(recommendations))
            for column, title in zip(columns, recommendations):
                with column:
                    st.image(fetch_poster(title), use_container_width=True)
                    st.markdown(f"**{title}**")

if not os.getenv("OMDB_API_KEY"):
    st.caption("Poster images are optional. Set an OMDB_API_KEY environment variable to load real posters; recommendations work without it.")
