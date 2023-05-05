#########################################################################################################################

# Imports to handle API keys
from dotenv import load_dotenv
import os

#########################################################################################################################

# Imports to communicate with APIs
import openai
import requests
import tweepy

#########################################################################################################################

import datetime # Used for formatting date received from weather API
import time # Used to wait between Twitter API requests

#########################################################################################################################

# Loads different API keys from .env file
load_dotenv()

# Authenticate with OpenAI API 
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create Twitter API object
twitter_client = tweepy.Client(
    bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
    consumer_key=os.getenv("TWITTER_CONSUMER_KEY"),
    consumer_secret=os.getenv("TWITTER_CONSUMER_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_SECRET"),
    wait_on_rate_limit=True
)

#########################################################################################################################

weather_endpoint = "https://api.open-meteo.com/v1/forecast?latitude=-34.90&longitude=-56.19&daily=temperature_2m_max," \
"temperature_2m_min,sunrise,sunset,uv_index_max,precipitation_sum,precipitation_probability_max,windspeed_10m_max," \
"winddirection_10m_dominant&windspeed_unit=kn&timezone=America%2FSao_Paulo"

# Request weather data from Open-Meteo API
weather_response = requests.get(weather_endpoint)

# Function to convert wind direction from degrees to cardinals
def degrees_to_cardinal(d):
    '''
    Convert degrees to cardinal direction names
    '''
    dirs = ['Norte', 'Norte-noreste', 'Nor-noreste', 'Este-noreste', 'Este', 'Este-sureste', 'Sureste', 
            'Sur-sureste', 'Sur', 'Sur-suroeste', 'Suroeste', 'Oeste-suroeste', 'Oeste', 'Oeste-noroeste', 
            'Noroeste', 'Norte-noroeste']
    ix = int((d + 11.25)/22.5)
    return dirs[ix % 16]

# If response is good then response data is formatted into a text prompt for GPT
if weather_response.status_code == 200:
    max_temp = weather_response.json()["daily"]["temperature_2m_max"][0]
    min_temp = weather_response.json()["daily"]["temperature_2m_min"][0]
    rain_sum = weather_response.json()["daily"]["precipitation_sum"][0]
    rain_prob_max = weather_response.json()["daily"]["precipitation_probability_max"][0]
    uv_max = weather_response.json()["daily"]["uv_index_max"][0]
    sunrise = datetime.datetime.fromisoformat(weather_response.json()["daily"]["sunrise"][0])
    sunset = datetime.datetime.fromisoformat(weather_response.json()["daily"]["sunset"][0])
    wind_max = weather_response.json()["daily"]["windspeed_10m_max"][0]
    wind_dir = degrees_to_cardinal(weather_response.json()["daily"]["winddirection_10m_dominant"][0])
    # Content for GPT completion request:
    daily_forecast = f"max. temp = {max_temp} celsius, min. temp = {min_temp} celsius, sunrise time = {sunrise}," \
    f" sunset time = {sunset}, total rainfall = {rain_sum} millimeters, max. rain probability = {rain_prob_max}," \
    f" max. uv index = {uv_max}, max wind = {wind_max} knots, dominant wind direction = {wind_dir}."
else:
    raise ValueError("Incorrect response from Open-Meteo.")

#########################################################################################################################

prompt = "Write a short tweet in rioplatense spanish about weather forecast for the day in Montevideo with " \
"the following data: " + daily_forecast

# Requests completion from OpenAI API
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a uruguayan meteorologist. " \
       "You are given daily weather data and you write a daily tweet about it."},
      {"role": "user", "content": prompt}
    ]
  )

# Saves relevant part of OpenAI API response
if(completion.choices[0].finish_reason == "stop"):
    openai_response = completion.choices[0].message.content.strip('"')
    print("\nOriginal GPT response: " + openai_response + "\n")
else:
    raise ValueError("Incorrect response from OpenAI API.")

#########################################################################################################################

# Will be used if OpenAI response needs to be shortened to fit in a tweet
remainder = " "
shortened = False

# Post a Tweet using Twitter API:
for i in range(50): # Rate limit for POST_2_tweets endpoint is 100, tries at maximum 50 times to post status update
    if(len(openai_response) <= 265): # Check if tweet is short enough to be posted
        try:
            # Attempt to create the tweet
            if(not shortened): # Original response was short enough to be posted as is
                tweet = twitter_client.create_tweet(text=openai_response)
                print("Original response posted successfully!\n")
                break  # Exit the loop if the tweet was posted successfully
            else: # Original had to be shortened
                # Attempt to post first part of tweet:
                print("Shortened tweet:\n")
                print(openai_response + " (1/2)..." + "\n")
                tweet = twitter_client.create_tweet(text=openai_response + " (1/2)...")
                print("Shortened tweet posted succesfully!\n")
                time.sleep(10) # Wait 10s 
                # Attempt to post second part of tweet as reply to first tweet:
                remainder_array.reverse()
                remainder = " ".join(remainder_array)
                print("Second part of tweet:\n")
                print("(2/2) " + remainder + "\n")
                reply_tweet = twitter_client.create_tweet(
                    text="(2/2) " + remainder,
                    in_reply_to_tweet_id=tweet.data['id']
                )
                print("Second part of tweet posted succesfully!\n")
                break  # Exit the loop if the tweet was posted successfully
        except tweepy.errors.TweepyException: 
            print("Warning: Entered exception!\n")
            raise ValueError("Incorrect response from Twitter API.")
    else:
        # If the tweet was too long, shorten and try again:
        openai_response_array = openai_response.split()
        openai_response = " ".join(openai_response_array[:-1])
        # Updates an array with what is removed from the original response:
        remainder_array = remainder.split()
        remainder_array.append(openai_response_array[-1])
        remainder = " ".join(remainder_array)
        # Try again:
        shortened = True
        print("Tweet shortened!\n")

#########################################################################################################################

