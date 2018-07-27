''' This module contains the class that extract
the tweets of a user and push them to mongoDB. '''

import tweepy
import time

import config


class ExportTweets:
    ''' Class containing components to export tweets
    from twitter to the mongo db collection. '''

    def __init__(self, username, logging):
        self.user_name = username
        self.logging = logging
        self.auth = tweepy.OAuthHandler(
            config.CUSTOMER_KEY, config.CUSTOMER_SECRET)
        self.auth.set_access_token(config.AUTH_TOKEN, config.AUTH_SECRET_KEY)
        self.api = tweepy.API(self.auth)

    def get_user_tweets(self):
        ''' Get all the tweets by user name in limits given by twitter
        apis. '''
        tweets = []
        if self.user_exists_on_twitter(self.user_name):
            for page in self.handle_limit_issue(tweepy.Cursor(
                    self.api.user_timeline,
                    screen_name=self.user_name,
                    count=config.TWEET_PER_PAGE).pages()):
                for tweet in page:
                    tweet_info = {}
                    tweet_info['tweet_id'] = tweet.id_str
                    tweet_info['tweet_text'] = tweet.text
                    tweet_info['created_at'] = tweet.created_at.strftime(
                        config.DATE_FORMAT)
                    tweet_info['user_id'] = tweet.user.id_str
                    tweet_info['screen_name'] = tweet.user.screen_name
                    tweet_info['total_tweets_on_twitter'] = tweet.user.statuses_count
                    tweets.append(tweet_info)
        return tweets

    def handle_limit_issue(self, cursor):
        ''' Lazy evaluates the cursors values and if limit
        error is encountered, handles it with sleeping for some time.'''
        while True:
            try:
                yield cursor.next()
            except tweepy.TweepError:
                self.logging.error('Hit exceeded allowed hits. Wait.')
                time.sleep(config.FALL_BACK_TIME)

    def user_exists_on_twitter(self, user_name):
        try:
            self.api.user_timeline(screen_name=user_name)
            return True
        except tweepy.TweepError:
            return False
