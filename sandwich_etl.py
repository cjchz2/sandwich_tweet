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
		        port = '5432')

sql_statement = ('INSERT INTO "sandwich_tweets"."tweets"(ID,TEXT,USERNAME,TWEET_DATE,PULLED_DATE)'
                 'VALUES (%s, %s, %s, %s, %s)'
                 'ON CONFLICT DO NOTHING')
#Creating connection to the s3 bucket.
s3_resource = boto3.resource('s3')
s3_bucket = s3_resource.Bucket('sandwich-tweet-chris-cunningham')

#This is going to be used to grab data frome the last hour.
#six_hour_delta = timedelta(hours = 6)
now_datetime = datetime.now()
#today_offset = str(now_offset.date())
#time_now_int = int(str(datetime.time(now_offset)).split('.')[0].replace(':',''))

for bucket in s3_bucket.objects.all():
    file_datetime_str = bucket.key[15:34]
    file_datetime = datetime.strptime(file_datetime_str, "%Y-%m-%d %H:%M:%S")
    print(file_datetime)
    if file_datetime > now_datetime - timedelta(hours = 1):
        print('hell yeah')
        s3_resource.Object('sandwich-tweet-chris-cunningham',bucket.key).download_file(Filename = bucket.key)


#Taking the comma seperated list and seperating by comma.
#tweet_list = tweet_info.split(',')
#Converting the ID to an integer
#tweet_list[3] = int(tweet_list[3])


cur = conn.cursor()

file_path_collection = glob.glob('/home/ec2-user/sandwich_tweet/sandwich_tweet%*')
for file_path in file_path_collection:
	with open(file_path) as file:
			print("about to read file")
			tweet_info = file.read()
			print("About to split file")
			tweet_list = tweet_info.split('^&*>*&^')
			print("about to convert id to int")
			tweet_list[0] = int(tweet_list[0])
			print("About to execute SQL")
			cur.execute(sql_statement, tweet_list)
			print("about to write a record")
			conn.commit()
cur.close()
