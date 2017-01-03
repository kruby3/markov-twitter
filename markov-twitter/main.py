
from flask import Flask, render_template
from flask import redirect
from flask import request
from flask import url_for
import tweepy

from markov_gen import MarkovGen
app = Flask(__name__)
app.debug = True

#Enter API keys from
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''


@app.route('/', methods=['GET'])
def index():
    error = request.args.get('error')
    return render_template('index.html', error = error)

@app.route('/tweets', methods=['POST'])
def tweets():
    twitter_handle = request.form['twitter_handle']
    num_tweets = int(request.form['num_tweets'])
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    #Check if user exists before generating tweets
    #If user exists, tweet page is loaded
    #If user does not exist, error is shown
    error = None
    try:
        user = api.get_user(twitter_handle)
    except tweepy.TweepError as e:
        error = "Twitter handle does not exist"
        return redirect(url_for('index', error = error))

    picture = user.profile_image_url
    markov = MarkovGen(twitter_handle, 1, 140, api)
    result = []

    #Generate given number of tweets
    genTweets = 0
    while genTweets < num_tweets:
        tweet = markov.generate_text()
        if tweet != "":
            result.append(tweet)
            genTweets += 1

    return render_template('tweets.html', result=result, twitter_handle=twitter_handle, picture = picture)

if __name__ == "__main__":
    app.run()