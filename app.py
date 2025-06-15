import streamlit as st
import pandas as pd
import requests
import pickle


try:
    with open('movie_data.pkl', 'rb') as file:
        movies, cosine_sim = pickle.load(file)
except Exception as e:
    st.error(f"Error loading movie_data.pkl: {e}")
    st.stop()

def get_recommendations(title, cosine_sim=cosine_sim):
    title = title.strip().lower()
    if title not in movies['title'].str.lower().values:
        return f"Movie '{title}' not found."

    idx = movies[movies['title'].str.lower() == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return movies[['title', 'movie_id']].iloc[movie_indices]

def fetch_poster(movie_id):
    api_key = '2f87bd6f1bbb899c438f06f1af6725f9'  # Replace with your TMDB API key
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
        return full_path
    else:
        return None

st.title("Movie Recommendation System")

selected_movie = st.selectbox("Select a movie:", movies['title'].values)

if st.button('Recommend'):
    recommendations = get_recommendations(selected_movie)
    if isinstance(recommendations, str):
        st.write(recommendations)  # show error message if movie not found
    else:
        st.write("Top 10 recommended movies:")

        for i in range(0, 10, 5):  # Loop over rows (2 rows, 5 movies each)
            cols = st.columns(5)  # Create 5 columns for each row
            for col, j in zip(cols, range(i, i+5)):
                if j < len(recommendations):
                    movie_title = recommendations.iloc[j]['title']
                    movie_id = recommendations.iloc[j]['movie_id']
                    poster_url = fetch_poster(movie_id)
                    with col:
                        if poster_url:
                            st.image(poster_url, width=130)
                        else:
                            st.write("No Image")
                        st.write(movie_title)
