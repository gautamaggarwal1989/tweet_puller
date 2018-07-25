This project ain't a big deal but might be useful for someone I guess.
This is basically code to pull tweets for the given user from the
twitter via twitter apis.

---------------------------------------------------------------------
Steps to setup the script before running script:-
---------------------------------------------------------------------
1. Enter the screen names of people whose tweets you need in users.py.
2. Create an app account on twitter and add the credentials in the export_tweets.py.
3. Create files main.log, done_users.db, not_present_users.db.
4. Create a virtual environment and install dependencies mentioned in requirements.txt.
5. Check if mongo db is running or not. Enter credentials if required in main.py.
6. Activate the virtual environment and run 'python main.py'.

---------------------------------------------------------------------
Things to know:-
---------------------------------------------------------------------
1. Script maintains state i.e if it breaks in between, It will still remember the users done and will only import tweets for users not done if restarted. Though it wont happen that It breaks on its own. But In case if you press 'ctrl + c' by mistake.
2. MongoDB is without password and installs on localhost.
3. There are api rate limits put by twitter that is encountered by script to sleep for 60 seconds. You can change that if you want. I will try to find some time to change the mechanism to exponential backoff.

Enjoy :)
