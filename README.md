# mvd-weather-twitterbot
**[Twitter bot](https://twitter.com/NubelGPT)** that uses OpenAI, Open-Meteo and Twitter APIs to make a daily tweets about the weather in Montevideo.

You can easily customize the behaviour of the bot to suit your needs by modifying the `LATITUDE`, `LONGITUDE`, `TIMEZONE`, `GPT_PROMPT` and `GPT_ROLE` constants at the beginning of `main.py`. You can find a list of timezone codes [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).

### Requirements
Requires installing the following libraries:
- [openai](https://platform.openai.com/docs/libraries)
- [tweepy](https://www.tweepy.org/)
- [requests](https://pypi.org/project/requests/)
- [dotenv](https://pypi.org/project/python-dotenv/)

For the script to work, you need to have a `.env` file in the same directory as `main.py`. In this file, you should have all the necessary API keys as follows:

    OPENAI_API_KEY="XXXXXXXXX"
    TWITTER_CONSUMER_KEY="XXXXXXXXX"
    TWITTER_CONSUMER_SECRET="XXXXXXXXX"
    TWITTER_ACCESS_TOKEN="XXXXXXXXX"
    TWITTER_ACCESS_SECRET="XXXXXXXXX"
    TWITTER_BEARER_TOKEN="XXXXXXXXX"
    TWITTER_CLIENT_ID="XXXXXXXXX"
    TWITTER_CLIENT_SECRET="XXXXXXXXX"

### Reference for APIs used:
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Open-Meteo API Reference](https://open-meteo.com/en/docs)
- [Twitter API Reference](https://developer.twitter.com/en/docs/api-reference-index)
