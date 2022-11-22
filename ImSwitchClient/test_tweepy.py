import tweepy


consumer_key = ""
consumer_secret = ""

access_token = "1594066265705955328-rwRJRk19OqFPwCtu387IRfNLaLamlw"
access_token_secret = "eSxxiMBFG8QMR9DzIS69EsuhISo7eRXKrdqCxGchkBJn9"

bearer_token = "AAAAAAAAAAAAAAAAAAAAAJgNjgEAAAAA143B6CpqLG40%2BFUQWlf%2Fa8g9UAo%3DUybqm2WZTYYQlZ6DrU7bKbF139kvwjh2iD67w25Ak9gHKlDhGA"
app_name = "uc2_micrsocope_1"

client_id = "SklfTUVXZmlTeE80VVBUNEVidWE6MTpjaQ"
client_secret = "BQiyZC2DBQc8wq-ekK8G2vWORH-8p5AZ5sfe8qTKfYXgphTwv-"


auth = tweepy.OAuth2BearerHandler(bearer_token)
api = tweepy.API(auth)

client = tweepy.Client(bearer_token=bearer_token)
api_key = "iF2Ggd8t2m1CPkG3euu3kNUY1"
api_key_secret = "JRHOrm5hgGB4NxKuhcwhSakQWh4YYR8YqnAfOVb8HMg7D6zjYH"


# Create Tweet
client = tweepy.Client(consumer_key=api_key,
                       consumer_secret=api_key_secret,
                       access_token=access_token,
                       access_token_secret=access_token_secret)

# Replace the text with whatever you want to Tweet about
response = client.create_tweet(text='hello world')
print(response)


#%%
import tweepy
import logging

import time

def create_api():
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)#,        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, keywords, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info(f"Answering to {tweet.user.name}")

            if not tweet.user.following:
                tweet.user.follow()

            api.update_status(
                status="Please reach us via DM",
                in_reply_to_status_id=tweet.id,
            )
    return new_since_id

def main():
    api = create_api()
    since_id = 1
    while True:
        since_id = check_mentions(api, ["help", "support"], since_id)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()
    
#%%

import tweepy 

bearer_token = "AAAAAAAAAAAAAAAAAAAAAJgNjgEAAAAA143B6CpqLG40%2BFUQWlf%2Fa8g9UAo%3DUybqm2WZTYYQlZ6DrU7bKbF139kvwjh2iD67w25Ak9gHKlDhGA"

class TweetListener(tweepy.StreamingClient):

    def on_tweet(self, tweet):
        print(tweet.text)


stream = TweetListener(bearer_token=bearer_token)

stream.add_rules(tweepy.StreamRule("from:@openuc2bot"))
stream.filter()