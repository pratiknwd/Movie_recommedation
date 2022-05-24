import streamlit as st
import pickle
import  pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=84a94f778e9e7290fa8341caf5b4c3a9&language=en-US'.format(     movie_id))
    data = response.json()
    # st.text(data)
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0] # here index zero bcz we have to find out zero matrix in similarity for given movie
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True, key=lambda x:x[1])[1:13]
    recommended_movies=[]
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters



similarity = pickle.load(open('similarity.pkl','rb'))

'For the layout for the webpage'
movies_dict =  pickle.load(open("movie_dict.pkl","rb"))
movies = pd.DataFrame(movies_dict)
st.container()
st.title('Movie Recomender System')

# lst = ((movies["title"].values))

# lst2 = [lst.title() for lst in lst] # for captilasing the first letter

selected_movie_name = st.selectbox(
'Please Choose Your Movie Here',
((movies["title"].values)))

session = requests.Session()
session.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.1.2222.33 Safari/537.36",
    "Accept-Encoding": "*",
    "Connection": "keep-alive"
}


if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)

    col1,col2,col3,col4 = st.columns(4)
    with col1:
         st.text(names[0])
         st.image(posters[0])
    with col2:
         st.text(names[1])
         st.image(posters[1])
    with col3:
         st.text(names[2])
         st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    col5, col6, col7,col8 = st.columns(4)
    with col5:
        st.text(names[4])
        st.image(posters[4])

    with col6:
         st.text(names[5])
         st.image(posters[5])

    with col7:
        st.text(names[6])
        st.image(posters[6])

    with col8:
        st.text(names[7])
        st.image(posters[7])

    col9, col10, col11, col12 = st.columns(4)

    with col9:
        st.text(names[8])
        st.image(posters[8])

    with col10:
        st.text(names[9])
        st.image(posters[9])
    with col11:
        st.text(names[10])
        st.image(posters[10])

    with col12:
        st.text(names[11])
        st.image(posters[11])


