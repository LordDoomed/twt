import os
import random
import tweepy
from dotenv import load_dotenv

load_dotenv()

def post_with_text(text):
    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_token_secret = "" 

    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )

    try:
        tweet = client.create_tweet(text=text)
        print(f"Tweet posted: {tweet.data['id']}")
        return True
    except tweepy.errors.TweepyException as e:
        print(f"Error posting tweet: {e}")
        return False

def get_next_tweet_url(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            tweet_url = file.readline().strip()
            return tweet_url
    else:
        return None

def get_next_line_number(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            line_number = int(file.readline().strip())
            return line_number
    else:
        return 0

def update_next_line_number(file_path, line_number):
    with open(file_path, 'w') as file:
        file.write(str(line_number))

if __name__ == "__main__":
    tweet_log_path = "twt.log"
    retweet_log_path = "retwt.log"

    # Read the next line number to post
    next_line_number = get_next_line_number(retweet_log_path)

    with open(tweet_log_path, 'r') as tweet_file:
        lines = tweet_file.readlines()

        if next_line_number >= len(lines):
            print("No more tweets to post.")
        else:
            # Read the next tweet URL to post
            next_tweet_url = lines[next_line_number].strip()
            print(next_tweet_url)

            # Modify the text as per your requirements
            additional_text = "今日AI主题 #DailyIdea #AIart "

            # Combine the URL and additional text
            tweet_text = f"{additional_text} {next_tweet_url}"
            print(tweet_text)
            if post_with_text(tweet_text):
                # Update the next line number to post
                next_line_number += 1
                update_next_line_number(retweet_log_path, next_line_number)