import requests
import boto3
from datetime import datetime
import pytz

s3_resource = boto3.resource('s3')

with open('twitter_api_token.txt', 'r') as f:
	token = f.readline()

#Removing white space/carriage return
token = token.strip()

class tweet_grabber:

    def __init__(self, token, tweet_topic, number_of_tweets=1):
        self.number_of_tweets = number_of_tweets
        self.token = token
        self.tweet_topic = tweet_topic

    #Authenticate into twitter API and get response.
    def auth_and_call(self):
        #Set up and execute API call
        header = {"Authorization": "Bearer " + token }
        param={"tweet_mode":"extended","count":self.token}
        response = requests.get("https://api.twitter.com/1.1/search/tweets.json?q={topic}&lang=en".format(topic = self.tweet_topic),
                                 headers = header,params=param)
        self.response = response

    def tweet_cleaning(self):
        response = self.response
        all_status = [(i,j) for i,j in  enumerate(response.json()['statuses'])]
        text_raw = [j['retweeted_status']['full_text'] if 'retweeted_status' in j else j['full_text'] for i,j in all_status]
        text_encode = [tweet.encode(encoding = 'ascii', errors = 'ignore') for tweet in text_raw]
        text_list = [tweet.decode(encoding = 'utf-8') for tweet in text_encode]
        user_name_raw=[str(i['user']['name']) for i in response.json()['statuses']]
        user_name_encode = [user.encode(encoding = 'ascii', errors = 'ignore') for user in user_name_raw]
        user_name_list = [user.decode(encoding = 'utf-8') for user in user_name_encode]
        tweet_datetime_str=[i['created_at'] for i in response.json()['statuses']]
        tweet_date_list=[datetime.strptime(tweet_datetime_str[i],'%a %b %d %H:%M:%S +%f %Y') for i,j in enumerate(tweet_datetime_str)]
        tweet_date_str_list = [str(i) for i in tweet_date_list]
        tweet_id_list = [str(i['id']) for i in response.json()['statuses']]
        self.text_list = text_list
        self.user_name_list = user_name_list
        self.tweet_date_str_list = tweet_date_str_list
        self.tweet_id_list = tweet_id_list

    def write_tweets_to_s3(self, local_file_path, bucket_name):
        for i in range(len(self.text_list)):
            date_now = datetime.now().replace(microsecond = 0)
            date_now_str = str(date_now)
            file_name = self.tweet_topic + "%{dt}%ident".format(dt = date_now_str, ident = self.tweet_id_list[i])
            full_file_path =  local_file_path + file_name
            with open(full_file_path, mode = 'w') as f:
                f.write(self.tweet_id_list[i])
                f.write("^&*>*&^")
                f.write(self.text_list[i])
                f.write("^&*>*&^")
                f.write(self.user_name_list[i])
                f.write("^&*>*&^")
                f.write(self.tweet_date_list[i])
                f.write("^&*>*&^")
                f.write(date_now_str)
        s3_obj = s3_resource.Object(bucket_name, file_name)
        s3_obj.upload_file(Filename = full_file_path, ExtraArgs = {'ContentType':'text/plan'})




file_path = '/home/ec2-user/sandwich_tweet_v2/sandwich_tweet'
bucket_name = 'sandwich-tweet-chris-cunningham'

sandwich_tweet_grabber = tweet_grabber(token, 'sandwich')
sandwich_tweet_grabber.auth_and_call()
sandwich_tweet.tweet_cleaning()
sandwich_tweet.write_tweets_to_s3(file, bucket_name)
