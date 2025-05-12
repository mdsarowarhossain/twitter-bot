import os
import tweepy
import openai
import requests
from io import BytesIO
from datetime import datetime
from time import sleep

# Load environment variables
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize APIs
twitter_auth = tweepy.OAuth1UserHandler(
    TWITTER_API_KEY, TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
)
twitter = tweepy.API(twitter_auth)
openai.api_key = OPENAI_API_KEY

def generate_tweet():
    """Generate tweet text using GPT-4"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{
            "role": "system",
            "content": "You are a wise self-improvement coach. Create concise (max 250 chars), motivational tweets about productivity, mindfulness, or personal growth."
        }],
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def generate_image(prompt):
    """Generate image using DALL-E 3"""
    response = openai.Image.create(
        model="dall-e-3",
        prompt=f"Minimalistic inspirational image: {prompt}. Clean, elegant, motivational style",
        size="1024x1024",
        quality="standard",
        n=1
    )
    return requests.get(response.data[0].url).content

def post_tweet():
    try:
        # Generate content
        tweet = generate_tweet()
        image = generate_image(tweet)
        
        # Upload media
        media = twitter.media_upload("motivation.jpg", file=BytesIO(image))
        
        # Post tweet
        twitter.update_status(
            status=tweet,
            media_ids=[media.media_id]
        )
        print(f"✅ Posted at {datetime.now()}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    post_tweet()
    # Heroku Scheduler will handle timing