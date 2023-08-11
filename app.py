import pandas as pd
import streamlit as st
import pickle
import requests


# Function to get the poster URL for a given movie_id
def fetch_poster(id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        id)
    data1 = requests.get(url)
    data = data1.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similar[index])), reverse=True, key=lambda x: x[1])
    movie_names = []
    movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        id = movies.iloc[i[0]].id
        movie_posters.append(fetch_poster(id))
        movie_names.append(movies.iloc[i[0]].title)

    return movie_names, movie_posters


# Setting the page configuration
st.set_page_config(
    page_title="Movie Recommender System",
    layout="wide"
)

# Applying custom styling
st.markdown(
        """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Forte&display=swap');
    
    .header-style {
        font-family: 'Forte', cursive;
        font-size: 36px;
        text-align: center;
        padding: 20px 0;
        background-color: #3498db;
        color: white;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .dropdown-style {
        font-family: 'Forte', cursive;
        font-size: 18px;
        color: #333;
    }
    .recommend-button {
        background-color: #27ae60;
        color: white;
        font-size: 16px;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .recommend-button:hover {
        background-color: #219653;
    }
    .movie-title {
        font-size: 20px;
        font-weight: bold;
        margin-top: 15px;
    }
    .movie-poster {
        max-width: 150px;
        border-radius: 5px;
        margin-top: 10px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    }
    
    @media (max-width: 600px) {
        .header-style {
            font-size: 28px;
            padding: 15px 0;
            margin-bottom: 15px;
        }
        .dropdown-style {
            font-size: 16px;
        }
        .movie-title {
            font-size: 18px;
            margin-top: 10px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Displaying the centered header
st.markdown('<p class="header-style">Movie Recommender System</p>', unsafe_allow_html=True)
new_data = pickle.load(open('movies_list.pkl', 'rb'))
movies = pd.DataFrame(new_data)
similar = pickle.load(open('similar.pkl', 'rb'))

movies_list = new_data['title'].values
select_movies = st.selectbox(
    " Type or select a movie from the dropdown menu !!!",
    movies_list
)

if st.button('Show Recommendation'):
    movie_names, movie_posters = recommend(select_movies)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(movie_names[0])
        st.image(movie_posters[0])
    with col2:
        st.text(movie_names[1])
        st.image(movie_posters[1])

    with col3:
        st.text(movie_names[2])
        st.image(movie_posters[2])
    with col4:
        st.text(movie_names[3])
        st.image(movie_posters[3])
    with col5:
        st.text(movie_names[4])
        st.image(movie_posters[4])
