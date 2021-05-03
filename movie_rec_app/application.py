from flask import Flask, render_template, make_response, jsonify, request
from movie_rec_app.recommender import MOVIES, get_rating_from_user, get_three_random_recommendations, get_nine_random_recommendations, get_convert_user_input
from movie_rec_app.big_surprise import big_surprise

app = Flask(__name__)


random3 = get_three_random_recommendations()
random9_2b_rated = get_nine_random_recommendations()

@app.route("/recommender")  # <-- decorator
def recommend():

    user_input = dict(request.args)
    ### THIS IS THE DATA THAT WAS ASSEMBLED BY THE FORM!!!
    print(user_input)
    #movie = get_rating_from_user(user_input)
    test_df_var = get_convert_user_input(user_input)
    recom_list = big_surprise(test_df_var)
    test_df_var = str(test_df_var)
    test_df_var = print(test_df_var)
    return render_template("recommendation.html", recom_list = recom_list)


@app.route("/")
def main_page():
    return render_template("index.html", random3 = random3, random9_2b_rated = random9_2b_rated)

if __name__ == "__main__":
    # this block is executed when we run application.py, not when we import it
    app.run(debug=True, port=5000)