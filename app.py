import pickle
import streamlit as st
import requests
import bz2
import random

# Customizing Streamlit App
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Functions
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id
    )
    data = requests.get(url)
    data = data.json()
    poster_path = data["poster_path"]
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def fetch_movie_details(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id
    )
    data = requests.get(url)
    return data.json()

def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1]
    )
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

def display_movie_details(movie_name):
    movie_index = movies[movies["title"] == movie_name].index[0]
    movie_details = fetch_movie_details(movies.iloc[movie_index].movie_id)
    st.write(f"## {movie_name}")
    st.write(f"**Release Date:** {movie_details['release_date']}")
    st.write(f"**Overview:** {movie_details['overview']}")
    st.write(f"**Rating:** {movie_details['vote_average']}")

# Header
st.title("Movie Recommender System")

# Load Data
movies = pickle.load(open("movie_list.pkl", "rb"))
ifile = bz2.BZ2File("similarity.pkl", "rb")
similarity = pickle.load(ifile)
ifile.close()

# Sidebar
# You can add more sidebar content here if needed.

# Main Content
st.markdown("### Select a movie from drop down")
selected_movie = st.selectbox("Choose a Movie", movies["title"].values)

if st.button("Show Recommendation"):
    if selected_movie:
        selected_movie_id = movies[movies["title"] == selected_movie][
            "movie_id"
        ].values[0]
        recommended_movie_names, recommended_movie_posters = recommend(
            selected_movie
        )
        col1, col2, col3, col4, col5 = st.columns(5)
        for i in range(5):
            with st.container():
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])
                display_movie_details(recommended_movie_names[i])

        # Display similarity score
        st.write("### Similarity Score")
        selected_movie_index = movies[movies["title"] == selected_movie].index[0]
        selected_movie_similarity = similarity[selected_movie_index]
        st.bar_chart(selected_movie_similarity)
    else:
        st.warning("Please select a movie before clicking 'Show Recommendation'")

# Random movie generator
if st.button("Get Random Movie"):
    random_movie = random.choice(movies["title"].values)
    st.write(f"Random Movie: {random_movie}")
