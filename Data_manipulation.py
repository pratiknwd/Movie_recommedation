import numpy as np
import pandas as pd
import ast
"""To permanently import a csv file in pycharm 
step 1 = paste file path """
# movies = pd.read_csv(r"C:\Users\Pratik Raj\PycharmProjects\movie-recomendation-system\Data\tmdb_5000_movies.csv")
"""step 2 = change the name of file make sure end with .csv"""
# movies.to_csv("movies_data.csv")
# print(pd.read_csv("movies_data.csv"))

# credit = pd.read_csv(r"C:\Users\Pratik Raj\PycharmProjects\movie-recomendation-system\Data\tmdb_5000_credits.csv")
# credit.to_csv("credit_data.csv")
#
movies = pd.read_csv("movies_data.csv")
# print(movies)
# print(movies.head(10)) # to check the first 10 data sets
credit = pd.read_csv("credit_data.csv")

# print(credit.head(1)["crew"].values)  # to check the crew name for first movie

"""Now merge the both datasets on the basis of title"""

movies = movies.merge(credit,on="title")
# print(movies.shape) #for checking the data column
# print(movies["original_language"].value_counts())

# print(movies.info()) #for better data analysis

""" NOw removing unwanted data from data set"""
""" list of data that we are using from dataset
1. genere
2. id
3. keywoard
4. overview
5. cast
6. crew """

"""keeeping data only for our use """
movies = movies[["movie_id","title",'keywords','overview','cast','crew','genres']]
# print(movies.info())

""" we will keep only three columns(1.movie_id, 2.title, 3.tags(which combine everything)) so, we will add all columns except movie_id and title"""

""" Data preprocessing"""
#  removing all  null data
# print(movies.isnull().sum()) # for checking missing data

# to remove missing data
movies.dropna(inplace=True)
# print(movies.isnull().sum())  #for checking data is dropped or not
# print(movies.duplicated().sum()) #to check data is duplicated or not

# print(movies.iloc[0].genres) # to check the format for the data

""" our data is in this format 
[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]
 we need to change it in this format ["Action","Adventure","Fantasy","Science Fiction"]
"""

# creating a function to manipulate data

def convert(obj):
    L = []
    for i in ast.literal_eval(obj): #ast.literal eval is used beacuse this list has multiple dictionary
        # and all are in string form to convert it into list this module is used
        L.append(i['name'])
    return L

# to check the ast function
# print(ast.literal_eval('[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]'))

#  converting data
movies['genres'] = movies['genres'].apply(convert)
# print(movies.head())

movies['keywords'] = movies['keywords'].apply(convert) # same for keywords
# print(movies["keywords"][0])

""" for cast """
# print(movies["cast"][0])
""" in cast segement we need only 3 - 4 cast beacuse they ae the main cast for that we need to make chnges in our function"""
def convert3(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj): #ast.literal eval is used beacuse this list has multiple dictionary
        # and all are in string form to convert it into list this module is used
        if counter != 3:
            L.append(i['name'])
            counter +=1
        else:
            break
    return L
movies["cast"] = movies["cast"].apply(convert3)
# print(movies["cast"])

""" now for crew its little diffirent beacuse there are lot of crew so i only want director from list for that there are some change in function"""
def fetch_director(obj):
    L =[]
    for i in ast.literal_eval(obj):
        if i["job"] == "Director":
            L.append(i["name"])
            break # beacuse there will only one director in movie
    return L
movies["crew"] = movies["crew"].apply(fetch_director)
# print(movies["crew"])

""" As our overview is in string for merging we need to convert it into list"""
movies["overview"] = movies["overview"].apply(lambda x:x.split())
# print(movies["overview"])

# for removing all spaces beacuse it will create problem as it will read name differently as "pratik raj" as "pratik" different and "raj" is different
movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","")for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ","")for i in x])
movies["crew"] = movies["crew"].apply(lambda x:[i.replace(" ","")for i in x])
movies["cast"] = movies["cast"].apply(lambda x:[i.replace(" ","")for i in x])
#  adding all data in a single list
movies["tags"] = movies["overview"] + movies['keywords'] + movies["cast"] + movies["crew"]

new_df = movies[["movie_id","title","tags"]]  # creating new dataframe with only requires data
# print(new_df)
new_df["tags"] = new_df["tags"].apply(lambda x:" ".join(x))
# print(new_df["tags"][0])

new_df["tags"] = new_df["tags"].apply(lambda x:x.lower()) # converting it into lower as recomended
# new_df["title"] = new_df["title"].apply(lambda x:x.lower()) # converting into lower for easier access as recomended

'**********************************************************************************************'
# print(new_df[new_df['title']=="The Amazing Spider-Man"].movie_id) # to print the movie_id

# new_movies = new_df
# new_movies.drop([2,20],axis=0,inplace=True)
# # print(new_movies[new_movies['title']=="Avatar"].movie_id) # to print the movie_id

import pickle
pickle.dump(new_df.to_dict(),open('movie_dict.pkl','wb'))
