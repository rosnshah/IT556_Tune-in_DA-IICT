import pandas as pd
from surprise import Reader
from surprise import SVD
from surprise import Dataset
from surprise.model_selection import cross_validate
from guppy import hpy

if __name__ == '__main__':
    df = pd.read_csv("data_1m.csv")
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df[['user_id', 'song_id', 'rating']], reader)
    algo = SVD()
    cross_validate(algo,data,measures=['RMSE'],cv=5,verbose=True)
    h = hpy()
    print h.heap()