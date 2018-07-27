''' This module calls the export tweet module on each user and also
maintains the states of users that have already been searched, that are
either suspended or dont have an active account. '''
import pickle
import logging
import time

from pymongo import MongoClient

from users import screen_names
from export_tweets import ExportTweets

LOG_FILE = 'main.log'
DONE_USERS_RECORD = 'done_users.db'
USERS_NOT_PRESENT = 'not_present_users.db'
CLIENT = MongoClient()


def get_done_users():
    ''' Get the users for which calculations have been already done.'''
    with open(DONE_USERS_RECORD, 'rb') as file_handler:
        try:
            users_done = pickle.load(file_handler)
        except EOFError:
            users_done = set()
    return users_done


def update_user_fail(failed_users):
    '''
    Those users whose profile is not present
    are added into this file.
    '''
    with open(USERS_NOT_PRESENT, 'wb') as file_handler:
        pickle.dump(failed_users, file_handler)


def update_done_users(done_user_set):
    ''' Save the users that have been done. '''
    with open(DONE_USERS_RECORD, 'wb') as file_handler:
        pickle.dump(done_user_set, file_handler)


def save_to_db(tweets):
    ''' This module saves the list of dictionaries to the db. '''
    db = CLIENT.twitter
    db.tweets.insert_many(tweets)


if __name__ == '__main__':
    done_users = get_done_users()
    failed_users = set()
    logging.basicConfig(filename=LOG_FILE, level=logging.ERROR)
    user_count = 0
    for user in screen_names:
        try:
            user_count += 1
            if user not in done_users:
                export_obj = ExportTweets(user, logging)
                tweets = export_obj.get_user_tweets()
                # Tweets are false not empty for non existing users
                if tweets is None:
                    failed_users.add(user)
                    update_user_fail(failed_users)
                    continue
                save_to_db(tweets)
                done_users.add(user)
                update_done_users(done_users)
                print('Total number of users processed:- ' + str(user_count))
                print('Tweets fetched for screen name:- ' + user)
        except Exception as e:
            logging.error('User Id failed:- ' + user)
