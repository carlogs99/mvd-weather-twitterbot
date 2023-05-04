from dotenv import load_dotenv
import os
import openai
import requests
import datetime
import tweepy
import re

load_dotenv()

# Authenticate with API keys and access tokens
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create API object
twitter_client = tweepy.Client(
    bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
    consumer_key=os.getenv("TWITTER_CONSUMER_KEY"),
    consumer_secret=os.getenv("TWITTER_CONSUMER_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_SECRET"),
    wait_on_rate_limit=True
)

weather_response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=-34.90&longitude=-56.19" \
                        "&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max," \
                        "precipitation_sum,precipitation_probability_max&timezone=America%2FSao_Paulo")

if weather_response.status_code == 200:
    max_temp = weather_response.json()["daily"]["temperature_2m_max"][0]
    min_temp = weather_response.json()["daily"]["temperature_2m_min"][0]
    rain_sum = weather_response.json()["daily"]["precipitation_sum"][0]
    rain_prob_max = weather_response.json()["daily"]["precipitation_probability_max"][0]
    uv_max = weather_response.json()["daily"]["uv_index_max"][0]
    sunrise = datetime.datetime.fromisoformat(weather_response.json()["daily"]["sunrise"][0])
    sunset = datetime.datetime.fromisoformat(weather_response.json()["daily"]["sunset"][0])

    daily_forecast = f"max. temp = {max_temp} celsius, min. temp = {min_temp} celsius, sunrise time = {sunrise}," \
    f" sunset time = {sunset}, total rainfall = {rain_sum} millimeters, max. rain probability = {rain_prob_max}," \
    f" max. uv index = {uv_max}."
else:
    raise ValueError("Incorrect response")


prompt = "Write an orignal tweet, using rioplatense spanish," \
        " about the weather forecast for the day in Montevideo using the following data: " + daily_forecast 

# completion = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[
#       {"role": "system", "content": "You are a helpful assistant. Answer the given question."},
#       {"role": "user", "content": prompt}
#     ]
#   )

# openai_response = completion.choices[0].message.content.rstrip()
# print(openai_response + "\n")

twitter_client.create_tweet(text="Testing...")

# while True:
#     try:
#         # attempt to create the tweet
#         twitter_client.create_tweet(text=openai_response)
#         print("Tweet posted successfully!")
#         break  # exit the loop if the tweet was posted successfully
#     except tweepy.errors.BadRequest:
#         # if the tweet was too long, truncate the text and try again
#         openai_response_array = openai_response.split()
#         openai_response = " ".join(openai_response_array[:-1])
#         print(openai_response)
#         continue


