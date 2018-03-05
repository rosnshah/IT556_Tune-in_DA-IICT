import pandas #Python Data Analysis Library
import sklearn.preprocessing as sk
from sklearn.decomposition import TruncatedSVD
from sklearn.utils.extmath import randomized_svd
#Loading in data using Pandas library
ratings_dataset = pandas.read_csv('TuneIn_ratings.csv', dtype={'rating': float})
#Printing the first five rows
print (ratings_dataset.head())
#Normalizing the ratings to fit in between 0 to 1 using squash function as  new x=(x - min/ max-min) .
# 1 will be now 0, 2 will be now 0.25, 3 will be now 0.5, 4 will be now 0.75, 5 will be now 1
ratings_dataset.loc[:,'rating'] = sk.minmax_scale(ratings_dataset.loc[:,'rating'] )
#Printing the first five rows after normalization
print (ratings_dataset.head())
#Forming matrix using user_id as row headers, song_id as column headers and rating as the respective values.
R = ratings_dataset.pivot(index = 'user_id', columns ='song_id', values = 'rating').fillna(0)
print(R)
# Forms the final matrix R_matrix
R_matrix = R.as_matrix()
# Decomposing R_matrix to U, sigma and V transpose matrix
U, Sigma, VT = randomized_svd(R_matrix,n_components=2)

print("U Matrix :\n")
print(U)
print("Sigma Matrix (Singular Values) :\n")
print(Sigma)
print("V Transpose Matrix :\n")
print(VT)

# Performing Truncated SVD with 30 components in final result and 10 iterations.
svd = TruncatedSVD(n_components=30, n_iter=10)
svd.fit(R_matrix)
print("Variance ratio:\n")
print(svd.explained_variance_ratio_)
print("Components:\n")
print(svd.components_)
print("Singular Values:\n")
print(svd.singular_values_)