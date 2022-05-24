from Data_manipulation import new_df
import numpy as np
""" Now we have data for our recomendation system to work we need to make vectors of data so that the nearest vector will be picked out
 so that movie recomendation sysytem will recomend the movie on the basis of the the vector.
  For the vectorization we will use the "BAG OF DATA" it will combine all the letters and make it as a matrix and we will convert
   that matrix into 2-D matrix for our convience"""

""" "BAG OF WORDS " = tags1 + tags 2 +...........+ n.   After we got a big string and compare the individual tags and count the no of words matching
with big string eg:- pratik present in big string is 5 times. and fromo that we will make a vector.
          eg=  w1 = Action,w2=romance,w3=comedy
 eg:- for movie 1 w1        w2      w3
                  5         3       8
          movie 2 w1        w2      w3
                  7         2       3 etc"""

""" NOTE while counting the word we will not count stop word stop word are like "are, is, i, am,etc..." while performaning we will leave those words."""

# for counting word we can do it or we can use library we are using sklearn it has  a very good module to count known as CountVectorizer
# link for documentation https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
# form this module will will use 2 functions 1.max_features=None,(to count max no of words)2.stop_words=None(to elimante stop words)

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words="english")
vectors = cv.fit_transform(new_df["tags"]).toarray() #toarray() is used to convert vector into matrix
# print(vectors.shape) # to check total records

""" now we have matrix if we check the words and total no of their presence we can see many wors having samemeaning repeating 
eg:- accept and accepting 'abuse', 'abusive' ,'accept', 'accepted',
so we need to solve this problem  for that we will apply Stemming """
# for checking the words present
# print(cv.get_feature_names())

# Apply Stemming

""" For Stemming we have to use a library called "NLTK" we have to install that installl command are" pip install nltk" """
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

# create a function to steam our all words
def stem(text):
    y =[]
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)
# now apply this function to tags
new_df["tags"] = new_df["tags"].apply(stem)
cv = CountVectorizer(max_features=5000,stop_words="english")
vectors = cv.fit_transform(new_df["tags"]).toarray()
# print(cv.get_feature_names())

"""now we calculate cosine function for distance as we need to calculate which is closer 
HEre we are using cosine instead of euclidean distance as euclidean distance doesnot work good for big data set
we can calculate cosine from "SKLEARN library" in that a function is given to calculate cosine distance """

from sklearn.metrics.pairwise import cosine_similarity    #similarity beacuse its just give us least distance
similarity = cosine_similarity(vectors) # this will give us similarity score with every movie including itself
# print(similarity[1]) #to check

""" we will make a function to recomend the movie based on the given movie name we will fetch out the index  that will give us the vector
and from that vector we will sort the vector and retrieve top 5 or top 10 based ob the demand"""

# print(sorted(list(enumerate(similarity[0])),reverse=True,key=lambda x:x[1])[1:6]) # for testing of aour model
def recommend(movie):
    # movie = movie.lower()
    movie_index = new_df[new_df['title']==movie].index[0] # here index zero bcz we have to find out zero matrix in similarity for given movie
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True, key=lambda x:x[1])[1:6]
    for i in movies_list:
        lst = (new_df.iloc[i[0]].title)
        print(lst.title()) #.title is used to convert firsat letter in capital
        # print(i)
# print(recommend('The Avengers'))
import  pickle
pickle.dump(similarity,open('similarity.pkl','wb'))
