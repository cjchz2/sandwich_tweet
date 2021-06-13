CREATE TABLE SANDWICH_TWEETS.TWEETS
(
TWEET_KEY SERIAL,
ID BIGINT UNIQUE,
TEXT VARCHAR(1024) NOT NULL, --Tweets can only be 280 characters, sometimes special characters can create larger tweets.  
USERNAME VARCHAR(50) NOT NULL,
TWEET_DATE TIMESTAMP NOT NULL,
PULLED_DATE TIMESTAMP NOT NULL, 
INSERT_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP - interval '5 hour' --want to set this as a dynamic conversion to central later.
)
