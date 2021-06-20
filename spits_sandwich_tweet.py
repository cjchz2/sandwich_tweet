import requests
import boto3
from datetime import datetime
import pytz
from pytz import timezone

s3_resource = boto3.resource('s3')

with open('twitter_api_token.txt', 'r') as f:
	token = f.readline()

#Removing white space/carriage return
token = token.strip()

def get_sandwich_tweets():
    #Set up and execute API call
    header = {'Authorization': 'Bearer ' + token }
    param={'tweet_mode':'extended','count':1}
    response = requests.get('https://api.twitter.com/1.1/search/tweets.json?q=sandwich&lang=en', headers = header,params=param)
    return response

def package_sandwich_tweets(response):
    all_status = [(i,j) for i,j in  enumerate(response.json()['statuses'])]
    text_raw = [j['retweeted_status']['full_text'] if 'retweeted_status' in j else j['full_text'] for i,j in all_status ]
    text_encode = [tweet.encode(encoding = 'ascii', errors = 'ignore') for tweet in text_raw]
    text_list = [tweet.decode(encoding = 'utf-8') for tweet in text_encode ]
    user_name_raw=[str(i['user']['name']) for i in response.json()['statuses']]
    user_name_encode = [user.encode(encoding = 'ascii', errors = 'ignore') for user in user_name_raw]
    user_name_list = [user.decode(encoding = 'utf-8') for user in user_name_encode]
    tweet_datetime_str=[i['created_at'] for i in response.json()['statuses']]
    tweet_date_list=[datetime.strptime(tweet_datetime_str[i],'%a %b %d %H:%M:%S +%f %Y') for i,j in enumerate(tweet_datetime_str)]
    tweet_date_str_list = [str(i) for i in tweet_date_list]
    tweet_id_list = [str(i['id']) for i in response.json()['statuses']]
    return text_list, user_name_list, tweet_date_str_list, tweet_id_list

response = get_sandwich_tweets()
text_list, user_name_list, tweet_date_list, tweet_id_list = package_sandwich_tweets(response)

print(response.status_code)

#Write output to a .txt file and move it to a s3 bucket
for i in range(len(text_list)):
    date_now = datetime.now().replace(microsecond = 0)
    date_now_str = str(date_now)
    with open('/home/ec2-user/sandwich_tweet/sandwich_tweet%{dt}%{ident}.txt'.format(dt = date_now_str, ident = tweet_id_list[i]), mode = 'w') as f:
        f.write(tweet_id_list[i])
        print(tweet_id_list[i])
        f.write("^&*>*&^")
        f.write(text_list[i])
        f.write("^&*>*&^")
        f.write(user_name_list[i])
        f.write("^&*>*&^")
        f.write(tweet_date_list[i])
        f.write("^&*>*&^")
        f.write(date_now_str)
    s3_resource.Object('sandwich-tweet-chris-cunningham', 'sandwich_tweet%{dt}%{ident}.txt'.format(dt = date_now_str,ident = tweet_id_list[i])).upload_file(Filename = '/home/ec2-user/sandwich_tweet/sandwich_tweet%{dt}%{ident}.txt'.format(dt = date_now_str, ident = tweet_id_list[i]), ExtraArgs = {'ContentType':'text/plan'})




