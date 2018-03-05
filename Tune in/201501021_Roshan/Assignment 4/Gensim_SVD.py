import pandas #Python Data Analysis Library
import sklearn.preprocessing as sk
import gensim
import gensim.models.lsimodel as ls

#Loading in data using Pandas library
ratings_dataset = pandas.read_csv('TuneIn_ratings.csv', dtype={'rating': float})
#Printing the first five rows
print (ratings_dataset.head())
#Normalizing the ratings to fit in between 0 to 1 using squash function as  new x=(x - min/ max-min) .
# 1 will be now 0, 2 will be now 0.25, 3 will be now 0.5, 4 will be now 0.75, 5 will be now 1
ratings_dataset.loc[:,'rating'] = sk.minmax_scale(ratings_dataset.loc[:,'rating'] )
#Printing the first five rows after normalization
print (ratings_dataset.head())
#Reshape data (produce a “pivot” table) based on column values.
# Uses unique values from index / columns to form axes of the resulting DataFrame.
R = ratings_dataset.pivot(index = 'user_id', columns ='song_id', values = 'rating').fillna(0).to_sparse(fill_value=0)
print(R.head())
#Interpret the input as a matrix.
R_matrix = R.as_matrix()

#Treat dense numpy array as a streamed gensim corpus in BoW format.
R_corpus=gensim.matutils.Dense2Corpus(R_matrix, documents_columns=True)
print(R_corpus)
#Implements fast truncated SVD
lsi=ls.LsiModel(R_corpus, num_topics=3)

print("Sigma Matrix (Singular Values) :\n")
print(lsi.projection.s)

print("U Matrix : \n")
print(lsi.projection.u)

print("V Transpose Matrix :\n")
VT = gensim.matutils.corpus2dense(lsi[R_corpus], len(lsi.projection.s)).T / lsi.projection.s
print(VT)