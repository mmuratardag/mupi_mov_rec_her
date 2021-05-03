
import pandas as pd
import numpy as np

from collections import defaultdict

from surprise import SVD, KNNBasic, Reader, Dataset, accuracy, dump
from surprise.model_selection import train_test_split


def big_surprise(user_input):
    
    user_input_object = user_input

    mdf = pd.read_csv('movie_rec_app/data/df_movieId_unique_title.csv')

    id_list = []
    for movie in user_input_object:
        idx = mdf[mdf.title_only == movie[0]].index.tolist()[0]
        id_list.append(mdf.iloc[idx]['movieId'])

    id_list_string = [str(x) for x in id_list]

    rating_list = []
    for rating in user_input_object:
        rat = rating[1]
        rating_list.append(rat)

    rating_list_float = [float(x) for x in rating_list]

    user_input_df = pd.DataFrame(list(zip(id_list_string, rating_list_float)), columns =['movieId', 'rating'])
    user_input_df['userId'] = '999999'
    user_input_df = user_input_df[['userId','movieId', 'rating']]

    ratings = pd.read_csv('movie_rec_app/data/ratings.csv')
    ratings = ratings [['userId', 'movieId', 'rating']]
    concat_df = pd.concat([ratings, user_input_df], axis = 0, ignore_index = True)

    reader = Reader()
    surprise_data = Dataset.load_from_df(concat_df, reader)
    trainset = surprise_data.build_full_trainset()
    algo = SVD(n_factors = 23, random_state = 666)
    algo.fit(trainset)
    testset = trainset.build_anti_testset()
    predictions = algo.test(testset)

    def get_top_n(predictions, n=10):
        """Return the top-N recommendation for each user from a set of predictions.

        Args:
            predictions(list of Prediction objects): The list of predictions, as
                returned by the test method of an algorithm.
            n(int): The number of recommendation to output for each user. Default
                is 10.

        Returns:
        A dict where keys are user (raw) ids and values are lists of tuples:
            [(raw item id, rating estimation), ...] of size n.
        """

        # First map the predictions to each user.
        top_n = defaultdict(list)
        for uid, iid, true_r, est, _ in predictions:
            top_n[uid].append((iid, est))

        # Then sort the predictions for each user and retrieve the k highest ones.
        for uid, user_ratings in top_n.items():
            user_ratings.sort(key=lambda x: x[1], reverse=True)
            top_n[uid] = user_ratings[:n]

        return top_n

    top_n = get_top_n(predictions, n=10)

    our_user = list(top_n.items())[-1]
    our_user_estimated = our_user[1]
    rec_movie_id=[]
    for a,b in enumerate(our_user_estimated):
        rec_movie_id.append(b[0])
        
    movie_title_list=[]
    for element in rec_movie_id:
        idx = mdf[mdf.movieId==element].index.tolist()[0]
        movie_title_list.append(mdf.iloc[idx].title_only)
    
    return movie_title_list

