import os
import json
import random
from PIL import Image, ImageDraw, ImageFont
import tweepy
# from dotenv import load_dotenv
import urllib.request

os.environ["CONSUMER_KEY"] = ""
os.environ["CONSUMER_SECRET"] = ""
os.environ["ACCESS_TOKEN"] = ""
os.environ["ACCESS_TOKEN_SECRET"] = ""


def generate_image(text):
    # Create a black image
    width, height = 600, 600
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Load a font
    font_path = os.path.abspath("font.ttf")
    font_size = 70
    font = ImageFont.truetype(font_path, font_size)

    # Calculate the font size that can fill 90% of the image
    while True:
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        if text_width >= 0.9 * width or text_height >= 0.9 * height:
            break
        font_size += 1
        font = ImageFont.truetype("font.ttf", font_size)

    # Calculate the position to center the text
    x = (width - text_width) / 2
    y = (height - text_height) / 2 * 0.9

    # Draw the text in red color
    draw.text((x, y), text, fill="#00aabb", font=font)

    image_file = f"{text.replace(' ', '_').replace('/', '_').replace(':', '_')}.png"
    image.save(image_file)

    return image_file



def post_to_twitter(text, image):
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)


    # image_path = "image.png"
    media = api.media_upload(image)
    media_id = media.media_id 

    response = client.create_tweet(
        text=text, media_ids=[media_id]
    )
    print(f"https://twitter.com/user/status/{response.data['id']}")
    
    with open("twt.log", "a") as log_file:
        log_file.write(tweet_url + "\n")
    # Remove the image file
    # os.remove(image_file)

def get_next_line(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            pos = int(file.readline())
            return pos
    else:
        return 0

def update_next_line(file_path, pos):
    with open(file_path, 'w') as file:
        file.write(str(pos))

if __name__ == "__main__":

    # json_file_path = "keyword.json"
    txt_file_path = "list.txt"
    pos_file_path = "pos.log"

    # Read the next line to post
    next_line = get_next_line(pos_file_path)

    with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
        lines = txt_file.readlines()

    if next_line >= len(lines):
        print("All lines have been posted.")
    else:
        # Select the next line from list.txt
        text = lines[next_line].strip().split("\"")[1]
        keyword = text.replace(' ', '_').replace('/', '_').replace(':', '_')

        # Generate the image
        image = generate_image(text)

        # Post the tweet to Twitter
        post_to_twitter(lines[next_line] + """Please share your AI-artwork about it.
Every day we can get a new idea!
#PromptChallenge #AIArt #promptShare #Midjourney #StableDiffusion #""" + keyword, image)

        # Update the next line to post
        next_line += 1
        update_next_line(pos_file_path, next_line)


