import boto3
from datetime import date, timedelta, datetime
from pytz import timezone
import psycopg2
import glob


#Grabbing credentials from a text file so they aren't hardcoded in script.
credential_list = []

with open("sandwich_db_credentials.txt") as file:
	lines = file.readlines()
	for line in lines:
		credential_list.append(line)

user_name_str = credential_list[0]
password_str = credential_list[1]

#Creating connection to the PostgreSQL database.
conn = psycopg2.connect(database = 'sandwich_tweets',
		user = user_name_str.strip(),
		password = password_str.strip(),
		host = 'sandwich-tweets.cxors8ly0k2i.us-east-2.rds.amazonaws.com',
		port = '5432'
)

sql_statement = 'INSERT INTO "sandwich_tweets"."tweets"(TEXT,USERNAME,DATE_TWEETED,ID)\
		VALUES (%s, %s, %s, %s)'

#Creating connection to the s3 bucket.
s3_resource = boto3.resource('s3')
s3_bucket = s3_resource.Bucket('sandwich-tweet-chris-cunningham')

#This is going to be used to grab data frome the last hour.
six_hour_delta = timedelta(hours = 6)
now_offset = datetime.now().astimezone(timezone('US/Central'))
today_offset = str(now_offset.date())
time_now_int = int(str(datetime.time(now_offset)).split('.')[0].replace(':',''))

for bucket in s3_bucket.objects.all():
	if today_offset in str(bucket.key) and int(bucket.key.split('%')[1].split(' ')[1].split('-')[0].replace(':', '')) >= time_now_int - 3000 :
		s3_resource.Object('sandwich-tweet-chris-cunningham',
			bucket.key).download_file(Filename = bucket.key)


#Taking the comma seperated list and seperating by comma.
#tweet_list = tweet_info.split(',')
#Converting the ID to an integer
#tweet_list[3] = int(tweet_list[3])


cur = conn.cursor()

file_path_collection = glob.glob('/home/ec2-user/tweet_folder/sandwich_tweet%*')
for file_path in file_path_collection:
	with open(file_path) as file:
		try:
			tweet_info = file.read()
			tweet_list = tweet_info.split('^&*>*&^')
			tweet_list[3] = int(tweet_list[3])
			cur.execute(sql_statement, tweet_list)
			conn.commit()
		except:
			print("this file is an issue: " + tweet_list[1])
cur.close()
